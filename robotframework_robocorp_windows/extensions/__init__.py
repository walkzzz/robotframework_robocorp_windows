# robotframework_robocorp_windows/extensions/__init__.py

"""
扩展插件模块，支持用户自定义关键字和定位策略
"""

from .base import (
    LocatorStrategy,
    KeywordExtension,
    ExtensionManager,
    extension_manager,
    get_extension_manager
)

__all__ = [
    'LocatorStrategy',
    'KeywordExtension',
    'ExtensionManager',
    'extension_manager',
    'get_extension_manager'
]