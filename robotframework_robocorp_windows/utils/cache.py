# robotframework_robocorp_windows/utils/cache.py

"""
缓存工具类，用于缓存控件查找结果，提高性能
"""

import time
from collections import OrderedDict


class ControlCache:
    """控件缓存类，用于缓存控件查找结果
    
    缓存策略：
    - 基于「窗口句柄+控件定位符」作为key
    - 设置过期时间（默认与timeout一致）
    - 当窗口状态变化时，自动清空关联缓存
    """
    
    def __init__(self, default_expire_time=10):
        """初始化缓存
        
        Args:
            default_expire_time: 默认过期时间（秒）
        """
        self.cache = OrderedDict()
        self.default_expire_time = default_expire_time
    
    def _get_key(self, window, control_identifier):
        """生成缓存键
        
        Args:
            window: 窗口元素
            control_identifier: 控件标识符
            
        Returns:
            str: 缓存键
        """
        window_handle = getattr(window, 'handle', id(window))
        return f"{window_handle}_{control_identifier}"
    
    def get(self, window, control_identifier):
        """从缓存中获取控件
        
        Args:
            window: 窗口元素
            control_identifier: 控件标识符
            
        Returns:
            tuple: (control, is_cached) - 控件元素和是否来自缓存的标志
        """
        key = self._get_key(window, control_identifier)
        if key in self.cache:
            control, expire_time = self.cache[key]
            if time.time() < expire_time:
                # 缓存未过期，返回控件
                return control, True
            else:
                # 缓存已过期，移除并返回None
                del self.cache[key]
        return None, False
    
    def set(self, window, control_identifier, control, expire_time=None):
        """将控件存入缓存
        
        Args:
            window: 窗口元素
            control_identifier: 控件标识符
            control: 控件元素
            expire_time: 过期时间（秒），如果为None则使用默认值
        """
        key = self._get_key(window, control_identifier)
        expire_time = time.time() + (expire_time or self.default_expire_time)
        self.cache[key] = (control, expire_time)
        
        # 限制缓存大小，防止内存溢出
        if len(self.cache) > 100:
            # 删除最旧的缓存项
            self.cache.popitem(last=False)
    
    def clear(self, window=None):
        """清空缓存
        
        Args:
            window: 窗口元素，如果提供则只清空该窗口的缓存
        """
        if window:
            # 只清空指定窗口的缓存
            window_handle = getattr(window, 'handle', id(window))
            keys_to_remove = [key for key in self.cache if key.startswith(f"{window_handle}_")]
            for key in keys_to_remove:
                del self.cache[key]
        else:
            # 清空所有缓存
            self.cache.clear()
    
    def clear_all(self):
        """清空所有缓存
        """
        self.clear()
    
    def size(self):
        """获取缓存大小
        
        Returns:
            int: 缓存中的控件数量
        """
        return len(self.cache)
    
    def __len__(self):
        """获取缓存大小
        
        Returns:
            int: 缓存中的控件数量
        """
        return self.size()
