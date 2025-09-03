#!/usr/bin/env python3
"""
Test script to verify the enhancer works with a small sample
"""

import pandas as pd
from spotify_enhancer import SpotifyDataEnhancer

def create_test_data():
    """Create a small test CSV with some popular track URIs"""
    test_tracks = [
        {
            'track_id': 'test1',
            'track': 'Shape of You',
            'artist': 'Ed Sheeran',
            'spotify_track_uri': 'spotify:track:7qiZfU4dY1lWllzX7mPBI3'
        },
        {
            'track_id': 'test2', 
            'track': 'Blinding Lights',
            'artist': 'The Weeknd',
            'spotify_track_uri': 'spotify:track:0VjIjW4GlUZAMYd2vXMi3b'
        },
        {
            'track_id': 'test3',
            'track': 'Watermelon Sugar',
            'artist': 'Harry Styles', 
            'spotify_track_uri': 'spotify:track:6UelLqGlWMcVH1E5c4H7lY'
        }
    ]
    
    df = pd.DataFrame(test_tracks)
    df.to_csv('test_tracks.csv', index=False)
    print("✅ Created test_tracks.csv with 3 popular songs")
    return df

def run_test():
    """Run the enhancer on test data"""
    print("🧪 Running test with small dataset...")
    
    # Create test data
    create_test_data()
    
    # Run enhancer with analysis
    enhancer = SpotifyDataEnhancer()
    enhancer.process_file('test_tracks.csv', 'test_output.csv', include_analysis=True)
    
    # Show results
    result_df = pd.read_csv('test_output.csv')
    print(f"\n📊 Test Results:")
    print(f"   • Input columns: 4")
    print(f"   • Output columns: {len(result_df.columns)}")
    print(f"   • New columns added: {len(result_df.columns) - 4}")
    print(f"   • Tracks processed: {len(result_df)}")
    
    # Show some enhanced data
    enhanced_cols = [col for col in result_df.columns if 'enhanced_' in col]
    if enhanced_cols:
        print(f"\n🎵 Sample enhanced features for '{result_df.iloc[0]['track']}':")
        for col in enhanced_cols[:5]:  # Show first 5 enhanced features
            value = result_df.iloc[0][col]
            if pd.notna(value):
                print(f"   • {col}: {value}")
    
    # Show analysis data if available
    analysis_cols = [col for col in result_df.columns if col.endswith('_count') or 'section_' in col]
    if analysis_cols:
        print(f"\n🔍 Sample analysis data:")
        for col in analysis_cols[:3]:
            value = result_df.iloc[0][col]
            if pd.notna(value):
                print(f"   • {col}: {value}")

if __name__ == '__main__':
    run_test()