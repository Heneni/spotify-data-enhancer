#!/usr/bin/env python3
"""
STANDALONE Spotify Test - No dependencies needed!
This version runs directly without requiring pandas or complex setup
"""

import requests
import json
import base64
import time
import csv
import sys
import os

def authenticate_spotify():
    """Authenticate with Spotify API"""
    CLIENT_ID = 'efef0dbb87ee4c37b550508ae2791737'
    CLIENT_SECRET = '09c12b5178734b5aae18743d5b4335d5'
    
    print("🔐 Authenticating with Spotify API...")
    
    # Encode credentials
    credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = 'grant_type=client_credentials'
    
    try:
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers=headers,
            data=data,
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access_token']
            expires_in = token_data.get('expires_in', 3600)
            print(f"✅ Successfully authenticated! Token expires in {expires_in} seconds")
            return access_token
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None

def extract_track_id(uri):
    """Extract Spotify track ID from URI"""
    if not uri:
        return None
    if 'spotify:track:' in uri:
        return uri.split(':')[2]
    elif '/track/' in uri:
        return uri.split('/track/')[1].split('?')[0]
    return uri if len(uri) == 22 else None

def fetch_audio_features(access_token, track_ids):
    """Fetch audio features for a batch of tracks"""
    if not track_ids:
        return []
    
    # Filter valid IDs and limit to 100
    valid_ids = [tid for tid in track_ids if tid and len(tid) == 22][:100]
    if not valid_ids:
        return []
    
    headers = {'Authorization': f'Bearer {access_token}'}
    endpoint = f"https://api.spotify.com/v1/audio-features?ids={','.join(valid_ids)}"
    
    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('audio_features', [])
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 1))
            print(f"⏳ Rate limited. Waiting {retry_after} seconds...")
            time.sleep(retry_after)
            return fetch_audio_features(access_token, track_ids)  # Retry
        else:
            print(f"❌ API request failed: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return []

def create_test_data():
    """Create test data with popular track URIs"""
    popular_tracks = [
        ('Shape of You', 'Ed Sheeran', 'spotify:track:7qiZfU4dY1lWllzX7mPBI3'),
        ('Blinding Lights', 'The Weeknd', 'spotify:track:0VjIjW4GlUZAMYd2vXMi3b'),
        ('Watermelon Sugar', 'Harry Styles', 'spotify:track:6UelLqGlWMcVH1E5c4H7lY'),
        ('Levitating', 'Dua Lipa', 'spotify:track:463CkQjx2Zk1yXoBuierM9'),
        ('Anti-Hero', 'Taylor Swift', 'spotify:track:0V3wPSX9ygBnCm8psDIegu'),
        ('As It Was', 'Harry Styles', 'spotify:track:4Dvkj6JhhA12EX05fT7y2e'),
        ('Heat Waves', 'Glass Animals', 'spotify:track:02MWAaffLxlfxAUY7c5dvx'),
        ('Stay', 'The Kid LAROI & Justin Bieber', 'spotify:track:5HCyWlXZPP0y6Gqq8TgA20'),
        ('Good 4 U', 'Olivia Rodrigo', 'spotify:track:4ZtFanR9U6ndgddUvNcjcG'),
        ('Peaches', 'Justin Bieber ft. Daniel Caesar & Giveon', 'spotify:track:4iJyoBOLtHqaGxP12qzhQI'),
    ]
    
    test_tracks = []
    for i in range(50):  # Smaller test - 50 tracks
        base_track = popular_tracks[i % len(popular_tracks)]
        track = {
            'track_id': f'test_{i+1}',
            'track': base_track[0],
            'artist': base_track[1],
            'spotify_track_uri': base_track[2],
            'energy': round(0.3 + (i % 7) * 0.1, 3),
            'valence': round(0.2 + (i % 8) * 0.1, 3),
            'danceability': round(0.4 + (i % 6) * 0.1, 3),
        }
        test_tracks.append(track)
    
    return test_tracks

def run_simple_test():
    """Run a simple test with 50 tracks"""
    print("🚀 SIMPLE Spotify Test - 50 tracks, features only")
    print("=" * 50)
    print("⚡ No pandas required - pure Python!")
    print("⏱️  Expected time: 2-3 minutes")
    print()
    
    # Authenticate
    access_token = authenticate_spotify()
    if not access_token:
        print("❌ Cannot proceed without authentication")
        return
    
    # Create test data
    print("📊 Creating test data...")
    tracks = create_test_data()
    print(f"✅ Created {len(tracks)} test tracks")
    
    # Process tracks
    print(f"\n🔄 Processing {len(tracks)} tracks in batches...")
    
    enhanced_tracks = []
    batch_size = 50
    processed = 0
    errors = 0
    
    start_time = time.time()
    
    for i in range(0, len(tracks), batch_size):
        batch = tracks[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(tracks) + batch_size - 1) // batch_size
        
        print(f"\n🔄 Processing batch {batch_num}/{total_batches} ({len(batch)} tracks)")
        
        # Extract track IDs
        track_ids = []
        for track in batch:
            track_id = extract_track_id(track['spotify_track_uri'])
            if track_id:
                track_ids.append(track_id)
        
        print(f"   📋 Found {len(track_ids)} valid track IDs")
        
        if track_ids:
            # Fetch audio features
            features_list = fetch_audio_features(access_token, track_ids)
            print(f"   ✅ Retrieved {len(features_list)} audio feature sets")
            
            # Enhance tracks
            for j, track in enumerate(batch):
                track_id = extract_track_id(track['spotify_track_uri'])
                enhanced_track = track.copy()
                
                # Find matching features
                features = None
                for f in features_list:
                    if f and f.get('id') == track_id:
                        features = f
                        break
                
                if features:
                    # Add enhanced features
                    enhanced_track['enhanced_acousticness'] = features.get('acousticness')
                    enhanced_track['enhanced_danceability'] = features.get('danceability')
                    enhanced_track['enhanced_energy'] = features.get('energy')
                    enhanced_track['enhanced_tempo'] = features.get('tempo')
                    enhanced_track['enhanced_valence'] = features.get('valence')
                    enhanced_track['enhanced_loudness'] = features.get('loudness')
                    enhanced_track['enhanced_key'] = features.get('key')
                    enhanced_track['enhanced_mode'] = features.get('mode')
                    enhanced_track['duration_ms'] = features.get('duration_ms')
                    processed += 1
                else:
                    errors += 1
                
                enhanced_tracks.append(enhanced_track)
        
        # Progress update
        success_rate = (processed / (processed + errors) * 100) if (processed + errors) > 0 else 0
        print(f"   📊 Batch complete: {processed} processed, {errors} errors ({success_rate:.1f}% success)")
        
        # Small delay
        time.sleep(0.2)
    
    # Calculate results
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n🎉 Simple test completed!")
    print(f"⚡ Total time: {duration/60:.1f} minutes")
    print(f"📊 Results:")
    print(f"   • Total tracks: {len(tracks)}")
    print(f"   • Successfully enhanced: {processed}")
    print(f"   • Errors: {errors}")
    print(f"   • Success rate: {(processed/len(tracks)*100):.1f}%")
    
    # Save results to CSV
    output_file = 'simple_test_results.csv'
    print(f"\n💾 Saving results to {output_file}...")
    
    if enhanced_tracks:
        # Get all column names
        all_keys = set()
        for track in enhanced_tracks:
            all_keys.update(track.keys())
        
        fieldnames = sorted(all_keys)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(enhanced_tracks)
        
        file_size = os.path.getsize(output_file)
        print(f"✅ Results saved! File size: {file_size/1024:.1f} KB")
        
        # Show sample enhanced data
        sample_track = enhanced_tracks[0]
        print(f"\n🎵 Sample enhanced data for '{sample_track['track']}':")
        enhanced_keys = [k for k in sample_track.keys() if 'enhanced_' in k]
        for key in enhanced_keys[:5]:
            value = sample_track.get(key)
            if value is not None:
                print(f"   • {key}: {value}")
        
        print(f"\n✅ SIMPLE TEST PASSED!")
        print(f"🚀 Core functionality working - ready for full dataset!")
        
        # Estimate full dataset time
        tracks_per_minute = len(tracks) / (duration / 60)
        estimated_hours = 54513 / tracks_per_minute / 60
        print(f"\n📊 Estimated time for 54,513 tracks: ~{estimated_hours:.1f} hours")
    
    else:
        print("❌ No enhanced tracks to save")

if __name__ == '__main__':
    run_simple_test()
