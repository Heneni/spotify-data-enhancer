#!/usr/bin/env python3
"""
🎵 Spotify Data Enhancer
Enhanced version with comprehensive audio features extraction

Built on the foundation of the successful inline test from devcontainer.json
Processes large datasets efficiently with batch operations and progress tracking
"""

import requests
import base64
import time
import json
import pandas as pd
import os
from typing import List, Dict, Optional
import logging
from tqdm import tqdm
import argparse
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('spotify_enhancement.log'),
        logging.StreamHandler()
    ]
)

class SpotifyDataEnhancer:
    """Enhanced Spotify data processor with batch operations and progress tracking"""
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        # Use provided credentials or default from inline test
        self.client_id = client_id or "efef0dbb87ee4c37b550508ae2791737"
        self.client_secret = client_secret or "09c12b5178734b5aae18743d5b4335d5"
        self.access_token = None
        self.token_expires_at = 0
        self.batch_size = 100  # Spotify API allows up to 100 tracks per batch
        self.rate_limit_delay = 0.1  # 100ms between requests to be conservative
        
    def authenticate(self) -> bool:
        """Authenticate with Spotify API using the successful method from inline test"""
        try:
            print("🔐 Authenticating with Spotify...")
            credentials = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
            
            auth_response = requests.post(
                'https://accounts.spotify.com/api/token',
                headers={
                    'Authorization': f'Basic {credentials}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data='grant_type=client_credentials'
            )
            
            if auth_response.status_code == 200:
                token_data = auth_response.json()
                self.access_token = token_data['access_token']
                self.token_expires_at = time.time() + token_data['expires_in'] - 300  # 5 min buffer
                print("✅ Authentication successful!")
                logging.info("Spotify authentication successful")
                return True
            else:
                print(f"❌ Authentication failed: {auth_response.status_code}")
                logging.error(f"Authentication failed: {auth_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {str(e)}")
            logging.error(f"Authentication error: {str(e)}")
            return False
    
    def ensure_authenticated(self) -> bool:
        """Ensure we have a valid access token"""
        if not self.access_token or time.time() >= self.token_expires_at:
            return self.authenticate()
        return True
    
    def get_audio_features_batch(self, track_ids: List[str]) -> List[Dict]:
        """Get audio features for a batch of tracks (up to 100)"""
        if not self.ensure_authenticated():
            return []
        
        if len(track_ids) > 100:
            raise ValueError("Batch size cannot exceed 100 tracks")
        
        try:
            # Filter out any None or empty track IDs
            valid_ids = [tid for tid in track_ids if tid and len(tid) == 22]
            if not valid_ids:
                return []
            
            ids_string = ','.join(valid_ids)
            url = f'https://api.spotify.com/v1/audio-features?ids={ids_string}'
            
            response = requests.get(
                url,
                headers={'Authorization': f'Bearer {self.access_token}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('audio_features', [])
            elif response.status_code == 429:
                # Rate limited - wait and retry
                retry_after = int(response.headers.get('Retry-After', 1))
                print(f"⏳ Rate limited, waiting {retry_after} seconds...")
                time.sleep(retry_after)
                return self.get_audio_features_batch(track_ids)
            else:
                logging.warning(f"API error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logging.error(f"Error getting audio features: {str(e)}")
            return []
    
    def process_dataset(self, input_file: str, output_file: str, resume: bool = True) -> Dict:
        """Process a large dataset with progress tracking and resumption capability"""
        
        print(f"🎵 Starting Spotify Data Enhancement")
        print(f"📂 Input file: {input_file}")
        print(f"💾 Output file: {output_file}")
        
        # Load input data
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        print("📊 Loading dataset...")
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        elif input_file.endswith('.json'):
            df = pd.read_json(input_file)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")
        
        total_tracks = len(df)
        print(f"🎯 Found {total_tracks:,} tracks to process")
        
        # Check for resume capability
        processed_ids = set()
        if resume and os.path.exists(output_file):
            print("🔄 Resume mode: Loading previous results...")
            try:
                if output_file.endswith('.csv'):
                    existing_df = pd.read_csv(output_file)
                else:
                    existing_df = pd.read_json(output_file)
                
                if 'id' in existing_df.columns:
                    processed_ids = set(existing_df['id'].tolist())
                    print(f"✅ Found {len(processed_ids):,} previously processed tracks")
            except:
                print("⚠️ Could not load existing results, starting fresh")
        
        # Process in batches
        results = []
        failed_count = 0
        success_count = 0
        
        # Identify track ID column
        id_columns = ['id', 'track_id', 'spotify_id', 'trackId']
        id_column = None
        for col in id_columns:
            if col in df.columns:
                id_column = col
                break
        
        if not id_column:
            raise ValueError(f"No track ID column found. Expected one of: {id_columns}")
        
        print(f"🎼 Using '{id_column}' as track ID column")
        
        # Create batches
        remaining_df = df[~df[id_column].isin(processed_ids)] if processed_ids else df
        track_ids = remaining_df[id_column].tolist()
        
        if not track_ids:
            print("✅ All tracks already processed!")
            return {"total": total_tracks, "success": len(processed_ids), "failed": 0}
        
        print(f"🚀 Processing {len(track_ids):,} remaining tracks...")
        
        # Process in batches with progress bar
        with tqdm(total=len(track_ids), desc="Enhancing tracks", unit="tracks") as pbar:
            for i in range(0, len(track_ids), self.batch_size):
                batch_ids = track_ids[i:i + self.batch_size]
                batch_df = remaining_df.iloc[i:i + self.batch_size]
                
                # Get audio features for this batch
                audio_features = self.get_audio_features_batch(batch_ids)
                
                # Merge with original data
                for j, features in enumerate(audio_features):
                    if features:  # Features can be None for invalid tracks
                        row_data = batch_df.iloc[j].to_dict()
                        # Add audio features to the row
                        row_data.update(features)
                        results.append(row_data)
                        success_count += 1
                    else:
                        # Keep original data for failed tracks
                        results.append(batch_df.iloc[j].to_dict())
                        failed_count += 1
                
                pbar.update(len(batch_ids))
                
                # Save intermediate results every 1000 tracks
                if len(results) % 1000 == 0:
                    self._save_intermediate_results(results, output_file, processed_ids)
                
                # Rate limiting
                time.sleep(self.rate_limit_delay)
        
        # Final save
        self._save_final_results(results, output_file, processed_ids)
        
        stats = {
            "total": total_tracks,
            "success": success_count + len(processed_ids),
            "failed": failed_count,
            "enhancement_rate": (success_count + len(processed_ids)) / total_tracks * 100
        }
        
        print(f"\n🎉 Processing complete!")
        print(f"✅ Success: {stats['success']:,} tracks ({stats['enhancement_rate']:.1f}%)")
        print(f"❌ Failed: {stats['failed']:,} tracks")
        print(f"💾 Results saved to: {output_file}")
        
        return stats
    
    def _save_intermediate_results(self, results: List[Dict], output_file: str, processed_ids: set):
        """Save intermediate results during processing"""
        try:
            if output_file.endswith('.csv'):
                pd.DataFrame(results).to_csv(f"{output_file}.tmp", index=False)
            else:
                with open(f"{output_file}.tmp", 'w') as f:
                    json.dump(results, f, indent=2)
            logging.info(f"Saved intermediate results: {len(results)} records")
        except Exception as e:
            logging.error(f"Error saving intermediate results: {str(e)}")
    
    def _save_final_results(self, results: List[Dict], output_file: str, processed_ids: set):
        """Save final results"""
        try:
            if output_file.endswith('.csv'):
                pd.DataFrame(results).to_csv(output_file, index=False)
            else:
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=2)
            
            # Remove temporary file if it exists
            temp_file = f"{output_file}.tmp"
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        except Exception as e:
            logging.error(f"Error saving final results: {str(e)}")
    
    def validate_enhancement(self, output_file: str) -> Dict:
        """Validate the enhancement results"""
        if not os.path.exists(output_file):
            return {"error": "Output file not found"}
        
        try:
            if output_file.endswith('.csv'):
                df = pd.read_csv(output_file)
            else:
                df = pd.read_json(output_file)
            
            # Check for audio features columns
            audio_features_cols = [
                'danceability', 'energy', 'key', 'loudness', 'mode',
                'speechiness', 'acousticness', 'instrumentalness',
                'liveness', 'valence', 'tempo', 'duration_ms'
            ]
            
            enhanced_cols = [col for col in audio_features_cols if col in df.columns]
            enhanced_count = df[enhanced_cols[0]].notna().sum() if enhanced_cols else 0
            
            return {
                "total_rows": len(df),
                "enhanced_rows": enhanced_count,
                "enhancement_rate": enhanced_count / len(df) * 100,
                "audio_features_columns": enhanced_cols
            }
            
        except Exception as e:
            return {"error": str(e)}

def main():
    """Main execution function with command line interface"""
    parser = argparse.ArgumentParser(description='Enhance Spotify data with audio features')
    parser.add_argument('input', help='Input file (CSV or JSON)')
    parser.add_argument('-o', '--output', help='Output file (default: enhanced_<input>)')
    parser.add_argument('--client-id', help='Spotify Client ID')
    parser.add_argument('--client-secret', help='Spotify Client Secret')
    parser.add_argument('--no-resume', action='store_true', help='Start fresh (ignore existing results)')
    parser.add_argument('--validate', action='store_true', help='Validate enhancement results only')
    
    args = parser.parse_args()
    
    # Determine output file
    if not args.output:
        name, ext = os.path.splitext(args.input)
        args.output = f"{name}_enhanced{ext}"
    
    # Create enhancer instance
    enhancer = SpotifyDataEnhancer(args.client_id, args.client_secret)
    
    if args.validate:
        # Validation mode
        print("🔍 Validating enhancement results...")
        results = enhancer.validate_enhancement(args.output)
        
        if "error" in results:
            print(f"❌ Validation error: {results['error']}")
            return 1
        
        print(f"📊 Validation Results:")
        print(f"   Total rows: {results['total_rows']:,}")
        print(f"   Enhanced rows: {results['enhanced_rows']:,}")
        print(f"   Enhancement rate: {results['enhancement_rate']:.1f}%")
        print(f"   Audio features: {', '.join(results['audio_features_columns'])}")
        
        return 0
    
    try:
        # Run the enhancement
        start_time = time.time()
        stats = enhancer.process_dataset(
            args.input, 
            args.output, 
            resume=not args.no_resume
        )
        processing_time = time.time() - start_time
        
        print(f"\n⏱️ Total processing time: {processing_time/60:.1f} minutes")
        print(f"⚡ Processing rate: {stats['success']/(processing_time/60):.0f} tracks/minute")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        logging.error(f"Main execution error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
