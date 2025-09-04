#!/usr/bin/env python3
"""
Sample usage demonstration for Spotify Data Enhancer
Creates sample data and shows how to use the enhancer
"""

import json
import csv
import os
from spotify_enhancer import SpotifyDataEnhancer

def create_sample_data():
    """Create sample Spotify data for testing"""
    
    # Sample track IDs (these are real Spotify track IDs)
    sample_tracks = [
        {
            "id": "7qiZfU4dY1lWllzX7mPBI3",
            "track_name": "Shape of You",
            "artist_name": "Ed Sheeran",
            "played_at": "2023-01-01T10:00:00Z"
        },
        {
            "id": "0VjIjW4GlUZAMYd2vXMi3b", 
            "track_name": "Blinding Lights",
            "artist_name": "The Weeknd",
            "played_at": "2023-01-01T11:00:00Z"
        },
        {
            "id": "6UelLqGlWMcVH1E5c4H7lY",
            "track_name": "Watermelon Sugar",
            "artist_name": "Harry Styles", 
            "played_at": "2023-01-01T12:00:00Z"
        },
        {
            "id": "11dFghVXANMlKmJXsNCbNl",
            "track_name": "Cruel Summer",
            "artist_name": "Taylor Swift",
            "played_at": "2023-01-01T13:00:00Z"
        },
        {
            "id": "1BxfuPKGuaTgP7aM0Bbdwr",
            "track_name": "Levitating",
            "artist_name": "Dua Lipa",
            "played_at": "2023-01-01T14:00:00Z"
        }
    ]
    
    # Create CSV sample
    with open('sample_tracks.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'track_name', 'artist_name', 'played_at'])
        writer.writeheader()
        writer.writerows(sample_tracks)
    
    # Create JSON sample  
    with open('sample_tracks.json', 'w') as f:
        json.dump(sample_tracks, f, indent=2)
    
    print("✅ Created sample data files:")
    print("   📄 sample_tracks.csv")
    print("   📄 sample_tracks.json")

def run_enhancement_demo():
    """Demonstrate the enhancement process"""
    
    print("🎵 Spotify Data Enhancer Demo")
    print("=" * 40)
    
    # Create sample data if it doesn't exist
    if not os.path.exists('sample_tracks.csv'):
        print("📊 Creating sample data...")
        create_sample_data()
        print()
    
    # Initialize enhancer
    enhancer = SpotifyDataEnhancer()
    
    # Test authentication
    print("🔐 Testing authentication...")
    if not enhancer.authenticate():
        print("❌ Authentication failed!")
        return False
    
    print("✅ Authentication successful!")
    print()
    
    # Process the sample data
    print("🚀 Processing sample tracks...")
    try:
        stats = enhancer.process_dataset(
            'sample_tracks.csv',
            'sample_tracks_enhanced.csv',
            resume=False
        )
        
        print("\n📊 Processing Statistics:")
        print(f"   Total tracks: {stats['total']}")
        print(f"   Successfully enhanced: {stats['success']}")
        print(f"   Failed: {stats['failed']}")
        print(f"   Success rate: {stats['enhancement_rate']:.1f}%")
        
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        return False
    
    # Validate results
    print("\n🔍 Validating results...")
    validation = enhancer.validate_enhancement('sample_tracks_enhanced.csv')
    
    if "error" not in validation:
        print("✅ Validation successful!")
        print(f"   Enhanced rows: {validation['enhanced_rows']}")
        print(f"   Enhancement rate: {validation['enhancement_rate']:.1f}%")
        print(f"   Audio features: {len(validation['audio_features_columns'])}")
        
        # Show sample of enhanced data
        print("\n📋 Sample Enhanced Data:")
        try:
            import pandas as pd
            df = pd.read_csv('sample_tracks_enhanced.csv')
            
            # Show first row with audio features
            audio_cols = ['danceability', 'energy', 'valence', 'tempo']
            available_cols = [col for col in audio_cols if col in df.columns]
            
            if available_cols:
                sample_row = df.iloc[0]
                print(f"   Track: {sample_row.get('track_name', 'N/A')} - {sample_row.get('artist_name', 'N/A')}")
                for col in available_cols:
                    value = sample_row.get(col, 'N/A')
                    if col == 'tempo':
                        print(f"   {col.capitalize()}: {value:.0f} BPM")
                    else:
                        print(f"   {col.capitalize()}: {value:.3f}")
            
        except ImportError:
            print("   (Install pandas to see detailed sample data)")
        except Exception as e:
            print(f"   Error showing sample: {str(e)}")
    
    else:
        print(f"❌ Validation failed: {validation['error']}")
        return False
    
    print("\n🎉 Demo completed successfully!")
    print(f"📁 Check 'sample_tracks_enhanced.csv' for full results")
    
    return True

def cleanup_demo_files():
    """Clean up demo files"""
    files_to_remove = [
        'sample_tracks.csv',
        'sample_tracks.json', 
        'sample_tracks_enhanced.csv',
        'spotify_enhancement.log'
    ]
    
    removed = []
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            removed.append(file)
    
    if removed:
        print(f"🧹 Cleaned up demo files: {', '.join(removed)}")
    else:
        print("🧹 No demo files to clean up")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Spotify Data Enhancer Demo')
    parser.add_argument('--cleanup', action='store_true', help='Clean up demo files and exit')
    parser.add_argument('--create-sample', action='store_true', help='Just create sample data and exit')
    
    args = parser.parse_args()
    
    if args.cleanup:
        cleanup_demo_files()
    elif args.create_sample:
        create_sample_data()
    else:
        success = run_enhancement_demo()
        if not success:
            exit(1)
