#!/usr/bin/env python3
"""
Monitor and run the fast 1000-record test
This script will run the test and provide detailed monitoring
"""

import subprocess
import time
import sys
import os

def run_monitored_test():
    """Run the fast test with monitoring"""
    print("🎯 MONITORING: Starting Fast 1000-Record Test")
    print("=" * 50)
    print("⚡ Features only - Expected time: 5-8 minutes")
    print("📊 Monitoring for issues and progress...")
    print("")
    
    try:
        # Start the test process
        print("🚀 Launching test_1000_fast.py...")
        
        # Run the test script
        process = subprocess.Popen(
            [sys.executable, 'test_1000_fast.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        start_time = time.time()
        
        # Monitor the process
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                elapsed = time.time() - start_time
                print(f"[{elapsed:.1f}s] {output.strip()}")
        
        # Get any remaining output
        stdout, stderr = process.communicate()
        if stdout:
            print(stdout)
        if stderr:
            print("STDERR:", stderr)
        
        # Check result
        if process.returncode == 0:
            elapsed = time.time() - start_time
            print(f"\n✅ TEST COMPLETED SUCCESSFULLY!")
            print(f"⏱️  Total time: {elapsed/60:.1f} minutes")
            
            # Check if output file was created
            if os.path.exists('enhanced_test_1000_features_only.csv'):
                file_size = os.path.getsize('enhanced_test_1000_features_only.csv')
                print(f"📁 Output file created: enhanced_test_1000_features_only.csv")
                print(f"📊 File size: {file_size/1024:.1f} KB")
                
                # Quick analysis of results
                import pandas as pd
                df = pd.read_csv('enhanced_test_1000_features_only.csv')
                enhanced_cols = [col for col in df.columns if 'enhanced_' in col]
                
                print(f"📈 Results summary:")
                print(f"   • Total rows: {len(df)}")
                print(f"   • Total columns: {len(df.columns)}")
                print(f"   • Enhanced columns: {len(enhanced_cols)}")
                print(f"   • Success rate: {(df['enhanced_energy'].count() / len(df) * 100):.1f}%")
                
            print(f"\n🎉 MONITORING COMPLETE - TEST PASSED!")
        else:
            print(f"\n❌ TEST FAILED with return code: {process.returncode}")
            
    except Exception as e:
        print(f"❌ MONITORING ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_monitored_test()
