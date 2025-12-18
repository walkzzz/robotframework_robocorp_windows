#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：模拟Robot Framework RIDE的库导入方式
"""

import sys
import os

print("=== RobotFramework RIDE 导入测试 ===")

# 测试1：模拟RIDE的导入方式
def test_ride_import():
    """模拟RIDE的库导入方式"""
    print("\n1. 模拟RIDE的库导入方式：")
    try:
        # RIDE通常使用这种方式导入库
        from robotframework_robocorp_windows import RobocorpWindows
        # 创建实例
        lib = RobocorpWindows()
        print("✅ 成功创建库实例")
        
        # 检查库的基本属性
        if hasattr(lib, 'ROBOT_LIBRARY_VERSION'):
            print(f"✅ 库版本：{lib.ROBOT_LIBRARY_VERSION}")
        if hasattr(lib, 'ROBOT_LIBRARY_SCOPE'):
            print(f"✅ 库作用域：{lib.ROBOT_LIBRARY_SCOPE}")
        
        return True
    except Exception as e:
        print(f"❌ 导入失败：{e}")
        return False

# 测试2：检查关键字列表
def test_keywords_list():
    """检查关键字列表"""
    print("\n2. 检查关键字列表：")
    try:
        from robotframework_robocorp_windows import keywords as exported_keywords
        print(f"✅ 从模块导出的关键字数量：{len(exported_keywords)}")
        print(f"✅ 关键字列表：{exported_keywords}")
        
        # 检查核心关键字是否存在
        core_keywords = ['launch_application', 'click_control', 'type_into_control', 'async_type_into_control']
        for kw in core_keywords:
            if kw in exported_keywords:
                print(f"✅ 核心关键字 {kw} 已导出")
            else:
                print(f"⚠️  核心关键字 {kw} 未导出")
        
        return True
    except Exception as e:
        print(f"❌ 检查关键字列表失败：{e}")
        return False

# 测试3：检查ROBOT_LIBRARY_CLASS
def test_robot_library_class():
    """检查ROBOT_LIBRARY_CLASS是否正确设置"""
    print("\n3. 检查ROBOT_LIBRARY_CLASS：")
    try:
        import robotframework_robocorp_windows
        if hasattr(robotframework_robocorp_windows, 'ROBOT_LIBRARY_CLASS'):
            print(f"✅ ROBOT_LIBRARY_CLASS 已设置：{robotframework_robocorp_windows.ROBOT_LIBRARY_CLASS}")
            # 尝试使用ROBOT_LIBRARY_CLASS创建实例
            lib_class = robotframework_robocorp_windows.ROBOT_LIBRARY_CLASS
            lib = lib_class()
            print(f"✅ 成功使用 ROBOT_LIBRARY_CLASS 创建实例")
            return True
        else:
            print("❌ ROBOT_LIBRARY_CLASS 未设置")
            return False
    except Exception as e:
        print(f"❌ 检查 ROBOT_LIBRARY_CLASS 失败：{e}")
        return False

# 测试4：检查__all__变量
def test_all_variable():
    """检查__all__变量是否正确设置"""
    print("\n4. 检查__all__变量：")
    try:
        import robotframework_robocorp_windows
        if hasattr(robotframework_robocorp_windows, '__all__'):
            print(f"✅ __all__ 变量已设置，包含 {len(robotframework_robocorp_windows.__all__)} 个元素")
            print(f"✅ __all__ 内容：{robotframework_robocorp_windows.__all__}")
            return True
        else:
            print("❌ __all__ 变量未设置")
            return False
    except Exception as e:
        print(f"❌ 检查 __all__ 变量失败：{e}")
        return False

# 测试5：模拟RIDE的关键字发现
def test_keyword_discovery():
    """模拟RIDE的关键字发现机制"""
    print("\n5. 模拟RIDE的关键字发现：")
    try:
        from robotframework_robocorp_windows import RobocorpWindows
        lib = RobocorpWindows()
        
        # 获取所有属性，模拟RIDE的关键字发现
        attrs = dir(lib)
        # 过滤掉私有属性和内置方法
        keywords = [attr for attr in attrs if not attr.startswith('_') and callable(getattr(lib, attr))]
        
        print(f"✅ 发现关键字数量：{len(keywords)}")
        # 打印前10个关键字作为示例
        print(f"✅ 关键字示例：{keywords[:10]}...")
        
        # 检查核心关键字
        core_keywords = ['launch_application', 'click_control', 'type_into_control', 'async_type_into_control', 'wait_for_async_task']
        found = 0
        for kw in core_keywords:
            if kw in keywords:
                found += 1
        print(f"✅ 核心关键字发现率：{found}/{len(core_keywords)}")
        
        return True
    except Exception as e:
        print(f"❌ 关键字发现失败：{e}")
        return False

# 运行所有测试
def run_all_tests():
    """运行所有测试"""
    tests = [
        test_ride_import,
        test_keywords_list,
        test_robot_library_class,
        test_all_variable,
        test_keyword_discovery
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== 测试结果 ===")
    print(f"通过测试：{passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！库可以被Robot Framework RIDE正确识别和导入。")
        return True
    else:
        print(f"⚠️  有 {total - passed} 个测试失败，请检查库的配置。")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
