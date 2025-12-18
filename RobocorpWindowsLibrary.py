# -*- coding: utf-8 -*-
"""
Robot Framework library for Windows automation using robocorp-windows.
"""

from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import ConnectionCache, timestr_to_secs
import logging
import time
import subprocess
from robocorp.windows import desktop, find_window, find_windows, ElementNotFound, WindowElement

@library(scope='GLOBAL', version='1.0.0')
class RobocorpWindowsLibrary:
    """Robocorp Windows Library is a Robot Framework library for Windows automation using robocorp-windows.
    
    This library provides keywords to interact with Windows applications, including window management,
    control operations, and keyboard/mouse simulations.
    
    Examples:
    | Library | RobocorpWindowsLibrary | timeout=10 | retry_interval=0.5 |
    | Launch Application | notepad.exe |
    | Type Into Control | Edit | Hello World |
    | Close Application |
    """
    
    ROBOT_LIBRARY_VERSION = '1.0.0'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_DOC_FORMAT = 'reST'
    
    def __init__(self, timeout=10, retry_interval=0.5):
        """Initialize RobocorpWindowsLibrary library with specified configuration.
        
        Args:
            timeout: Default timeout for waiting operations in seconds (default: 10)
            retry_interval: Interval between retries in seconds (default: 0.5)
        """
        self.timeout = timestr_to_secs(timeout)
        self.retry_interval = timestr_to_secs(retry_interval)
        self.current_window = None
        self.cache = ConnectionCache()
        self.logger = logging.getLogger(__name__)
        self.builtin = BuiltIn()
    
    @keyword("Launch Application")
    def launch_application(self, app_path, timeout=None):
        """Launch a Windows application and connect to it.
        
        Args:
            app_path: Path to the application executable.
            timeout: Timeout for waiting until the application is ready (default: library timeout)
            
        Returns:
            str: Application identifier that can be used with other keywords
            
        Examples:
        | Launch Application | notepad.exe |
        | ${app_id} | Launch Application | C:\Program Files\MyApp\myapp.exe | timeout=5 |
        """
        timeout = timeout or self.timeout
        self._log(f"Launching application: {app_path}")
        
        # Start the application
        subprocess.Popen(app_path)
        time.sleep(1)  # Give some time for the application to start
        
        # Try to find the main window by executable name
        executable_name = app_path.split('\\')[-1] if '\\' in app_path else app_path
        
        def find_main_window():
            try:
                windows = find_windows(f"executable:{executable_name}")
                return windows[0] if windows else None
            except Exception:
                return None
        
        # Wait for window to appear
        window = self._wait_until(find_main_window, timeout)
        if window:
            self.current_window = window
            self._log(f"Found main window: {window.title}")
        else:
            self._log(f"Could not automatically find main window for {executable_name}", level="WARN")
        
        # In this API, we don't have an Application object, so we'll just use a dummy identifier
        return f"app_{id(self)}"
    
    @keyword("Get Window Title")
    def get_window_title(self):
        """Get the title of the current window.
        
        Returns:
            str: Title of the current window
            
        Examples:
        | ${title} | Get Window Title |
        | Should Contain | ${title} | Notepad |
        """
        window = self._get_current_window()
        title = window.title
        self._log(f"Current window title: {title}")
        return title
    
    def _get_current_window(self):
        """Get the current window instance.
        
        Returns:
            Window: The current window instance
            
        Raises:
            RuntimeError: If no window is active
        """
        if not self.current_window:
            raise RuntimeError("No active window. Use 'Set Current Window' or 'Launch Application' first.")
        return self.current_window
        
    def _log(self, message, level='INFO'):
        """Log a message using Robot Framework's logging system.
        
        Args:
            message: Message to log
            level: Log level ('TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR')
        """
        self.builtin.log(message, level)
        
    def _wait_until(self, condition, timeout=None, retry_interval=None):
        """Wait until a condition is met.
        
        Args:
            condition: Callable that returns True when the condition is met
            timeout: Maximum time to wait in seconds
            retry_interval: Interval between retries in seconds
            
        Returns:
            bool: True if condition was met, False otherwise
        """
        timeout = timeout or self.timeout
        retry_interval = retry_interval or self.retry_interval
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            result = condition()
            if result:
                return result
            time.sleep(retry_interval)
        return False