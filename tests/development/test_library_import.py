#!/usr/bin/env python3
"""
Test script to verify that the library can be imported correctly.
"""

import sys
import os

# Add the current directory to the path so we can import the library
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from robotframework_robocorp_windows import RobocorpWindows
    print("✅ Successfully imported RobocorpWindows class")
    
    # Create an instance of the library
    library = RobocorpWindows()
    print("✅ Successfully created RobocorpWindows instance")
    
    # Check if keywords are available
    print("\n📋 Available keywords:")
    for attr_name in dir(library):
        if not attr_name.startswith('_'):
            attr = getattr(library, attr_name)
            if callable(attr):
                print(f"  - {attr_name}")
    
    print("\n✅ Test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)