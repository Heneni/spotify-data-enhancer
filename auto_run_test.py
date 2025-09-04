#!/usr/bin/env python3
"""
AUTO-RUN: Execute the fast test automatically
This script runs the 1000-record test and reports results
"""

import sys
import time
import traceback
from datetime import datetime

# Import our test modules
from test_1000_fast import run_fast_test_1000

def main():
    """Main execution with monitoring"""
    print("🤖 AUTO-RUNNER: Starting Fast 1000-Record Test")
    print("=" * 55)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("⚡ Running features-only test for speed")
    print("🎯 Target: 5-8 minutes processing time")
    print()
    
    start_time = time.time()
    
    try:
        # Run the fast test
        print("🚀 Executing test_1000_fast.run_fast_test_1000()...")
        run_fast_test_1000()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n🎉 AUTO-RUNNER: Test completed successfully!")
        print(f"⏱️  Total execution time: {duration/60:.1f} minutes")
        print(f"📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✅ Status: PASSED")
        
        return 0
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n❌ AUTO-RUNNER: Test failed!")
        print(f"⏱️  Failed after: {duration/60:.1f} minutes")
        print(f"🐛 Error: {str(e)}")
        print(f"📅 Failed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n📋 Full traceback:")
        traceback.print_exc()
        print(f"❌ Status: FAILED")
        
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
