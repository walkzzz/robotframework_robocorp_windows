# robotframework_robocorp_windows/utils/logger.py

"""
日志工具模块，实现结构化日志系统
"""

import logging
import time
from typing import Any, Optional
from .config import get_config


class RobocorpWindowsLogger:
    """结构化日志记录器"""
    
    def __init__(self, name: str = __name__):
        """初始化日志记录器
        
        Args:
            name: 日志记录器名称
        """
        self._logger = logging.getLogger(name)
        self.config = get_config()
        # 设置日志级别
        log_level = self.config.get('log_level', 'INFO').upper()
        self._logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    def _get_log_message(self, message: str, **kwargs) -> str:
        """构建结构化日志消息
        
        Args:
            message: 基本消息
            **kwargs: 额外的日志字段
            
        Returns:
            str: 结构化日志消息
        """
        log_fields = [f"{k}={v}" for k, v in kwargs.items() if v is not None]
        if log_fields:
            return f"{message} | {', '.join(log_fields)}"
        return message
    
    def trace(self, message: str, **kwargs):
        """记录TRACE级别的日志
        
        Args:
            message: 日志消息
            **kwargs: 额外的日志字段
        """
        if self._logger.isEnabledFor(logging.DEBUG - 5):  # TRACE级别
            self._logger.log(logging.DEBUG - 5, self._get_log_message(message, **kwargs))
    
    def debug(self, message: str, **kwargs):
        """记录DEBUG级别的日志，用于控件查找细节
        
        Args:
            message: 日志消息
            **kwargs: 额外的日志字段
        """
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(self._get_log_message(message, **kwargs))
    
    def info(self, message: str, **kwargs):
        """记录INFO级别的日志，用于关键字执行结果
        
        Args:
            message: 日志消息
            **kwargs: 额外的日志字段
        """
        if self._logger.isEnabledFor(logging.INFO):
            self._logger.info(self._get_log_message(message, **kwargs))
    
    def warn(self, message: str, **kwargs):
        """记录WARN级别的日志，用于非致命错误
        
        Args:
            message: 日志消息
            **kwargs: 额外的日志字段
        """
        if self._logger.isEnabledFor(logging.WARNING):
            self._logger.warning(self._get_log_message(message, **kwargs))
    
    def error(self, message: str, **kwargs):
        """记录ERROR级别的日志，用于异常信息
        
        Args:
            message: 日志消息
            **kwargs: 额外的日志字段
        """
        if self._logger.isEnabledFor(logging.ERROR):
            self._logger.error(self._get_log_message(message, **kwargs))
    
    def log_keyword(self, keyword_name: str, args: tuple, kwargs: dict, result: Any = None, duration: Optional[float] = None, window_id: Any = None, control_id: Any = None):
        """记录关键字执行日志
        
        Args:
            keyword_name: 关键字名称
            args: 关键字位置参数
            kwargs: 关键字关键字参数
            result: 关键字返回结果
            duration: 执行耗时（秒）
            window_id: 关联的窗口ID
            control_id: 关联的控件ID
        """
        log_kwargs = {
            'keyword': keyword_name,
            'args': args,
            'kwargs': kwargs,
            'duration': f"{duration:.3f}s" if duration is not None else None,
            'window_id': window_id,
            'control_id': control_id,
            'result': result
        }
        self.info(f"Keyword executed", **log_kwargs)
    
    def log_control_operation(self, operation: str, control_identifier: str, window: Any = None, duration: Optional[float] = None):
        """记录控件操作日志
        
        Args:
            operation: 操作名称，如 "click", "type", "find"
            control_identifier: 控件标识符
            window: 窗口元素
            duration: 执行耗时（秒）
        """
        window_id = getattr(window, 'handle', id(window)) if window else None
        log_kwargs = {
            'operation': operation,
            'control_identifier': control_identifier,
            'window_id': window_id,
            'duration': f"{duration:.3f}s" if duration is not None else None
        }
        self.info(f"Control operation executed", **log_kwargs)
    
    def log_window_operation(self, operation: str, window_identifier: str, duration: Optional[float] = None):
        """记录窗口操作日志
        
        Args:
            operation: 操作名称，如 "launch", "close", "set_current"
            window_identifier: 窗口标识符
            duration: 执行耗时（秒）
        """
        log_kwargs = {
            'operation': operation,
            'window_identifier': window_identifier,
            'duration': f"{duration:.3f}s" if duration is not None else None
        }
        self.info(f"Window operation executed", **log_kwargs)
    
    def set_level(self, level: str):
        """设置日志级别
        
        Args:
            level: 日志级别，如 "DEBUG", "INFO", "WARN", "ERROR"
        """
        log_level = level.upper()
        self._logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    def get_level(self) -> str:
        """获取当前日志级别
        
        Returns:
            str: 当前日志级别
        """
        return logging.getLevelName(self._logger.level)


# 创建全局日志记录器实例
logger = RobocorpWindowsLogger()


def get_logger(name: str = __name__) -> RobocorpWindowsLogger:
    """获取日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        RobocorpWindowsLogger: 日志记录器实例
    """
    return RobocorpWindowsLogger(name)
