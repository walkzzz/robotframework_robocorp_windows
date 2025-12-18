# robotframework_robocorp_windows/drivers/robocorp_driver.py

"""
robocorp-windows底层库的封装，提供统一的接口用于访问底层功能
"""

from robocorp.windows import desktop, find_window, find_windows, ElementNotFound, WindowElement
import subprocess
import time
from ..utils.exceptions import (
    WindowNotFoundError,
    ControlNotFoundError,
    ApplicationLaunchError,
    ApplicationConnectionError
)


class RobocorpWindowsDriver:
    """robocorp-windows底层驱动，封装对底层库的调用"""
    
    def __init__(self):
        """初始化驱动"""
        self.logger = None
    
    def set_logger(self, logger):
        """设置日志记录器
        
        Args:
            logger: 日志记录器对象
        """
        self.logger = logger
    
    def launch_application(self, app_path):
        """启动Windows应用程序
        
        Args:
            app_path: 应用程序可执行文件路径
            
        Returns:
            str: 可执行文件名
            
        Raises:
            ApplicationLaunchError: 应用程序启动失败时
        """
        try:
            subprocess.Popen(app_path)
            time.sleep(1)  # 给应用程序一些启动时间
            executable_name = app_path.split('\\')[-1] if '\\' in app_path else app_path
            return executable_name
        except Exception as e:
            raise ApplicationLaunchError(f"Failed to launch application {app_path}: {str(e)}")
    
    def find_window_by_executable(self, executable_name, timeout=10):
        """根据可执行文件名查找窗口
        
        Args:
            executable_name: 可执行文件名
            timeout: 超时时间（秒）
            
        Returns:
            WindowElement: 找到的窗口元素
            
        Raises:
            WindowNotFoundError: 窗口未找到时
        """
        def _find_window():
            try:
                windows = find_windows(f"executable:{executable_name}")
                return windows[0] if windows else None
            except Exception:
                return None
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            window = _find_window()
            if window:
                return window
            time.sleep(0.5)
        
        raise WindowNotFoundError(f"Window not found for executable {executable_name}")
    
    def find_window_by_locator(self, locator, timeout=10):
        """根据定位符查找窗口
        
        Args:
            locator: 窗口定位符
            timeout: 超时时间（秒）
            
        Returns:
            WindowElement: 找到的窗口元素
            
        Raises:
            WindowNotFoundError: 窗口未找到时
        """
        def _find_window():
            try:
                return find_window(locator, raise_error=False)
            except Exception:
                return None
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            window = _find_window()
            if window:
                return window
            time.sleep(0.5)
        
        raise WindowNotFoundError(f"Window not found with locator: {locator}")
    
    def find_control(self, window, control_identifier, timeout=10):
        """在窗口中查找控件

        Args:
            window: 窗口元素
            control_identifier: 控件标识符
            timeout: 超时时间（秒）

        Returns:
            ControlElement: 找到的控件元素

        Raises:
            ControlNotFoundError: 控件未找到时
        """
        # 验证定位符格式
        valid_formats = ["name:", "id:", "class:", "text:"]
        has_valid_prefix = any(control_identifier.startswith(format) for format in valid_formats)
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if isinstance(window, WindowElement):
                    return window.find(control_identifier)
                else:
                    return find_window(f"{window} {control_identifier}")
            except ElementNotFound:
                time.sleep(0.5)
        
        # 优化异常消息，提供有效定位符格式
        if not has_valid_prefix:
            raise ControlNotFoundError(f"Control not found with identifier: {control_identifier}. Valid locator formats: name:Button1, id:123, class:Edit, text:OK")
        else:
            raise ControlNotFoundError(f"Control not found with identifier: {control_identifier}")
    
    def get_window_title(self, window):
        """获取窗口标题
        
        Args:
            window: 窗口元素
            
        Returns:
            str: 窗口标题
        """
        return window.name if hasattr(window, 'name') else str(window)
    
    def close_window(self, window):
        """关闭窗口
        
        Args:
            window: 窗口元素
        """
        window.close_window()
    
    def minimize_window(self, window):
        """最小化窗口
        
        Args:
            window: 窗口元素
        """
        window.minimize_window()
    
    def maximize_window(self, window):
        """最大化窗口
        
        Args:
            window: 窗口元素
        """
        window.maximize_window()
    
    def restore_window(self, window):
        """恢复窗口
        
        Args:
            window: 窗口元素
        """
        window.restore_window()
    
    def window_exists(self, window):
        """检查窗口是否存在
        
        Args:
            window: 窗口元素
            
        Returns:
            bool: 窗口是否存在
        """
        return hasattr(window, 'exists') and window.exists()
    
    def get_window_by_locator(self, locator, timeout=1):
        """根据定位符获取窗口（立即返回，不等待）
        
        Args:
            locator: 窗口定位符
            timeout: 超时时间（秒）
            
        Returns:
            WindowElement or None: 窗口元素或None
        """
        try:
            return find_window(locator, raise_error=False, timeout=timeout)
        except Exception:
            return None
