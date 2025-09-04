#!/bin/bash

echo "🚀 Spotify Data Enhancer - Quick Setup & Run"
echo "============================================"
echo ""

# Skip devcontainer - run directly in GitHub Codespace
echo "⚡ Quick setup (skipping devcontainer for speed)..."

# Install dependencies directly
echo "📦 Installing Python dependencies..."
pip install requests pandas --quiet

echo ""
echo "🧪 Running FAST 1000-record test..."
echo "⏱️  Expected time: 5-8 minutes"
echo "📊 Features only (no detailed analysis)"
echo ""

# Run the test directly
python test_1000_fast.py

echo ""
echo "✅ Test execution complete!"
echo "📁 Check for output file: enhanced_test_1000_features_only.csv"
echo "🔗 Repository: https://github.com/Heneni/spotify-data-enhancer"
