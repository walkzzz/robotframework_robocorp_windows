# robotframework_robocorp_windows/services/window_service.py

"""
窗口管理服务，封装窗口管理的核心业务逻辑
"""

from ..drivers.robocorp_driver import RobocorpWindowsDriver
from ..utils.exceptions import (
    WindowNotFoundError,
    ApplicationLaunchError,
    ApplicationConnectionError
)


class WindowService:
    """窗口管理服务，提供窗口相关的业务逻辑"""
    
    def __init__(self, driver=None):
        """初始化窗口服务
        
        Args:
            driver: RobocorpWindowsDriver实例，如果为None则创建新实例
        """
        self.driver = driver or RobocorpWindowsDriver()
        self.logger = None
    
    def set_logger(self, logger):
        """设置日志记录器
        
        Args:
            logger: 日志记录器对象
        """
        self.logger = logger
        self.driver.set_logger(logger)
    
    def launch_application(self, app_path, timeout=10):
        """启动Windows应用程序并找到主窗口
        
        Args:
            app_path: 应用程序可执行文件路径
            timeout: 超时时间（秒）
            
        Returns:
            tuple: (executable_name, window) - 可执行文件名和找到的窗口元素
            
        Raises:
            ApplicationLaunchError: 应用程序启动失败时
            WindowNotFoundError: 未找到主窗口时
        """
        # 启动应用程序
        executable_name = self.driver.launch_application(app_path)
        
        # 尝试查找主窗口
        try:
            window = self.driver.find_window_by_executable(executable_name, timeout)
            return executable_name, window
        except WindowNotFoundError:
            # 如果找不到，返回None作为窗口
            return executable_name, None
    
    def connect_to_application(self, title=None, class_name=None, process=None, timeout=10):
        """连接到已运行的应用程序
        
        Args:
            title: 窗口标题或部分标题
            class_name: 窗口类名
            process: 进程ID
            timeout: 超时时间（秒）
            
        Returns:
            tuple: (locator, window) - 定位符和找到的窗口元素
            
        Raises:
            ValueError: 未提供任何定位信息时
            WindowNotFoundError: 未找到窗口时
        """
        # 构建定位符字符串
        locator_parts = []
        if title:
            locator_parts.append(f"name:{title}")
        if class_name:
            locator_parts.append(f"class:{class_name}")
        if process:
            locator_parts.append(f"pid:{process}")
        
        if not locator_parts:
            raise ValueError("At least one of title, class_name, or process must be provided.")
        
        locator = " ".join(locator_parts)
        
        # 查找窗口
        window = self.driver.find_window_by_locator(locator, timeout)
        return locator, window
    
    def set_current_window(self, title=None, class_name=None, timeout=10):
        """设置当前活动窗口
        
        Args:
            title: 窗口标题或部分标题
            class_name: 窗口类名
            timeout: 超时时间（秒）
            
        Returns:
            WindowElement: 找到的窗口元素
            
        Raises:
            WindowNotFoundError: 未找到窗口时
        """
        # 构建定位符字符串
        locator_parts = []
        if title:
            locator_parts.append(f"name:{title}")
        if class_name:
            locator_parts.append(f"class:{class_name}")
        
        if not locator_parts:
            # 如果没有提供定位符，使用第一个顶级窗口
            locator = "regex:.*"
        else:
            locator = " ".join(locator_parts)
        
        # 查找窗口
        window = self.driver.find_window_by_locator(locator, timeout)
        return window
    
    def get_window_title(self, window):
        """获取窗口标题
        
        Args:
            window: 窗口元素
            
        Returns:
            str: 窗口标题
        """
        return self.driver.get_window_title(window)
    
    def close_window(self, window):
        """关闭窗口
        
        Args:
            window: 窗口元素
        """
        self.driver.close_window(window)
    
    def minimize_window(self, window):
        """最小化窗口
        
        Args:
            window: 窗口元素
        """
        self.driver.minimize_window(window)
    
    def maximize_window(self, window):
        """最大化窗口
        
        Args:
            window: 窗口元素
        """
        self.driver.maximize_window(window)
    
    def restore_window(self, window):
        """恢复窗口
        
        Args:
            window: 窗口元素
        """
        self.driver.restore_window(window)
    
    def window_should_be_open(self, title=None, class_name=None, timeout=10, current_window=None):
        """验证窗口是否打开
        
        Args:
            title: 窗口标题或部分标题
            class_name: 窗口类名
            timeout: 超时时间（秒）
            current_window: 当前窗口元素
            
        Raises:
            AssertionError: 窗口未找到时
        """
        def window_exists():
            try:
                # 构建定位符字符串
                locator_parts = []
                if title:
                    locator_parts.append(f"name:{title}")
                if class_name:
                    locator_parts.append(f"class:{class_name}")
                
                if not locator_parts:
                    # 如果没有提供定位符，检查当前窗口是否存在
                    return current_window is not None and self.driver.window_exists(current_window)
                
                locator = " ".join(locator_parts)
                window = self.driver.get_window_by_locator(locator, timeout=0.5)
                return window is not None
            except Exception:
                return False
        
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            if window_exists():
                return
            time.sleep(0.5)
        
        raise AssertionError(f"Window not found with title='{title}', class_name='{class_name}'")
    
    def window_should_be_closed(self, title=None, class_name=None, timeout=10, current_window=None):
        """验证窗口是否关闭
        
        Args:
            title: 窗口标题或部分标题
            class_name: 窗口类名
            timeout: 超时时间（秒）
            current_window: 当前窗口元素
            
        Raises:
            AssertionError: 窗口仍然打开时
        """
        def window_not_exists():
            try:
                # 构建定位符字符串
                locator_parts = []
                if title:
                    locator_parts.append(f"name:{title}")
                if class_name:
                    locator_parts.append(f"class:{class_name}")
                
                if not locator_parts:
                    # 如果没有提供定位符，检查当前窗口是否关闭
                    return current_window is None or not self.driver.window_exists(current_window)
                
                locator = " ".join(locator_parts)
                window = self.driver.get_window_by_locator(locator, timeout=0.5)
                return window is None
            except Exception:
                return True
        
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            if window_not_exists():
                return
            time.sleep(0.5)
        
        raise AssertionError(f"Window is still open: title='{title}', class_name='{class_name}'")
