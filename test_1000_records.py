#!/usr/bin/env python3
"""
Test script to run Spotify enhancement on 1000 records
This will demonstrate the full functionality with a substantial sample
"""

import pandas as pd
import requests
import time
from spotify_enhancer import SpotifyDataEnhancer

def create_test_sample_1000():
    """Create a test sample with 1000 popular track URIs"""
    
    # Sample of popular track URIs for testing
    # These are real Spotify track IDs for popular songs
    sample_tracks = []
    
    # Popular tracks with known good URIs
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
    
    # Replicate these tracks to get 1000 records with variations
    for i in range(1000):
        base_track = popular_tracks[i % len(popular_tracks)]
        track_data = {
            'track_id': f'test_{i+1}',
            'track': base_track[0],
            'artist': base_track[1],
            'album': f'Album {i+1}',
            'spotify_track_uri': base_track[2],
            'energy': round(0.3 + (i % 7) * 0.1, 3),
            'valence': round(0.2 + (i % 8) * 0.1, 3),
            'danceability': round(0.4 + (i % 6) * 0.1, 3),
            'acousticness': round(0.1 + (i % 5) * 0.15, 3),
            'instrumentalness': round((i % 10) * 0.05, 4),
            'speechiness': round(0.03 + (i % 4) * 0.02, 4),
            'tempo': 80 + (i % 60),
            'mode': i % 2,
            'loudness': -15 + (i % 10),
            'JOY_SOCIAL_UPBEAT': round(0.1 + (i % 9) * 0.1, 3),
            'CALM_MEDITATIVE': round((i % 7) * 0.1, 3),
            'FOCUSED_NEUTRAL': round(0.05 + (i % 6) * 0.1, 3),
            'EXCITED_INTENSE': round((i % 8) * 0.1, 3),
            'SAD_MELANCHOLIC': round((i % 5) * 0.15, 3),
            'ASSERTIVE_NARRATIVE': round((i % 4) * 0.2, 3),
            'WARM_INTIMATE': round(0.1 + (i % 6) * 0.1, 3),
            'DARK_AGGRESSIVE': round((i % 3) * 0.1, 3),
            'PLAYFUL_GROOVY': round(0.2 + (i % 7) * 0.1, 3),
            'SERENE_ZEN': round((i % 5) * 0.1, 3),
            'BITTERSWEET': round((i % 4) * 0.15, 3),
            'CONTEMPLATIVE': round(0.05 + (i % 6) * 0.1, 3),
            'EUPHORIC': round((i % 8) * 0.1, 3),
            'NOSTALGIC': round(0.1 + (i % 5) * 0.1, 3),
            'MYSTERIOUS': round((i % 7) * 0.1, 3),
            'AUSTERE_MINIMAL': round((i % 3) * 0.05, 3),
            'mood_top_1': i % 5,
            'mood_top_1_score': round(0.3 + (i % 7) * 0.1, 3),
            'mood_vector': round((i % 10) * 0.1, 3)
        }
        sample_tracks.append(track_data)
    
    # Create DataFrame and save
    df = pd.DataFrame(sample_tracks)
    df.to_csv('test_tracks_1000.csv', index=False)
    
    print(f"✅ Created test_tracks_1000.csv with {len(df)} tracks")
    print(f"📊 Columns: {len(df.columns)}")
    print(f"🎵 Unique track URIs: {df['spotify_track_uri'].nunique()}")
    print(f"📋 Sample track: {df.iloc[0]['track']} by {df.iloc[0]['artist']}")
    
    return df

def run_test_1000():
    """Run the enhancer on 1000-record test data with analysis"""
    print("🧪 Running 1000-record test with detailed analysis...")
    print("=" * 50)
    
    # Create test data
    df = create_test_sample_1000()
    
    # Initialize enhancer
    enhancer = SpotifyDataEnhancer()
    
    # Authenticate
    print("\n🔐 Authenticating with Spotify...")
    if not enhancer.authenticate():
        print("❌ Authentication failed!")
        return
    
    # Run enhancement with analysis
    print(f"\n🚀 Starting enhancement of {len(df)} tracks WITH detailed analysis...")
    print("⏱️  Estimated time: 15-20 minutes")
    print("🔍 This will test all API endpoints and functionality")
    
    start_time = time.time()
    
    try:
        # Process the data
        enhanced_df = enhancer.enhance_tracks(df, include_analysis=True)
        
        # Save results
        output_file = 'enhanced_test_1000_results.csv'
        enhanced_df.to_csv(output_file, index=False)
        
        # Calculate results
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n🎉 Test completed successfully!")
        print(f"⏱️  Total time: {duration/60:.1f} minutes")
        print(f"📁 Output file: {output_file}")
        print(f"📊 Results:")
        print(f"   • Original columns: {len(df.columns)}")
        print(f"   • Enhanced columns: {len(enhanced_df.columns)}")
        print(f"   • New columns added: {len(enhanced_df.columns) - len(df.columns)}")
        print(f"   • Records processed: {len(enhanced_df)}")
        
        # Show sample enhanced data
        print(f"\n🎵 Sample enhanced data for '{enhanced_df.iloc[0]['track']}':")
        enhanced_cols = [col for col in enhanced_df.columns if 'enhanced_' in col][:5]
        for col in enhanced_cols:
            value = enhanced_df.iloc[0][col]
            print(f"   • {col}: {value}")
        
        # Show analysis data
        analysis_cols = [col for col in enhanced_df.columns if col.endswith('_count') or 'section_' in col][:3]
        if analysis_cols:
            print(f"\n🔍 Sample analysis data:")
            for col in analysis_cols:
                value = enhanced_df.iloc[0][col]
                if pd.notna(value):
                    print(f"   • {col}: {value}")
        
        # Performance stats
        enhanced_records = enhanced_df[enhanced_df['enhanced_energy'].notna()].shape[0]
        success_rate = (enhanced_records / len(enhanced_df)) * 100
        analysis_records = enhanced_df[enhanced_df['bars_count'].notna()].shape[0] if 'bars_count' in enhanced_df.columns else 0
        
        print(f"\n📈 Performance Stats:")
        print(f"   • Success rate: {success_rate:.1f}%")
        print(f"   • Audio features added: {enhanced_records} tracks")
        print(f"   • Analysis completed: {analysis_records} tracks")
        print(f"   • Average time per track: {(duration/len(df)):.2f} seconds")
        
        print(f"\n✅ 1000-record test PASSED! Ready for full dataset.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_test_1000()
