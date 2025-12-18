#!/usr/bin/env python3
"""
Test script to verify exception handling in RobocorpWindows library.
"""

from robotframework_robocorp_windows import RobocorpWindows

def test_exception_scenarios():
    """Test various exception scenarios."""
    print("🧪 Testing Exception Scenarios...")
    
    # Create library instance
    lib = RobocorpWindows()
    
    # Test 1: Invalid application path
    print("\n1️⃣ Testing invalid application path...")
    try:
        result = lib.launch_application("invalid/path/to/app.exe")
        print(f"   ❌ Expected exception but got: {result}")
    except Exception as e:
        print(f"   ✅ Correctly raised exception: {type(e).__name__}")
    
    # Test 2: Invalid window title
    print("\n2️⃣ Testing invalid window title...")
    try:
        result = lib.set_current_window("This Window Does Not Exist")
        print(f"   ❌ Expected exception but got: {result}")
    except Exception as e:
        print(f"   ✅ Correctly raised exception: {type(e).__name__}")
    
    # Test 3: Invalid control locator
    print("\n3️⃣ Testing invalid control locator...")
    try:
        result = lib.click_control("invalid_locator_without_strategy")
        print(f"   ❌ Expected exception but got: {result}")
    except Exception as e:
        print(f"   ✅ Correctly raised exception: {type(e).__name__}")
    
    # Test 4: Control operations without current window
    print("\n4️⃣ Testing control operations without current window...")
    try:
        result = lib.find_control("name:InvalidControl")
        print(f"   ❌ Expected exception but got: {result}")
    except Exception as e:
        print(f"   ✅ Correctly raised exception: {type(e).__name__}")
    
    # Test 5: Wait until with invalid condition
    print("\n5️⃣ Testing wait until with invalid condition...")
    try:
        result = lib.wait_until_condition("invalid_python_expression")
        print(f"   ❌ Expected exception but got: {result}")
    except Exception as e:
        print(f"   ✅ Correctly raised exception: {type(e).__name__}")
    
    # Test 6: Check checkbox that doesn't exist
    print("\n6️⃣ Testing checkbox operations on non-existent control...")
    try:
        result = lib.check_checkbox("name:NonExistentCheckbox")
        print(f"   ❌ Expected exception but got: {result}")
    except Exception as e:
        print(f"   ✅ Correctly raised exception: {type(e).__name__}")
    
    # Test 7: Close application without current app
    print("\n7️⃣ Testing close application without current app...")
    try:
        result = lib.close_application()
        print(f"   ❌ Expected exception but got: {result}")
    except Exception as e:
        print(f"   ✅ Correctly raised exception: {type(e).__name__}")
    
    # Test 8: Get window title without current window
    print("\n8️⃣ Testing get window title without current window...")
    try:
        result = lib.get_window_title()
        print(f"   ❌ Expected exception but got: {result}")
    except Exception as e:
        print(f"   ✅ Correctly raised exception: {type(e).__name__}")
    
    # Test 9: Select from combobox that doesn't exist
    print("\n9️⃣ Testing combobox operations on non-existent control...")
    try:
        result = lib.select_from_combobox("name:NonExistentCombobox", "Option1")
        print(f"   ❌ Expected exception but got: {result}")
    except Exception as e:
        print(f"   ✅ Correctly raised exception: {type(e).__name__}")
    
    print("\n🎉 Exception scenarios testing completed!")
    return True

if __name__ == "__main__":
    test_exception_scenarios()
