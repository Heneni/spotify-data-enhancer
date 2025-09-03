#!/bin/bash
echo "🎵 Spotify Data Enhancer - Quick Start"
echo "====================================="

# Check if tracks file exists
if [ ! -f "tracks_for_import.csv" ]; then
    echo "❌ tracks_for_import.csv not found!"
    echo "📄 Please upload your CSV file to this workspace"
    echo ""
    echo "💡 Want to test first? Run: python test_small.py"
    exit 1
fi

echo "📁 Found tracks_for_import.csv"
echo "🔍 Starting enhancement WITH detailed analysis..."
echo "⏱️  This will take several hours for large datasets"
echo ""

# Run the enhancer with analysis
python spotify_enhancer.py --analysis

echo ""
echo "🎉 Done! Check enhanced_spotify_tracks.csv for results"