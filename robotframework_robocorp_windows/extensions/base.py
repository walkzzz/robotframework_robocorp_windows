# robotframework_robocorp_windows/extensions/base.py

"""
扩展插件基类，定义插件的接口规范
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class LocatorStrategy(ABC):
    """定位策略基类，用于扩展控件定位方式"""
    
    @abstractmethod
    def get_name(self) -> str:
        """获取定位策略名称
        
        Returns:
            str: 定位策略名称，如 "name", "id", "xpath" 等
        """
        pass
    
    @abstractmethod
    def find_control(self, window, locator: str, timeout: float = 10.0):
        """根据定位策略查找控件
        
        Args:
            window: 窗口元素
            locator: 控件定位符
            timeout: 超时时间（秒）
            
        Returns:
            ControlElement: 找到的控件元素
            
        Raises:
            ControlNotFoundError: 控件未找到时
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查该定位策略是否可用
        
        Returns:
            bool: 是否可用
        """
        pass


class KeywordExtension(ABC):
    """关键字扩展基类，用于扩展自定义关键字"""
    
    @abstractmethod
    def get_keywords(self) -> Dict[str, Any]:
        """获取扩展的关键字
        
        Returns:
            Dict[str, Any]: 关键字名称到关键字函数的映射
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取扩展名称
        
        Returns:
            str: 扩展名称
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查该扩展是否可用
        
        Returns:
            bool: 是否可用
        """
        pass


class ExtensionManager:
    """扩展管理器，用于注册和管理扩展插件"""
    
    def __init__(self):
        """初始化扩展管理器"""
        self.locator_strategies = {}  # 定位策略映射
        self.keyword_extensions = {}    # 关键字扩展映射
    
    def register_locator_strategy(self, strategy: LocatorStrategy):
        """注册定位策略
        
        Args:
            strategy: 定位策略实例
        """
        if strategy.is_available():
            self.locator_strategies[strategy.get_name()] = strategy
    
    def register_keyword_extension(self, extension: KeywordExtension):
        """注册关键字扩展
        
        Args:
            extension: 关键字扩展实例
        """
        if extension.is_available():
            self.keyword_extensions[extension.get_name()] = extension
    
    def get_locator_strategy(self, name: str):
        """获取定位策略
        
        Args:
            name: 定位策略名称
            
        Returns:
            LocatorStrategy or None: 定位策略实例，如果不存在则返回None
        """
        return self.locator_strategies.get(name)
    
    def get_all_locator_strategies(self) -> Dict[str, LocatorStrategy]:
        """获取所有定位策略
        
        Returns:
            Dict[str, LocatorStrategy]: 所有定位策略
        """
        return self.locator_strategies.copy()
    
    def get_all_keyword_extensions(self) -> Dict[str, KeywordExtension]:
        """获取所有关键字扩展
        
        Returns:
            Dict[str, KeywordExtension]: 所有关键字扩展
        """
        return self.keyword_extensions.copy()
    
    def get_all_keywords(self) -> Dict[str, Any]:
        """获取所有扩展关键字
        
        Returns:
            Dict[str, Any]: 所有扩展关键字
        """
        all_keywords = {}
        for extension in self.keyword_extensions.values():
            all_keywords.update(extension.get_keywords())
        return all_keywords


# 创建全局扩展管理器实例
extension_manager = ExtensionManager()


def get_extension_manager() -> ExtensionManager:
    """获取全局扩展管理器
    
    Returns:
        ExtensionManager: 全局扩展管理器实例
    """
    return extension_manager
