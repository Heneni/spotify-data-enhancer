#!/usr/bin/env python3
"""
Spotify Data Enhancer - Python Version
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
    def __init__(self, client_id=None, client_secret=None):
        self.CLIENT_ID = client_id or os.getenv('SPOTIFY_CLIENT_ID', 'efef0dbb87ee4c37b550508ae2791737')
        self.CLIENT_SECRET = client_secret or os.getenv('SPOTIFY_CLIENT_SECRET', '09c12b5178734b5aae18743d5b4335d5')
        self.access_token = None
        self.session = requests.Session()
        
    def authenticate(self) -> bool:
        """Authenticate with Spotify API using Client Credentials flow"""
        try:
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
                data=data
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                print("✅ Successfully authenticated with Spotify API")
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
            return uri.split(':')[2]
        elif '/track/' in uri:
            return uri.split('/track/')[1].split('?')[0]
        else:
            # Assume it's already just the ID
            return uri if len(uri) == 22 else None
    
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
                    headers=headers
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    # Rate limited
                    retry_after = int(response.headers.get('Retry-After', 1))
                    print(f"⏳ Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                else:
                    print(f"❌ API request failed: {response.status_code}")
                    print(f"Response: {response.text}")
                    return None
                    
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
            
        # Filter out invalid IDs
        valid_ids = [tid for tid in track_ids if tid and len(tid) == 22]
        if not valid_ids:
            return []
        
        # Spotify API allows up to 100 tracks per request
        endpoint = f"/v1/audio-features?ids={','.join(valid_ids[:100])}"
        response = self.make_spotify_request(endpoint)
        
        if response and 'audio_features' in response:
            return response['audio_features'] or []
        return []
    
    def fetch_audio_analysis(self, track_id: str) -> Optional[Dict]:
        """Fetch detailed audio analysis for a single track"""
        if not track_id or len(track_id) != 22:
            return None
            
        endpoint = f"/v1/audio-analysis/{track_id}"
        return self.make_spotify_request(endpoint)
    
    def enhance_tracks(self, df: pd.DataFrame, include_analysis: bool = False, max_analysis: int = 100) -> pd.DataFrame:
        """Enhance tracks DataFrame with Spotify data"""
        print(f"📊 Processing {len(df)} tracks...")
        
        enhanced_df = df.copy()
        batch_size = 50  # Conservative batch size
        processed = 0
        errors = 0
        analysis_count = 0
        
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
        
        for col in feature_columns:
            enhanced_df[col] = None
        
        # Process in batches
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(df) + batch_size - 1) // batch_size
            
            print(f"🔄 Processing batch {batch_num}/{total_batches} ({len(batch)} tracks)")
            
            # Extract track IDs from batch
            track_ids = []
            batch_indices = []
            
            for idx, row in batch.iterrows():
                track_id = self.extract_track_id(row.get('spotify_track_uri', ''))
                if track_id:
                    track_ids.append(track_id)
                    batch_indices.append(idx)
            
            if not track_ids:
                errors += len(batch)
                continue
            
            # Fetch audio features for batch
            audio_features = self.fetch_audio_features_batch(track_ids)
            
            # Process each track in batch
            for j, (track_id, df_idx) in enumerate(zip(track_ids, batch_indices)):
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
                    
                    # Add detailed analysis if requested and within limit
                    if include_analysis and analysis_count < max_analysis:
                        print(f"🔍 Fetching detailed analysis for track {analysis_count + 1}/{max_analysis}...")
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
                        
                        analysis_count += 1
                        # Add delay for analysis requests
                        time.sleep(0.2)
                    
                    processed += 1
                else:
                    errors += 1
            
            # Progress update
            print(f"✅ Progress: {processed}/{len(df)} processed, {errors} errors")
            if include_analysis:
                print(f"🔍 Analysis: {analysis_count}/{max_analysis} completed")
            
            # Add delay between batches
            time.sleep(0.1)
        
        print(f"🎉 Enhancement complete! {processed} enhanced, {errors} errors")
        return enhanced_df
    
    def process_file(self, input_path: str, output_path: str, include_analysis: bool = False, max_analysis: int = 100):
        """Process CSV file and enhance with Spotify data"""
        try:
            print("🎵 Spotify Data Enhancer")
            print("========================")
            print(f"📄 Input file: {input_path}")
            print(f"💾 Output file: {output_path}")
            print(f"🔍 Include analysis: {'Yes' if include_analysis else 'No'}")
            if include_analysis:
                print(f"📊 Max analysis tracks: {max_analysis}")
            print()
            
            # Authenticate
            if not self.authenticate():
                raise Exception("Authentication failed")
            
            # Load CSV
            print(f"📁 Loading {input_path}...")
            df = pd.read_csv(input_path)
            print(f"📊 Loaded {len(df)} tracks with {len(df.columns)} columns")
            
            # Show first few track URIs for debugging
            if 'spotify_track_uri' in df.columns:
                print(f"📝 Sample URIs:")
                for i, uri in enumerate(df['spotify_track_uri'].head(3)):
                    track_id = self.extract_track_id(uri)
                    print(f"  {i+1}. {uri} -> {track_id}")
            
            # Enhance data
            enhanced_df = self.enhance_tracks(df, include_analysis, max_analysis)
            
            # Save enhanced data
            print(f"💾 Saving enhanced data to {output_path}...")
            enhanced_df.to_csv(output_path, index=False)
            print(f"✅ Enhanced data saved successfully!")
            
            # Print summary
            new_columns = len(enhanced_df.columns) - len(df.columns)
            print(f"📈 Added {new_columns} new columns to your data")
            
            # Show some statistics
            feature_cols = [col for col in enhanced_df.columns if col.startswith('enhanced_')]
            for col in feature_cols[:5]:  # Show first 5 enhanced columns
                non_null = enhanced_df[col].notna().sum()
                print(f"  - {col}: {non_null} tracks enhanced")
            
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Enhance Spotify track data with audio features')
    parser.add_argument('input', nargs='?', default='tracks_for_import.csv', help='Input CSV file path')
    parser.add_argument('output', nargs='?', default='enhanced_spotify_tracks.csv', help='Output CSV file path')
    parser.add_argument('--analysis', action='store_true', help='Include detailed audio analysis')
    parser.add_argument('--max-analysis', type=int, default=100, help='Maximum number of tracks to analyze in detail')
    parser.add_argument('--client-id', help='Spotify Client ID')
    parser.add_argument('--client-secret', help='Spotify Client Secret')
    
    args = parser.parse_args()
    
    enhancer = SpotifyDataEnhancer(args.client_id, args.client_secret)
    enhancer.process_file(args.input, args.output, args.analysis, args.max_analysis)

if __name__ == '__main__':
    main()
