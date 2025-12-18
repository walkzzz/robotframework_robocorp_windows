# robotframework_robocorp_windows/drivers/version_adapter.py

"""
版本适配抽象层，根据底层库版本动态选择实现
"""

import sys
import pkg_resources
from typing import Optional


class PyWin32Adapter:
    """pywin32版本适配基类"""
    
    def __init__(self, version):
        """初始化适配器
        
        Args:
            version: pywin32版本号
        """
        self.version = version
    
    def get_version(self):
        """获取当前pywin32版本
        
        Returns:
            tuple: 版本号元组 (major, minor, patch)
        """
        return self.version
    
    def is_compatible(self):
        """检查版本是否兼容
        
        Returns:
            bool: 是否兼容
        """
        # 默认兼容
        return True


class PyWin32V300Adapter(PyWin32Adapter):
    """pywin32 300-303版本适配器"""
    
    def __init__(self, version):
        super().__init__(version)
    
    def is_compatible(self):
        """检查版本是否兼容
        
        Returns:
            bool: 是否兼容
        """
        major, minor, _ = self.version
        return 300 <= major < 304


class PyWin32V304Adapter(PyWin32Adapter):
    """pywin32 304+版本适配器"""
    
    def __init__(self, version):
        super().__init__(version)
    
    def is_compatible(self):
        """检查版本是否兼容
        
        Returns:
            bool: 是否兼容
        """
        major, _, _ = self.version
        return major >= 304


class VersionAdapterFactory:
    """版本适配器工厂，根据版本号创建相应的适配器"""
    
    @staticmethod
    def get_pywin32_version():
        """获取当前pywin32版本
        
        Returns:
            tuple: 版本号元组 (major, minor, patch)
        """
        try:
            pywin32_version = pkg_resources.get_distribution("pywin32").version
            # 解析版本号，处理类似 "311.2" 的情况
            parts = pywin32_version.split(".")
            major = int(parts[0])
            minor = int(parts[1]) if len(parts) > 1 else 0
            patch = int(parts[2]) if len(parts) > 2 else 0
            return (major, minor, patch)
        except (pkg_resources.DistributionNotFound, ValueError):
            # 如果无法获取版本，返回默认值
            return (0, 0, 0)
    
    @staticmethod
    def create_pywin32_adapter():
        """创建pywin32适配器
        
        Returns:
            PyWin32Adapter: 适合当前版本的pywin32适配器
        """
        version = VersionAdapterFactory.get_pywin32_version()
        if version[0] >= 304:
            return PyWin32V304Adapter(version)
        elif 300 <= version[0] < 304:
            return PyWin32V300Adapter(version)
        else:
            # 默认使用304+适配器，因为300-303版本已不再维护
            return PyWin32V304Adapter(version)
    
    @staticmethod
    def create_robocorp_windows_adapter():
        """创建robocorp-windows适配器
        
        Returns:
            Optional[object]: robocorp-windows适配器，如果未安装则返回None
        """
        try:
            from robocorp.windows import __version__ as rc_windows_version
            # 这里可以根据robocorp-windows版本创建不同的适配器
            # 目前我们只需返回版本号
            return rc_windows_version
        except ImportError:
            return None


# 创建全局适配器实例
pywin32_adapter = VersionAdapterFactory.create_pywin32_adapter()
robocorp_windows_version = VersionAdapterFactory.create_robocorp_windows_adapter()


def get_pywin32_adapter():
    """获取pywin32适配器
    
    Returns:
        PyWin32Adapter: pywin32适配器
    """
    return pywin32_adapter


def get_robocorp_windows_version():
    """获取robocorp-windows版本
    
    Returns:
        Optional[str]: robocorp-windows版本号
    """
    return robocorp_windows_version
