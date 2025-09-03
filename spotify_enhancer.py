#!/usr/bin/env python3
"""
Spotify Data Enhancer for GitHub Codespaces
Enhances your Spotify track data with audio features and analysis
"""

import requests
import pandas as pd
import time
import json
import base64
from typing import List, Dict, Optional
import argparse
import sys
import os

class SpotifyDataEnhancer:
    def __init__(self):
        self.CLIENT_ID = 'efef0dbb87ee4c37b550508ae2791737'
        self.CLIENT_SECRET = '09c12b5178734b5aae18743d5b4335d5'
        self.access_token = None
        self.session = requests.Session()
        
    def authenticate(self) -> bool:
        """Authenticate with Spotify API using Client Credentials flow"""
        try:
            print("🔐 Authenticating with Spotify API...")
            
            # Encode credentials
            credentials = base64.b64encode(
                f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode()
            ).decode()
            
            headers = {
                'Authorization': f'Basic {credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {'grant_type': 'client_credentials'}
            
            response = self.session.post(
                'https://accounts.spotify.com/api/token',
                headers=headers,
                data=data,
                timeout=10
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                expires_in = token_data.get('expires_in', 3600)
                print(f"✅ Successfully authenticated! Token expires in {expires_in} seconds")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def extract_track_id(self, uri: str) -> Optional[str]:
        """Extract Spotify track ID from URI or URL"""
        if not uri:
            return None
            
        if 'spotify:track:' in uri:
            track_id = uri.split(':')[2]
        elif '/track/' in uri:
            track_id = uri.split('/track/')[1].split('?')[0]
        else:
            track_id = uri.strip()
            
        # Validate track ID format (22 characters, alphanumeric)
        if len(track_id) == 22 and track_id.replace('_', '').replace('-', '').isalnum():
            return track_id
        return None
    
    def make_spotify_request(self, endpoint: str, max_retries: int = 3) -> Optional[Dict]:
        """Make request to Spotify API with retry logic"""
        if not self.access_token:
            print("❌ Not authenticated")
            return None
            
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(
                    f'https://api.spotify.com{endpoint}',
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    # Rate limited
                    retry_after = int(response.headers.get('Retry-After', 1))
                    print(f"⏳ Rate limited. Waiting {retry_after} seconds... (attempt {attempt + 1})")
                    time.sleep(retry_after)
                    continue
                elif response.status_code == 401:
                    print("🔐 Token expired, re-authenticating...")
                    if self.authenticate():
                        headers = {'Authorization': f'Bearer {self.access_token}'}
                        continue
                    else:
                        return None
                else:
                    print(f"❌ API request failed: {response.status_code} - {response.text}")
                    return None
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Request timeout (attempt {attempt + 1})")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
            except Exception as e:
                print(f"❌ Request error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                    
        return None
    
    def fetch_audio_features_batch(self, track_ids: List[str]) -> List[Dict]:
        """Fetch audio features for multiple tracks (up to 100)"""
        if not track_ids:
            return []
            
        # Filter out invalid IDs and limit to 100
        valid_ids = [tid for tid in track_ids if tid and len(tid) == 22][:100]
        if not valid_ids:
            return []
        
        endpoint = f"/v1/audio-features?ids={','.join(valid_ids)}"
        response = self.make_spotify_request(endpoint)
        
        if response and 'audio_features' in response:
            return [f for f in response['audio_features'] if f is not None]
        return []
    
    def fetch_audio_analysis(self, track_id: str) -> Optional[Dict]:
        """Fetch detailed audio analysis for a single track"""
        if not track_id or len(track_id) != 22:
            return None
            
        endpoint = f"/v1/audio-analysis/{track_id}"
        return self.make_spotify_request(endpoint)
    
    def enhance_tracks(self, df: pd.DataFrame, include_analysis: bool = False, sample_size: Optional[int] = None) -> pd.DataFrame:
        """Enhance tracks DataFrame with Spotify data"""
        
        # Sample data if requested (for testing)
        if sample_size and sample_size < len(df):
            print(f"🎯 Sampling {sample_size} tracks for testing...")
            df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
        
        print(f"📊 Processing {len(df)} tracks...")
        
        enhanced_df = df.copy()
        batch_size = 50  # Conservative batch size
        processed = 0
        errors = 0
        analysis_processed = 0
        
        # Add new columns for enhanced features
        feature_columns = [
            'enhanced_acousticness', 'enhanced_danceability', 'enhanced_energy',
            'enhanced_instrumentalness', 'enhanced_liveness', 'enhanced_loudness',
            'enhanced_speechiness', 'enhanced_tempo', 'enhanced_valence',
            'enhanced_key', 'enhanced_mode', 'enhanced_time_signature', 'duration_ms'
        ]
        
        if include_analysis:
            analysis_columns = [
                'bars_count', 'beats_count', 'sections_count', 'segments_count',
                'tatums_count', 'first_section_tempo', 'first_section_loudness',
                'first_section_key', 'first_section_mode'
            ]
            feature_columns.extend(analysis_columns)
        
        # Initialize new columns
        for col in feature_columns:
            enhanced_df[col] = None
        
        # Process in batches
        total_batches = (len(df) + batch_size - 1) // batch_size
        
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            batch_num = i // batch_size + 1
            
            print(f"\n🔄 Processing batch {batch_num}/{total_batches} ({len(batch)} tracks)")
            
            # Extract track IDs from batch
            track_ids = []
            batch_indices = []
            
            for idx, row in batch.iterrows():
                track_id = self.extract_track_id(row.get('spotify_track_uri', ''))
                if track_id:
                    track_ids.append(track_id)
                    batch_indices.append(idx)
            
            print(f"   📋 Found {len(track_ids)} valid track IDs in batch")
            
            if not track_ids:
                errors += len(batch)
                print(f"   ❌ No valid track IDs found in batch")
                continue
            
            # Fetch audio features for batch
            audio_features = self.fetch_audio_features_batch(track_ids)
            print(f"   ✅ Retrieved {len(audio_features)} audio feature sets")
            
            # Process each track in batch
            for track_id, df_idx in zip(track_ids, batch_indices):
                features = None
                
                # Find features for this track
                for feature in audio_features:
                    if feature and feature.get('id') == track_id:
                        features = feature
                        break
                
                if features:
                    # Add audio features
                    enhanced_df.loc[df_idx, 'enhanced_acousticness'] = features.get('acousticness')
                    enhanced_df.loc[df_idx, 'enhanced_danceability'] = features.get('danceability')
                    enhanced_df.loc[df_idx, 'enhanced_energy'] = features.get('energy')
                    enhanced_df.loc[df_idx, 'enhanced_instrumentalness'] = features.get('instrumentalness')
                    enhanced_df.loc[df_idx, 'enhanced_liveness'] = features.get('liveness')
                    enhanced_df.loc[df_idx, 'enhanced_loudness'] = features.get('loudness')
                    enhanced_df.loc[df_idx, 'enhanced_speechiness'] = features.get('speechiness')
                    enhanced_df.loc[df_idx, 'enhanced_tempo'] = features.get('tempo')
                    enhanced_df.loc[df_idx, 'enhanced_valence'] = features.get('valence')
                    enhanced_df.loc[df_idx, 'enhanced_key'] = features.get('key')
                    enhanced_df.loc[df_idx, 'enhanced_mode'] = features.get('mode')
                    enhanced_df.loc[df_idx, 'enhanced_time_signature'] = features.get('time_signature')
                    enhanced_df.loc[df_idx, 'duration_ms'] = features.get('duration_ms')
                    
                    # Add detailed analysis if requested (for all tracks when analysis=True)
                    if include_analysis:
                        if analysis_processed % 50 == 0:  # Log progress every 50 analyses
                            print(f"   🔍 Fetching detailed analysis ({analysis_processed + 1})...")
                        
                        analysis = self.fetch_audio_analysis(track_id)
                        
                        if analysis:
                            enhanced_df.loc[df_idx, 'bars_count'] = len(analysis.get('bars', []))
                            enhanced_df.loc[df_idx, 'beats_count'] = len(analysis.get('beats', []))
                            enhanced_df.loc[df_idx, 'sections_count'] = len(analysis.get('sections', []))
                            enhanced_df.loc[df_idx, 'segments_count'] = len(analysis.get('segments', []))
                            enhanced_df.loc[df_idx, 'tatums_count'] = len(analysis.get('tatums', []))
                            
                            sections = analysis.get('sections', [])
                            if sections:
                                first_section = sections[0]
                                enhanced_df.loc[df_idx, 'first_section_tempo'] = first_section.get('tempo')
                                enhanced_df.loc[df_idx, 'first_section_loudness'] = first_section.get('loudness')
                                enhanced_df.loc[df_idx, 'first_section_key'] = first_section.get('key')
                                enhanced_df.loc[df_idx, 'first_section_mode'] = first_section.get('mode')
                            
                            analysis_processed += 1
                        
                        # Add delay for analysis requests
                        time.sleep(0.1)
                    
                    processed += 1
                else:
                    errors += 1
            
            # Progress update
            success_rate = (processed / (processed + errors) * 100) if (processed + errors) > 0 else 0
            print(f"   📊 Batch complete: {processed} total processed, {errors} errors ({success_rate:.1f}% success)")
            if include_analysis:
                print(f"   🔍 Analysis completed: {analysis_processed} tracks")
            
            # Add delay between batches to be nice to the API
            time.sleep(0.3)
        
        print(f"\n🎉 Enhancement complete!")
        print(f"📈 Final stats: {processed} enhanced, {errors} errors out of {len(df)} total tracks")
        print(f"✅ Success rate: {(processed / len(df) * 100):.1f}%")
        if include_analysis:
            print(f"🔍 Analysis completed for {analysis_processed} tracks")
        
        return enhanced_df
    
    def process_file(self, input_path: str, output_path: str, include_analysis: bool = False, sample_size: Optional[int] = None):
        """Process CSV file and enhance with Spotify data"""
        try:
            print("🎵 Spotify Data Enhancer - Codespace Edition")
            print("=" * 45)
            print(f"📄 Input file: {input_path}")
            print(f"💾 Output file: {output_path}")
            print(f"🔍 Include analysis: {'Yes' if include_analysis else 'No'}")
            if sample_size:
                print(f"🎯 Sample size: {sample_size} tracks")
            print()
            
            # Check if input file exists
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Input file not found: {input_path}")
            
            # Authenticate
            if not self.authenticate():
                raise Exception("Authentication failed")
            
            # Load CSV
            print(f"📁 Loading {input_path}...")
            try:
                df = pd.read_csv(input_path)
                print(f"📊 Loaded {len(df)} tracks with {len(df.columns)} columns")
                
                # Show sample of data
                if 'spotify_track_uri' in df.columns:
                    valid_uris = df['spotify_track_uri'].notna().sum()
                    print(f"🎯 Found {valid_uris} non-empty Spotify URIs")
                    
                    # Show sample URIs
                    sample_uris = df['spotify_track_uri'].dropna().head(3).tolist()
                    print(f"📋 Sample URIs: {sample_uris}")
                else:
                    print("⚠️  Warning: No 'spotify_track_uri' column found")
                    print("Available columns:", list(df.columns))
                    
            except Exception as e:
                raise Exception(f"Failed to load CSV: {e}")
            
            # Enhance data
            enhanced_df = self.enhance_tracks(df, include_analysis, sample_size)
            
            # Save enhanced data
            print(f"\n💾 Saving enhanced data to {output_path}...")
            enhanced_df.to_csv(output_path, index=False)
            print(f"✅ Enhanced data saved successfully!")
            
            # Print summary
            new_columns = len(enhanced_df.columns) - len(df.columns)
            print(f"\n📈 Summary:")
            print(f"   • Added {new_columns} new columns")
            print(f"   • Original size: {len(df)} rows × {len(df.columns)} columns")
            print(f"   • Enhanced size: {len(enhanced_df)} rows × {len(enhanced_df.columns)} columns")
            print(f"   • Output file size: {os.path.getsize(output_path) / 1024 / 1024:.1f} MB")
            
            # Show new column names
            enhanced_cols = [col for col in enhanced_df.columns if 'enhanced_' in col or col in ['duration_ms', 'bars_count', 'beats_count', 'sections_count']]
            print(f"\n🆕 New columns added: {', '.join(enhanced_cols[:10])}{'...' if len(enhanced_cols) > 10 else ''}")
            
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Enhance Spotify track data with audio features')
    parser.add_argument('input', nargs='?', default='tracks_for_import.csv', 
                       help='Input CSV file path (default: tracks_for_import.csv)')
    parser.add_argument('output', nargs='?', default='enhanced_spotify_tracks.csv', 
                       help='Output CSV file path (default: enhanced_spotify_tracks.csv)')
    parser.add_argument('--analysis', action='store_true', 
                       help='Include detailed audio analysis for ALL tracks')
    parser.add_argument('--sample', type=int, 
                       help='Process only a sample of tracks (for testing)')
    
    args = parser.parse_args()
    
    enhancer = SpotifyDataEnhancer()
    enhancer.process_file(args.input, args.output, args.analysis, args.sample)

if __name__ == '__main__':
    main()