#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证库的基本功能和导入
"""

import sys
import os

print("=== RobotFramework Robocorp Windows Library 导入测试 ===")

# 测试1：基本导入
print("\n1. 测试基本导入：")
try:
    from robotframework_robocorp_windows import RobocorpWindows
    print("✅ 成功导入 RobocorpWindows 类")
except Exception as e:
    print(f"❌ 导入失败：{e}")
    sys.exit(1)

# 测试2：创建实例
print("\n2. 测试创建实例：")
try:
    lib = RobocorpWindows()
    print("✅ 成功创建 RobocorpWindows 实例")
except Exception as e:
    print(f"❌ 创建实例失败：{e}")
    sys.exit(1)

# 测试3：检查关键字是否可用
print("\n3. 测试关键字可用性：")
keywords_to_check = [
    # 窗口管理关键字
    'launch_application', 'connect_to_application', 'set_current_window',
    'close_application', 'minimize_window', 'maximize_window', 'restore_window',
    'window_should_be_open', 'window_should_be_closed', 'get_window_title',
    # 控件操作关键字
    'find_control', 'click_control', 'double_click_control', 'right_click_control',
    'type_into_control', 'get_control_text', 'control_should_exist',
    'control_should_not_exist', 'set_control_value', 'get_control_value',
    'select_from_combobox', 'check_checkbox', 'uncheck_checkbox',
    'checkbox_should_be_checked', 'checkbox_should_be_unchecked',
    # 异步操作关键字
    'async_type_into_control', 'async_find_all_controls', 'async_click_control',
    'wait_for_async_task', 'shutdown_async_executor'
]

all_keywords_found = True
for keyword in keywords_to_check:
    if hasattr(lib, keyword):
        print(f"✅ 关键字 {keyword} 可用")
    else:
        print(f"❌ 关键字 {keyword} 不可用")
        all_keywords_found = False

if not all_keywords_found:
    print("\n⚠️  部分关键字不可用")
else:
    print("\n✅ 所有测试关键字均可用")

# 测试4：检查entry_points配置
print("\n4. 测试entry_points配置：")
try:
    import pkg_resources
    entry_points = pkg_resources.iter_entry_points('robotframework.libraries')
    robocorp_entry_point = None
    for ep in entry_points:
        if ep.name == 'RobocorpWindows':
            robocorp_entry_point = ep
            break
    
    if robocorp_entry_point:
        print(f"✅ 找到 entry_point：{robocorp_entry_point.name}")
        print(f"   入口：{robocorp_entry_point.module_name}:{robocorp_entry_point.attrs[0]}")
        # 测试加载entry_point
        try:
            lib_from_entry_point = robocorp_entry_point.load()
            print("✅ 成功从 entry_point 加载库类")
            if hasattr(lib_from_entry_point, '__name__'):
                print(f"   库类名：{lib_from_entry_point.__name__}")
        except Exception as e:
            print(f"❌ 从 entry_point 加载库类失败：{e}")
    else:
        print("❌ 未找到 RobocorpWindows entry_point")
except Exception as e:
    print(f"❌ 检查 entry_points 失败：{e}")

# 测试5：检查版本信息
print("\n5. 测试版本信息：")
try:
    import robotframework_robocorp_windows
    if hasattr(robotframework_robocorp_windows, '__version__'):
        print(f"✅ 版本信息：{robotframework_robocorp_windows.__version__}")
    else:
        print("❌ 未找到版本信息")
except Exception as e:
    print(f"❌ 检查版本信息失败：{e}")

# 测试6：检查ROBOT_LIBRARY_CLASS
print("\n6. 测试ROBOT_LIBRARY_CLASS：")
try:
    import robotframework_robocorp_windows
    if hasattr(robotframework_robocorp_windows, 'ROBOT_LIBRARY_CLASS'):
        print(f"✅ ROBOT_LIBRARY_CLASS：{robotframework_robocorp_windows.ROBOT_LIBRARY_CLASS}")
    else:
        print("❌ 未找到 ROBOT_LIBRARY_CLASS")
except Exception as e:
    print(f"❌ 检查 ROBOT_LIBRARY_CLASS 失败：{e}")

print("\n=== 测试完成 ===")
