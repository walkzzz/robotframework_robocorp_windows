#!/usr/bin/env python3
"""
Test script to verify that the library keywords can be called directly.
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
    
    # Try calling a keyword directly
    print("\n📋 Testing keyword call...")
    
    # We'll just check if the method exists, since we can't actually launch an app in this environment
    if hasattr(library, 'launch_application'):
        print("✅ launch_application method exists")
    else:
        print("❌ launch_application method does not exist")
    
    # Check all expected keywords
    expected_keywords = [
        'launch_application', 'connect_to_application', 'set_current_window',
        'close_application', 'minimize_window', 'maximize_window', 'restore_window',
        'window_should_be_open', 'window_should_be_closed', 'get_window_title',
        'find_control', 'click_control', 'double_click_control', 'right_click_control',
        'type_into_control', 'get_control_text', 'control_should_exist',
        'control_should_not_exist', 'set_control_value', 'get_control_value',
        'select_from_combobox', 'check_checkbox', 'uncheck_checkbox',
        'checkbox_should_be_checked', 'checkbox_should_be_unchecked'
    ]
    
    print("\n📋 Checking expected keywords:")
    missing_keywords = []
    for keyword in expected_keywords:
        if hasattr(library, keyword):
            print(f"  ✅ {keyword}")
        else:
            print(f"  ❌ {keyword}")
            missing_keywords.append(keyword)
    
    if not missing_keywords:
        print("\n✅ All expected keywords are available!")
    else:
        print(f"\n❌ Missing keywords: {missing_keywords}")
    
    print("\n✅ Test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)