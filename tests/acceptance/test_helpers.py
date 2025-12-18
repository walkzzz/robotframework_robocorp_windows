# test_helpers.py
"""
验收测试辅助模块，用于处理环境检查和窗口模拟
"""

import os
import sys
import time
from typing import Optional


def check_environment():
    """检查测试环境，返回是否适合运行验收测试
    
    Returns:
        bool: True表示适合运行验收测试，False表示不适合
    """
    # 检查是否在CI环境中
    if os.environ.get('CI') or os.environ.get('CONTINUOUS_INTEGRATION'):
        # 在CI环境中，需要检查是否有桌面环境
        if sys.platform == 'win32':
            # Windows CI环境通常有桌面环境
            return True
        else:
            # 非Windows环境不支持Windows自动化
            return False
    
    # 本地环境，检查是否为Windows系统
    if sys.platform == 'win32':
        return True
    
    return False


def is_application_running(app_name: str) -> bool:
    """检查应用程序是否正在运行
    
    Args:
        app_name: 应用程序名称（如notepad.exe）
        
    Returns:
        bool: True表示应用程序正在运行，False表示没有运行
    """
    try:
        import psutil
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == app_name:
                return True
        return False
    except Exception:
        return False


def kill_application(app_name: str) -> bool:
    """终止应用程序进程
    
    Args:
        app_name: 应用程序名称（如notepad.exe）
        
    Returns:
        bool: True表示成功终止，False表示失败
    """
    try:
        import psutil
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == app_name:
                proc.kill()
                return True
        return False
    except Exception:
        return False


def wait_for_application(app_name: str, timeout: int = 10) -> bool:
    """等待应用程序启动
    
    Args:
        app_name: 应用程序名称（如notepad.exe）
        timeout: 超时时间（秒）
        
    Returns:
        bool: True表示应用程序成功启动，False表示超时
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_application_running(app_name):
            return True
        time.sleep(0.5)
    return False


def get_windows_version():
    """获取Windows版本信息
    
    Returns:
        str: Windows版本字符串
    """
    import platform
    return platform.version()
