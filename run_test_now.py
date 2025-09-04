#!/usr/bin/env python3
"""
EXECUTE THE FAST TEST NOW - This will run immediately when executed
"""

import os
import sys
import subprocess
import time

def main():
    print("🚀 EXECUTING FAST TEST NOW...")
    print("=" * 50)
    
    # Change to the correct directory
    os.chdir('/workspaces/spotify-data-enhancer' if os.path.exists('/workspaces/spotify-data-enhancer') else '.')
    
    # Install dependencies
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests', 'pandas'], check=True)
    
    # Run the fast test
    print("⚡ Starting fast test execution...")
    result = subprocess.run([sys.executable, 'test_1000_fast.py'], 
                          capture_output=True, text=True)
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    print(f"Return code: {result.returncode}")
    
    # Check if output file was created
    if os.path.exists('enhanced_test_1000_features_only.csv'):
        file_size = os.path.getsize('enhanced_test_1000_features_only.csv')
        print(f"✅ Output file created: {file_size} bytes")
    else:
        print("❌ Output file not found")

if __name__ == '__main__':
    main()
