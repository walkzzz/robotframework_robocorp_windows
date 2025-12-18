from robot.api.deco import keyword
from robocorp.windows import desktop, find_window, find_windows, ElementNotFound, WindowElement
import time
import subprocess

class WindowManagementKeywords:
    """Keywords for window management operations."""
    
    def __init__(self, library):
        """Initialize WindowManagementKeywords with the main library instance."""
        self.library = library
        self.logger = library.logger
        self.builtin = library.builtin
        
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
        timeout = timeout or self.library.timeout
        self.library._log(f"Launching application: {app_path}")
        
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
        window = self.library._wait_until(find_main_window, timeout)
        if window:
            self.library.current_window = window
            # In robocorp-windows 1.0.0, use name property to get window title
            self.library._log(f"Found main window: {window.name}")
        else:
            self.library._log(f"Could not automatically find main window for {executable_name}", level="WARN")
        
        # In this API, we don't have an Application object, so we'll just use a dummy identifier
        app_id = self.library.cache.register({"executable": executable_name, "window": window})
        return app_id
    
    @keyword("Connect To Application")
    def connect_to_application(self, title=None, class_name=None, process=None, timeout=None):
        """Connect to an already running application.
        
        Args:
            title: Window title or partial title to match
            class_name: Window class name to match
            process: Process ID to connect to
            timeout: Timeout for waiting until the application is ready (default: library timeout)
            
        Returns:
            str: Application identifier that can be used with other keywords
            
        Examples:
        | Connect To Application | title=Notepad |
        | ${app_id} | Connect To Application | process=${PID} |
        """
        timeout = timeout or self.library.timeout
        self.library._log(f"Connecting to application with title='{title}', class_name='{class_name}', process='{process}'")
        
        # Build locator string
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
        
        # Find the window
        def find_window_func():
            try:
                return find_window(locator, raise_error=False)
            except Exception:
                return None
        
        window = self.library._wait_until(find_window_func, timeout)
        if not window:
            raise ElementNotFound(f"Window not found with locator: {locator}")
        
        self.library.current_window = window
        # In robocorp-windows 1.0.0, use name property to get window title
        self.library._log(f"Found main window: {window.name}")
        
        # In this API, we don't have an Application object, so we'll just use a dummy identifier
        app_id = self.library.cache.register({"locator": locator, "window": window})
        return app_id
    
    @keyword("Set Current Window")
    def set_current_window(self, title=None, class_name=None, timeout=None):
        """Set the current active window.
        
        Args:
            title: Window title or partial title to match
            class_name: Window class name to match
            timeout: Timeout for waiting until the window is available (default: library timeout)
            
        Examples:
        | Set Current Window | title=Notepad |
        | Set Current Window | title=MyApp | class_name=MyAppMainWindow |
        """
        timeout = timeout or self.library.timeout
        self.library._log(f"Setting current window with title='{title}', class_name='{class_name}'")
        
        # Build locator string
        locator_parts = []
        if title:
            locator_parts.append(f"name:{title}")
        if class_name:
            locator_parts.append(f"class:{class_name}")
        
        if not locator_parts:
            # If no locator provided, use the first top-level window
            locator = "regex:.*"
        else:
            locator = " ".join(locator_parts)
        
        # Wait for window to be available
        def find_window_func():
            try:
                return find_window(locator, raise_error=False)
            except Exception:
                return None
        
        window = self.library._wait_until(find_window_func, timeout)
        if not window:
            raise ElementNotFound(f"Window not found with title='{title}', class_name='{class_name}'")
        
        self.library.current_window = window
        # In robocorp-windows 1.0.0, use name property to get window title
        self.library._log(f"Set current window to: {window.name}")
    
    @keyword("Close Application")
    def close_application(self):
        """Close the currently connected application.
        
        Examples:
        | Close Application |
        """
        if self.library.current_window:
            # In robocorp-windows 1.0.0, use name property to get window title
            self.library._log(f"Closing window: {self.library.current_window.name}")
            self.library.current_window.close_window()
            self.library.current_window = None
        
    @keyword("Minimize Window")
    def minimize_window(self):
        """Minimize the current window.
        
        Examples:
        | Minimize Window |
        """
        window = self.library._get_current_window()
        # In robocorp-windows 1.0.0, use name property to get window title
        self.library._log(f"Minimizing window: {window.name}")
        window.minimize_window()
    
    @keyword("Maximize Window")
    def maximize_window(self):
        """Maximize the current window.
        
        Examples:
        | Maximize Window |
        """
        window = self.library._get_current_window()
        # In robocorp-windows 1.0.0, use name property to get window title
        self.library._log(f"Maximizing window: {window.name}")
        window.maximize_window()
    
    @keyword("Restore Window")
    def restore_window(self):
        """Restore the current window from minimized or maximized state.
        
        Examples:
        | Restore Window |
        """
        window = self.library._get_current_window()
        # In robocorp-windows 1.0.0, use name property to get window title
        self.library._log(f"Restoring window: {window.name}")
        window.restore_window()
    
    @keyword("Window Should Be Open")
    def window_should_be_open(self, title=None, class_name=None, timeout=None):
        """Verify that a window is open.
        
        Args:
            title: Window title or partial title to match
            class_name: Window class name to match
            timeout: Timeout for waiting until the window is available (default: library timeout)
            
        Examples:
        | Window Should Be Open | title=Notepad |
        | Window Should Be Open | title=MyApp | class_name=MyAppMainWindow | timeout=5 |
        """
        timeout = timeout or self.library.timeout
        
        def window_exists():
            try:
                # Build locator string
                locator_parts = []
                if title:
                    locator_parts.append(f"name:{title}")
                if class_name:
                    locator_parts.append(f"class:{class_name}")
                
                if not locator_parts:
                    # If no locator provided, check if current window exists
                    return self.library.current_window is not None and self.library.current_window.exists()
                
                locator = " ".join(locator_parts)
                window = find_window(locator, raise_error=False, timeout=0.5)
                return window is not None
            except Exception:
                return False
        
        if not self.library._wait_until(window_exists, timeout):
            raise AssertionError(f"Window not found with title='{title}', class_name='{class_name}'")
        
        self.library._log(f"Window is open: title='{title}', class_name='{class_name}'")
    
    @keyword("Window Should Be Closed")
    def window_should_be_closed(self, title=None, class_name=None, timeout=None):
        """Verify that a window is closed.
        
        Args:
            title: Window title or partial title to match
            class_name: Window class name to match
            timeout: Timeout for waiting until the window is closed (default: library timeout)
            
        Examples:
        | Window Should Be Closed | title=Notepad |
        | Window Should Be Closed | title=MyApp | class_name=MyAppDialog | timeout=5 |
        """
        timeout = timeout or self.library.timeout
        
        def window_not_exists():
            try:
                # Build locator string
                locator_parts = []
                if title:
                    locator_parts.append(f"name:{title}")
                if class_name:
                    locator_parts.append(f"class:{class_name}")
                
                if not locator_parts:
                    # If no locator provided, check if current window is closed
                    return self.library.current_window is None or not self.library.current_window.exists()
                
                locator = " ".join(locator_parts)
                window = find_window(locator, raise_error=False, timeout=0.5)
                return window is None
            except Exception:
                return True
        
        if not self.library._wait_until(window_not_exists, timeout):
            raise AssertionError(f"Window is still open: title='{title}', class_name='{class_name}'")
        
        self.library._log(f"Window is closed: title='{title}', class_name='{class_name}'")
    
    @keyword("Get Window Title")
    def get_window_title(self):
        """Get the title of the current window.
        
        Returns:
            str: Title of the current window
            
        Examples:
        | ${title} | Get Window Title |
        | Should Contain | ${title} | Notepad |
        """
        window = self.library._get_current_window()
        # In robocorp-windows 1.0.0, use name property to get window title
        title = window.name
        self.library._log(f"Current window title: {title}")
        return title