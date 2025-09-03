#!/bin/bash

echo "🎵 Spotify Data Enhancer - Setup & Run Script"
echo "============================================="
echo ""

# Check if we're in a Codespace
if [ -n "$CODESPACES" ]; then
    echo "✅ Running in GitHub Codespace"
else
    echo "📍 Running locally"
fi

echo ""
echo "🔧 Installing dependencies..."
pip install -q requests pandas

echo ""
echo "📋 Setup checklist:"
echo "1. ✅ Repository created: Heneni/spotify-data-enhancer"
echo "2. ✅ Dependencies installed"
echo "3. 📤 Upload your tracks_for_import.csv file"
echo "4. 🚀 Ready to run enhancement"

echo ""
echo "📤 To upload your CSV file:"
echo "   - Drag and drop 'tracks_for_import.csv' into the file explorer"
echo "   - Or use: 'git add tracks_for_import.csv && git commit -m \"Add data\" && git push'"

echo ""
if [ -f "tracks_for_import.csv" ]; then
    echo "✅ Found tracks_for_import.csv"
    
    # Get file info
    LINES=$(wc -l < tracks_for_import.csv)
    SIZE=$(du -h tracks_for_import.csv | cut -f1)
    
    echo "📊 File info: $LINES lines, $SIZE"
    echo ""
    echo "🚀 Starting Spotify enhancement WITH detailed analysis..."
    echo "⏱️  Estimated time: 6-8 hours for 54K+ tracks"
    echo "🔍 This includes detailed audio analysis for ALL tracks"
    echo ""
    echo "Starting in 5 seconds... (Ctrl+C to cancel)"
    sleep 5
    
    # Run the enhancement with full analysis
    python spotify_enhancer.py --analysis
    
    echo ""
    echo "🎉 Enhancement complete!"
    if [ -f "enhanced_spotify_tracks.csv" ]; then
        OUTPUT_SIZE=$(du -h enhanced_spotify_tracks.csv | cut -f1)
        OUTPUT_LINES=$(wc -l < enhanced_spotify_tracks.csv)
        echo "📁 Output file: enhanced_spotify_tracks.csv ($OUTPUT_SIZE, $OUTPUT_LINES lines)"
        echo "📊 Download your enhanced data from the file explorer"
    fi
    
else
    echo "❌ tracks_for_import.csv not found"
    echo ""
    echo "📝 Please upload your CSV file with these steps:"
    echo "   1. In the file explorer (left panel), click 'Upload Files'"
    echo "   2. Select your tracks_for_import.csv file"
    echo "   3. Run this script again: ./setup_and_run.sh"
    echo ""
    echo "🧪 Or test with sample data: python test_small.py"
fi

echo ""
echo "🔗 Repository: https://github.com/Heneni/spotify-data-enhancer"
echo "📚 Documentation: See README.md for details"
