# robotframework_robocorp_windows/services/control_service.py

"""
控件操作服务，封装控件操作的核心业务逻辑
"""

from ..drivers.robocorp_driver import RobocorpWindowsDriver
from ..utils.exceptions import (
    ControlNotFoundError,
    ControlOperationException
)
from ..utils.cache import ControlCache
from robocorp.windows import ElementNotFound


class ControlService:
    """控件操作服务，提供控件相关的业务逻辑"""
    
    def __init__(self, driver=None):
        """初始化控件服务
        
        Args:
            driver: RobocorpWindowsDriver实例，如果为None则创建新实例
        """
        self.driver = driver or RobocorpWindowsDriver()
        self.logger = None
        self.control_cache = ControlCache()
        self.cache_enabled = True  # 默认启用缓存
    
    def set_logger(self, logger):
        """设置日志记录器
        
        Args:
            logger: 日志记录器对象
        """
        self.logger = logger
        self.driver.set_logger(logger)
    
    def find_control(self, window, control_identifier, timeout=10, use_cache=True):
        """在窗口中查找控件
        
        Args:
            window: 窗口元素
            control_identifier: 控件标识符
            timeout: 超时时间（秒）
            use_cache: 是否使用缓存（默认：True）
            
        Returns:
            ControlElement: 找到的控件元素
            
        Raises:
            ControlNotFoundError: 控件未找到时
        """
        if use_cache and self.cache_enabled:
            # 尝试从缓存获取
            control, is_cached = self.control_cache.get(window, control_identifier)
            if is_cached:
                return control
        
        # 从驱动层查找控件
        control = self.driver.find_control(window, control_identifier, timeout)
        
        if use_cache and self.cache_enabled:
            # 将控件存入缓存
            self.control_cache.set(window, control_identifier, control, timeout)
        
        return control
    
    def clear_cache(self, window=None):
        """清空缓存
        
        Args:
            window: 窗口元素，如果提供则只清空该窗口的缓存
        """
        self.control_cache.clear(window)
    
    def enable_cache(self):
        """启用缓存"""
        self.cache_enabled = True
    
    def disable_cache(self):
        """禁用缓存"""
        self.cache_enabled = False
    
    def is_cache_enabled(self):
        """检查缓存是否启用
        
        Returns:
            bool: 缓存是否启用
        """
        return self.cache_enabled
    
    def click_control(self, control):
        """点击控件
        
        Args:
            control: 控件元素
            
        Raises:
            ControlOperationException: 控件操作失败时
        """
        try:
            control.click()
        except Exception as e:
            raise ControlOperationException(f"Failed to click control: {str(e)}")
    
    def double_click_control(self, control):
        """双击控件
        
        Args:
            control: 控件元素
            
        Raises:
            ControlOperationException: 控件操作失败时
        """
        try:
            control.double_click()
        except Exception as e:
            raise ControlOperationException(f"Failed to double click control: {str(e)}")
    
    def right_click_control(self, control):
        """右键点击控件
        
        Args:
            control: 控件元素
            
        Raises:
            ControlOperationException: 控件操作失败时
        """
        try:
            control.right_click()
        except Exception as e:
            raise ControlOperationException(f"Failed to right click control: {str(e)}")
    
    def type_into_control(self, control, text):
        """向控件输入文本
        
        Args:
            control: 控件元素
            text: 要输入的文本
            
        Raises:
            ControlOperationException: 控件操作失败时
        """
        try:
            control.type(text)
        except Exception as e:
            raise ControlOperationException(f"Failed to type into control: {str(e)}")
    
    def get_control_text(self, control):
        """获取控件文本
        
        Args:
            control: 控件元素
            
        Returns:
            str: 控件文本
            
        Raises:
            ControlOperationException: 控件操作失败时
        """
        try:
            return control.text
        except Exception as e:
            raise ControlOperationException(f"Failed to get control text: {str(e)}")
    
    def set_control_value(self, control, value):
        """设置控件值
        
        Args:
            control: 控件元素
            value: 要设置的值
            
        Raises:
            ControlOperationException: 控件操作失败时
        """
        try:
            control.set_value(value)
        except Exception as e:
            raise ControlOperationException(f"Failed to set control value: {str(e)}")
    
    def get_control_value(self, control):
        """获取控件值
        
        Args:
            control: 控件元素
            
        Returns:
            str: 控件值
            
        Raises:
            ControlOperationException: 控件操作失败时
        """
        try:
            return control.get_value()
        except Exception as e:
            raise ControlOperationException(f"Failed to get control value: {str(e)}")
    
    def select_from_combobox(self, control, item):
        """从组合框中选择项目
        
        Args:
            control: 组合框控件元素
            item: 要选择的项目
            
        Raises:
            ControlOperationException: 控件操作失败时
        """
        try:
            control.select(item)
        except Exception as e:
            raise ControlOperationException(f"Failed to select from combobox: {str(e)}")
    
    def check_checkbox(self, control):
        """勾选复选框
        
        Args:
            control: 复选框控件元素
            
        Raises:
            ControlOperationException: 控件操作失败时
        """
        try:
            control.check()
        except Exception as e:
            raise ControlOperationException(f"Failed to check checkbox: {str(e)}")
    
    def uncheck_checkbox(self, control):
        """取消勾选复选框
        
        Args:
            control: 复选框控件元素
            
        Raises:
            ControlOperationException: 控件操作失败时
        """
        try:
            control.uncheck()
        except Exception as e:
            raise ControlOperationException(f"Failed to uncheck checkbox: {str(e)}")
    
    def is_checkbox_checked(self, control):
        """检查复选框是否已勾选
        
        Args:
            control: 复选框控件元素
            
        Returns:
            bool: 复选框是否已勾选
            
        Raises:
            ControlOperationException: 控件操作失败时
        """
        try:
            return control.is_checked()
        except Exception as e:
            raise ControlOperationException(f"Failed to check checkbox state: {str(e)}")
    
    def control_should_exist(self, window, control_identifier, timeout=10):
        """验证控件是否存在
        
        Args:
            window: 窗口元素
            control_identifier: 控件标识符
            timeout: 超时时间（秒）
            
        Raises:
            AssertionError: 控件不存在时
        """
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self.find_control(window, control_identifier, timeout=0.5)
                return True
            except ControlNotFoundError:
                time.sleep(0.5)
        
        raise AssertionError(f"Control not found: {control_identifier}")
    
    def control_should_not_exist(self, window, control_identifier, timeout=10):
        """验证控件是否不存在
        
        Args:
            window: 窗口元素
            control_identifier: 控件标识符
            timeout: 超时时间（秒）
            
        Raises:
            AssertionError: 控件存在时
        """
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self.find_control(window, control_identifier, timeout=0.5)
                time.sleep(0.5)
            except ControlNotFoundError:
                return True
        
        raise AssertionError(f"Control should not exist but was found: {control_identifier}")
