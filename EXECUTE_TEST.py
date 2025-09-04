#!/usr/bin/env python3
"""
DIRECT EXECUTION: Run the 1000-record test now
This will run immediately and show results
"""

import requests
import pandas as pd
import time
import base64
import json

def run_test_now():
    print("🚀 EXECUTING 1000-Record Spotify Test...")
    print("=" * 50)
    
    # Spotify credentials
    CLIENT_ID = 'efef0dbb87ee4c37b550508ae2791737'
    CLIENT_SECRET = '09c12b5178734b5aae18743d5b4335d5'
    
    # Step 1: Authenticate
    print("🔐 Authenticating with Spotify API...")
    
    try:
        credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        
        auth_response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={
                'Authorization': f'Basic {credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={'grant_type': 'client_credentials'},
            timeout=10
        )
        
        if auth_response.status_code != 200:
            print(f"❌ Authentication failed: {auth_response.status_code}")
            print(f"Response: {auth_response.text}")
            return
        
        token_data = auth_response.json()
        access_token = token_data['access_token']
        print(f"✅ Authentication successful! Token expires in {token_data.get('expires_in', 'unknown')} seconds")
        
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return
    
    # Step 2: Create test data
    print("\n📊 Creating 1000 test tracks...")
    
    popular_tracks = [
        ('Shape of You', 'Ed Sheeran', '7qiZfU4dY1lWllzX7mPBI3'),
        ('Blinding Lights', 'The Weeknd', '0VjIjW4GlUZAMYd2vXMi3b'),
        ('Watermelon Sugar', 'Harry Styles', '6UelLqGlWMcVH1E5c4H7lY'),
        ('Levitating', 'Dua Lipa', '463CkQjx2Zk1yXoBuierM9'),
        ('Anti-Hero', 'Taylor Swift', '0V3wPSX9ygBnCm8psDIegu'),
        ('As It Was', 'Harry Styles', '4Dvkj6JhhA12EX05fT7y2e'),
        ('Heat Waves', 'Glass Animals', '02MWAaffLxlfxAUY7c5dvx'),
        ('Stay', 'The Kid LAROI & Justin Bieber', '5HCyWlXZPP0y6Gqq8TgA20'),
        ('Good 4 U', 'Olivia Rodrigo', '4ZtFanR9U6ndgddUvNcjcG'),
        ('Peaches', 'Justin Bieber ft. Daniel Caesar', '4iJyoBOLtHqaGxP12qzhQI'),
    ]
    
    test_data = []
    for i in range(1000):
        base_track = popular_tracks[i % len(popular_tracks)]
        test_data.append({
            'track_id': f'test_{i+1}',
            'track': base_track[0],
            'artist': base_track[1],
            'spotify_track_uri': f'spotify:track:{base_track[2]}',
            'energy': round(0.3 + (i % 7) * 0.1, 3),
            'valence': round(0.2 + (i % 8) * 0.1, 3),
        })
    
    print(f"✅ Created {len(test_data)} test tracks")
    
    # Step 3: Process in batches
    print(f"\n🔄 Processing tracks in batches...")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    batch_size = 50
    processed = 0
    errors = 0
    enhanced_data = []
    start_time = time.time()
    
    for i in range(0, len(test_data), batch_size):
        batch = test_data[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(test_data) + batch_size - 1) // batch_size
        
        print(f"\n   🔄 Batch {batch_num}/{total_batches} ({len(batch)} tracks)")
        
        # Extract track IDs
        track_ids = [track['spotify_track_uri'].split(':')[2] for track in batch]
        
        try:
            # Call Spotify API
            features_response = requests.get(
                f"https://api.spotify.com/v1/audio-features?ids={','.join(track_ids)}",
                headers=headers,
                timeout=30
            )
            
            if features_response.status_code == 200:
                features_data = features_response.json()
                audio_features = features_data.get('audio_features', [])
                
                print(f"   ✅ Retrieved {len([f for f in audio_features if f])} audio features")
                
                # Merge with original data
                for j, track in enumerate(batch):
                    enhanced_track = track.copy()
                    
                    if j < len(audio_features) and audio_features[j]:
                        features = audio_features[j]
                        enhanced_track.update({
                            'enhanced_acousticness': features.get('acousticness'),
                            'enhanced_danceability': features.get('danceability'), 
                            'enhanced_energy': features.get('energy'),
                            'enhanced_tempo': features.get('tempo'),
                            'enhanced_valence': features.get('valence'),
                            'enhanced_loudness': features.get('loudness'),
                            'duration_ms': features.get('duration_ms'),
                        })
                        processed += 1
                    else:
                        errors += 1
                        
                    enhanced_data.append(enhanced_track)
                
                success_rate = (processed / (processed + errors)) * 100 if (processed + errors) > 0 else 0
                print(f"   📊 Progress: {processed} enhanced, {errors} errors ({success_rate:.1f}% success)")
                
            elif features_response.status_code == 429:
                # Rate limited
                retry_after = int(features_response.headers.get('Retry-After', 1))
                print(f"   ⏳ Rate limited, waiting {retry_after} seconds...")
                time.sleep(retry_after)
                continue
                
            else:
                print(f"   ❌ API error: {features_response.status_code}")
                errors += len(batch)
                enhanced_data.extend(batch)
        
        except Exception as e:
            print(f"   ❌ Batch error: {e}")
            errors += len(batch)
            enhanced_data.extend(batch)
        
        # Small delay between batches
        time.sleep(0.2)
    
    # Results
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n🎉 TEST COMPLETED!")
    print(f"⏱️  Total time: {duration/60:.1f} minutes")
    print(f"📊 Final results:")
    print(f"   • Total tracks: {len(enhanced_data)}")
    print(f"   • Successfully enhanced: {processed}")
    print(f"   • Errors: {errors}")
    print(f"   • Success rate: {(processed/len(enhanced_data)*100):.1f}%")
    print(f"   • Processing speed: {len(enhanced_data)/(duration/60):.0f} tracks/minute")
    
    # Save results
    df = pd.DataFrame(enhanced_data)
    output_file = 'test_results_1000.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    print(f"📁 File contains {len(df)} rows and {len(df.columns)} columns")
    
    # Show sample enhanced data
    enhanced_cols = [col for col in df.columns if 'enhanced_' in col]
    if enhanced_cols and processed > 0:
        sample_row = df[df['enhanced_energy'].notna()].iloc[0] if any(df['enhanced_energy'].notna()) else None
        if sample_row is not None:
            print(f"\n🎵 Sample enhanced data for '{sample_row['track']}':")
            for col in enhanced_cols:
                if pd.notna(sample_row[col]):
                    print(f"   • {col}: {sample_row[col]}")
    
    # Estimate full dataset time  
    if duration > 0:
        estimated_full = (duration / len(test_data)) * 54513 / 3600  # hours
        print(f"\n📊 Estimated time for full 54,513 tracks: {estimated_full:.1f} hours")
    
    print(f"\n✅ 1000-RECORD TEST COMPLETE!")
    print(f"🚀 Ready to process your full dataset!")

if __name__ == '__main__':
    run_test_now()
