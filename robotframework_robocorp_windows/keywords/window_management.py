from robot.api.deco import keyword
from ..services.window_service import WindowService
from ..utils.exceptions import (
    WindowNotFoundError,
    ControlNotFoundError,
    ApplicationLaunchError,
    ApplicationConnectionError
)

class WindowManagementKeywords:
    """Keywords for window management operations."""
    
    def __init__(self, library):
        """Initialize WindowManagementKeywords with the main library instance."""
        self.library = library
        self.logger = library.logger
        self.builtin = library.builtin
        self.window_service = WindowService()
        self.window_service.set_logger(self.logger)
        
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
        | ${app_id} | Launch Application | C:/Program Files/MyApp/myapp.exe | timeout=5 |
        """
        timeout = timeout or self.library.timeout
        self.library._log(f"Launching application: {app_path}")
        
        # Use WindowService to launch application and find main window
        executable_name, window = self.window_service.launch_application(app_path, timeout)
        
        if window:
            self.library.current_window = window
            # Get window title using the service
            window_title = self.window_service.get_window_title(window)
            self.library._log(f"Found main window: {window_title}")
        else:
            self.library._log(f"Could not automatically find main window for {executable_name}", level="WARN")
        
        # Register application in cache
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
        
        try:
            # Use WindowService to connect to application
            locator, window = self.window_service.connect_to_application(title, class_name, process, timeout)
            
            self.library.current_window = window
            # Get window title using the service
            window_title = self.window_service.get_window_title(window)
            self.library._log(f"Found main window: {window_title}")
            
            # Register application in cache
            app_id = self.library.cache.register({"locator": locator, "window": window})
            return app_id
        except WindowNotFoundError as e:
            # Re-raise with appropriate message
            raise AssertionError(str(e))
    
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
        
        try:
            # Use WindowService to find and set current window
            window = self.window_service.set_current_window(title, class_name, timeout)
            
            self.library.current_window = window
            # Get window title using the service
            window_title = self.window_service.get_window_title(window)
            self.library._log(f"Set current window to: {window_title}")
        except WindowNotFoundError as e:
            # Re-raise with appropriate message
            raise AssertionError(str(e))
    
    @keyword("Close Application")
    def close_application(self):
        """Close the currently connected application.
        
        Examples:
        | Close Application |
        """
        # Get current window (will raise exception if no active window)
        window = self.library._get_current_window()
        
        # Get window title using the service
        window_title = self.window_service.get_window_title(window)
        self.library._log(f"Closing window: {window_title}")
        self.window_service.close_window(window)
        self.library.current_window = None
    
    @keyword("Minimize Window")
    def minimize_window(self):
        """Minimize the current window.
        
        Examples:
        | Minimize Window |
        """
        window = self.library._get_current_window()
        # Get window title using the service
        window_title = self.window_service.get_window_title(window)
        self.library._log(f"Minimizing window: {window_title}")
        self.window_service.minimize_window(window)
    
    @keyword("Maximize Window")
    def maximize_window(self):
        """Maximize the current window.
        
        Examples:
        | Maximize Window |
        """
        window = self.library._get_current_window()
        # Get window title using the service
        window_title = self.window_service.get_window_title(window)
        self.library._log(f"Maximizing window: {window_title}")
        self.window_service.maximize_window(window)
    
    @keyword("Restore Window")
    def restore_window(self):
        """Restore the current window from minimized or maximized state.
        
        Examples:
        | Restore Window |
        """
        window = self.library._get_current_window()
        # Get window title using the service
        window_title = self.window_service.get_window_title(window)
        self.library._log(f"Restoring window: {window_title}")
        self.window_service.restore_window(window)
    
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
        
        # Use WindowService to check if window is open
        self.window_service.window_should_be_open(title, class_name, timeout, self.library.current_window)
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
        
        # Use WindowService to check if window is closed
        self.window_service.window_should_be_closed(title, class_name, timeout, self.library.current_window)
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
        # Use WindowService to get window title
        title = self.window_service.get_window_title(window)
        self.library._log(f"Current window title: {title}")
        return title