# robotframework_robocorp_windows/utils/config.py

"""
配置管理模块，支持通过Library导入参数、环境变量、配置文件多级覆盖
"""

import os
from typing import Dict, Any


class Configuration:
    """配置管理类，实现分层配置管理"""
    
    def __init__(self, default_config: Dict[str, Any] = None):
        """初始化配置
        
        Args:
            default_config: 默认配置
        """
        self._default_config = default_config or {}
        self._config = self._default_config.copy()
        self._env_prefix = "ROBOCORP_WINDOWS_"
    
    def update_from_dict(self, config_dict: Dict[str, Any]):
        """从字典更新配置
        
        Args:
            config_dict: 配置字典
        """
        self._config.update(config_dict)
    
    def update_from_env(self):
        """从环境变量更新配置
        
        环境变量命名规则：ROBOCORP_WINDOWS_<CONFIG_KEY>
        例如：ROBOCORP_WINDOWS_TIMEOUT=30
        """
        for key, value in os.environ.items():
            if key.startswith(self._env_prefix):
                config_key = key[len(self._env_prefix):].lower()
                # 尝试转换为相应类型
                if value.lower() in ('true', 'false'):
                    # 布尔值
                    self._config[config_key] = value.lower() == 'true'
                elif value.isdigit():
                    # 整数
                    self._config[config_key] = int(value)
                elif '.' in value and all(part.isdigit() for part in value.split('.')):
                    # 浮点数
                    self._config[config_key] = float(value)
                else:
                    # 字符串
                    self._config[config_key] = value
    
    def update_from_file(self, config_file: str):
        """从配置文件更新配置
        
        Args:
            config_file: 配置文件路径，支持YAML格式
        """
        if os.path.exists(config_file):
            try:
                import yaml
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                    if config_data:
                        self._config.update(config_data)
            except ImportError:
                # 如果没有安装yaml，忽略文件
                pass
            except Exception as e:
                # 配置文件解析错误，忽略
                pass
    
    def get(self, key: str, default: Any = None):
        """获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            Any: 配置值
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置值
        
        Args:
            key: 配置键
            value: 配置值
        """
        self._config[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """获取配置字典
        
        Returns:
            Dict[str, Any]: 配置字典
        """
        return self._config.copy()


# 默认配置
def get_default_config() -> Dict[str, Any]:
    """获取默认配置
    
    Returns:
        Dict[str, Any]: 默认配置
    """
    return {
        'timeout': 10.0,
        'retry_interval': 0.5,
        'log_level': 'INFO',
        'cache_enabled': True,
        'async_max_workers': 5
    }


# 创建全局配置实例
DEFAULT_CONFIG = get_default_config()
configuration = Configuration(DEFAULT_CONFIG)


def get_config() -> Configuration:
    """获取全局配置实例
    
    Returns:
        Configuration: 全局配置实例
    """
    return configuration