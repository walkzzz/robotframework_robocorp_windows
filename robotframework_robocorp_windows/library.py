from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import ConnectionCache, timestr_to_secs
import logging
import time

# Import custom exceptions
from .utils.exceptions import ApplicationNotConnectedError, NoActiveWindowError

# Import keyword modules
from .keywords.window_management import WindowManagementKeywords
from .keywords.control_operations import ControlOperationsKeywords
from .keywords.keyboard_mouse import KeyboardMouseKeywords
from .keywords.async_control_operations import AsyncControlOperationsKeywords

@library(scope='GLOBAL', version='1.0.0')
class RobocorpWindows:
    ROBOT_LIBRARY_VERSION = '1.0.0'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_DOC_FORMAT = 'reST'
    """Robocorp Windows Library is a Robot Framework library for Windows automation using robocorp-windows.
    
    This library provides keywords to interact with Windows applications, including window management,
    control operations, and keyboard/mouse simulations.
    
    Examples:
    | Library | RobocorpWindows | timeout=10 | retry_interval=0.5 |
    | Launch Application | notepad.exe |
    | Type Into Control | Edit | Hello World |
    | Close Application |
    """
    
    def __init__(self, timeout=10, retry_interval=0.5, log_level='INFO'):
        """Initialize RobocorpWindows library with specified configuration.
        
        Args:
            timeout: Default timeout for waiting operations in seconds (default: 10)
            retry_interval: Interval between retries in seconds (default: 0.5)
            log_level: Log level ('TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR') (default: INFO)
        """
        self.timeout = timestr_to_secs(timeout)
        self.retry_interval = timestr_to_secs(retry_interval)
        self.app = None
        self.current_window = None
        self.cache = ConnectionCache()
        
        # Initialize logger with specified log level
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level.upper())
        self.log_level = log_level.upper()
        
        self.builtin = BuiltIn()
        self.builtin.log(f"RobocorpWindows Library initialized with log level: {self.log_level}", level='DEBUG')
        
        # Initialize keyword modules
        self.window_management = WindowManagementKeywords(self)
        self.control_operations = ControlOperationsKeywords(self)
        self.keyboard_mouse = KeyboardMouseKeywords(self)
        self.async_control_operations = AsyncControlOperationsKeywords(self)
    
    # 直接重新暴露关键字方法，确保Robot Framework能检测到它们
    
    # 窗口管理关键字
    @keyword
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
        return self.window_management.launch_application(app_path, timeout)
    
    @keyword
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
        return self.window_management.connect_to_application(title, class_name, process, timeout)
    
    @keyword
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
        return self.window_management.set_current_window(title, class_name, timeout)
    
    @keyword
    def close_application(self):
        """Close the currently connected application.
        
        Examples:
        | Close Application |
        """
        return self.window_management.close_application()
    
    @keyword
    def minimize_window(self):
        """Minimize the current window.
        
        Examples:
        | Minimize Window |
        """
        return self.window_management.minimize_window()
    
    @keyword
    def maximize_window(self):
        """Maximize the current window.
        
        Examples:
        | Maximize Window |
        """
        return self.window_management.maximize_window()
    
    @keyword
    def restore_window(self):
        """Restore the current window from minimized or maximized state.
        
        Examples:
        | Restore Window |
        """
        return self.window_management.restore_window()
    
    @keyword
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
        return self.window_management.window_should_be_open(title, class_name, timeout)
    
    @keyword
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
        return self.window_management.window_should_be_closed(title, class_name, timeout)
    
    @keyword
    def get_window_title(self):
        """Get the title of the current window.
        
        Returns:
            str: Title of the current window
            
        Examples:
        | ${title} | Get Window Title |
        | Should Contain | ${title} | Notepad |
        """
        return self.window_management.get_window_title()
    
    # 控件操作关键字
    @keyword
    def find_control(self, control_identifier, timeout=None):
        """Find a control in the current window.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Returns:
            Control: The found control object
            
        Examples:
        | ${control} | Find Control | Edit |
        | ${control} | Find Control | name=OKButton | timeout=5 |
        """
        return self.control_operations.find_control(control_identifier, timeout)
    
    @keyword
    def click_control(self, control_identifier, timeout=None):
        """Click on a control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Click Control | OKButton |
        | Click Control | name=SubmitButton | timeout=5 |
        """
        return self.control_operations.click_control(control_identifier, timeout)
    
    @keyword
    def double_click_control(self, control_identifier, timeout=None):
        """Double click on a control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Double Click Control | FileIcon |
        | Double Click Control | name=DocumentFile | timeout=5 |
        """
        return self.control_operations.double_click_control(control_identifier, timeout)
    
    @keyword
    def right_click_control(self, control_identifier, timeout=None):
        """Right click on a control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Right Click Control | FileIcon |
        | Right Click Control | name=ContextMenuButton | timeout=5 |
        """
        return self.control_operations.right_click_control(control_identifier, timeout)
    
    @keyword
    def type_into_control(self, control_identifier, text, timeout=None):
        """Type text into a control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            text: Text to type into the control
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Type Into Control | Edit | Hello, Robot Framework! |
        | Type Into Control | name=UsernameField | admin | timeout=5 |
        """
        return self.control_operations.type_into_control(control_identifier, text, timeout)
    
    @keyword
    def get_control_text(self, control_identifier, timeout=None):
        """Get text from a control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Returns:
            str: Text from the control
            
        Examples:
        | ${text} | Get Control Text | Edit |
        | ${text} | Get Control Text | name=StatusLabel | timeout=5 |
        """
        return self.control_operations.get_control_text(control_identifier, timeout)
    
    @keyword
    def control_should_exist(self, control_identifier, timeout=None):
        """Verify that a control exists.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Control Should Exist | OKButton |
        | Control Should Exist | name=SubmitButton | timeout=5 |
        """
        return self.control_operations.control_should_exist(control_identifier, timeout)
    
    @keyword
    def control_should_not_exist(self, control_identifier, timeout=None):
        """Verify that a control does not exist.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is not available (default: library timeout)
            
        Examples:
        | Control Should Not Exist | ErrorDialog |
        | Control Should Not Exist | name=LoadingSpinner | timeout=5 |
        """
        return self.control_operations.control_should_not_exist(control_identifier, timeout)
    
    @keyword
    def set_control_value(self, control_identifier, value, timeout=None):
        """Set the value of a control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            value: Value to set for the control
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Set Control Value | UsernameField | admin |
        | Set Control Value | name=PasswordField | secret | timeout=5 |
        """
        return self.control_operations.set_control_value(control_identifier, value, timeout)
    
    @keyword
    def get_control_value(self, control_identifier, timeout=None):
        """Get the value of a control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Returns:
            str: Value of the control
            
        Examples:
        | ${value} | Get Control Value | UsernameField |
        | ${value} | Get Control Value | name=ComboBox | timeout=5 |
        """
        return self.control_operations.get_control_value(control_identifier, timeout)
    
    @keyword
    def select_from_combobox(self, control_identifier, item, timeout=None):
        """Select an item from a combobox control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            item: Item to select from the combobox
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Select From Combobox | CountryComboBox | United States |
        | Select From Combobox | name=LanguageComboBox | English | timeout=5 |
        """
        return self.control_operations.select_from_combobox(control_identifier, item, timeout)
    
    @keyword
    def check_checkbox(self, control_identifier, timeout=None):
        """Check a checkbox control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Check Checkbox | AcceptTermsCheckbox |
        | Check Checkbox | name=EnableFeatureCheckbox | timeout=5 |
        """
        return self.control_operations.check_checkbox(control_identifier, timeout)
    
    @keyword
    def uncheck_checkbox(self, control_identifier, timeout=None):
        """Uncheck a checkbox control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Uncheck Checkbox | AcceptTermsCheckbox |
        | Uncheck Checkbox | name=EnableFeatureCheckbox | timeout=5 |
        """
        return self.control_operations.uncheck_checkbox(control_identifier, timeout)
    
    @keyword
    def checkbox_should_be_checked(self, control_identifier, timeout=None):
        """Verify that a checkbox is checked.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Checkbox Should Be Checked | AcceptTermsCheckbox |
        | Checkbox Should Be Checked | name=EnableFeatureCheckbox | timeout=5 |
        """
        return self.control_operations.checkbox_should_be_checked(control_identifier, timeout)
    
    @keyword
    def checkbox_should_be_unchecked(self, control_identifier, timeout=None):
        """Verify that a checkbox is unchecked.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Checkbox Should Be Unchecked | AcceptTermsCheckbox |
        | Checkbox Should Be Unchecked | name=EnableFeatureCheckbox | timeout=5 |
        """
        return self.control_operations.checkbox_should_be_unchecked(control_identifier, timeout)
    
    def _get_application(self):
        """Get the current application instance.
        
        Returns:
            Application: The current robocorp-windows Application instance
            
        Raises:
            ApplicationNotConnectedError: If no application is connected or launched
        """
        if not self.app:
            raise ApplicationNotConnectedError("No application connected. Use 'Launch Application' or 'Connect To Application' first.")
        return self.app
        
    def _get_current_window(self):
        """Get the current window instance.
        
        Returns:
            Window: The current window instance
            
        Raises:
            NoActiveWindowError: If no window is active
        """
        if not self.current_window:
            raise NoActiveWindowError("No active window. Use 'Set Current Window' or 'Launch Application' first.")
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
            condition: Callable that returns a truthy value when the condition is met
            timeout: Maximum time to wait in seconds
            retry_interval: Interval between retries in seconds
            
        Returns:
            The result of the condition function if it was met, None otherwise
        """
        timeout = timeout or self.timeout
        retry_interval = retry_interval or self.retry_interval
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            result = condition()
            if result:
                return result
            time.sleep(retry_interval)
        return None
    
    # 异步控件操作关键字
    @keyword("Async Type Into Control")
    def async_type_into_control(self, control_identifier, text, timeout=None):
        """异步向控件输入文本
        
        Args:
            control_identifier: 控件标识符
            text: 要输入的文本
            timeout: 超时时间（秒）
            
        Returns:
            str: 任务ID，可用于后续查询结果
            
        Examples:
        | ${task_id} | Async Type Into Control | name=LargeTextArea | ${long_text} |
        | # 执行其他操作 |
        | Wait For Async Task | ${task_id} |
        """
        return self.async_control_operations.async_type_into_control(control_identifier, text, timeout)
    
    @keyword("Async Find All Controls")
    def async_find_all_controls(self, control_identifier, timeout=None):
        """异步查找所有匹配的控件
        
        Args:
            control_identifier: 控件标识符
            timeout: 超时时间（秒）
            
        Returns:
            str: 任务ID，可用于后续查询结果
            
        Examples:
        | ${task_id} | Async Find All Controls | name=ListBoxItem |
        | ${controls} | Wait For Async Task | ${task_id} |
        | Log | Found ${len(controls)} controls |
        """
        return self.async_control_operations.async_find_all_controls(control_identifier, timeout)
    
    @keyword("Wait For Async Task")
    def wait_for_async_task(self, task_id, timeout=None):
        """等待异步任务完成并返回结果
        
        Args:
            task_id: 异步任务的ID
            timeout: 等待超时时间（秒），如果为None则使用默认超时
            
        Returns:
            Any: 异步任务的返回结果
            
        Examples:
        | ${task_id} | Async Type Into Control | name=LargeTextArea | ${long_text} |
        | ${result} | Wait For Async Task | ${task_id} | timeout=30 |
        | Log | ${result} |
        """
        return self.async_control_operations.wait_for_async_task(task_id, timeout)
    
    @keyword("Async Click Control")
    def async_click_control(self, control_identifier, timeout=None):
        """异步点击控件
        
        Args:
            control_identifier: 控件标识符
            timeout: 超时时间（秒）
            
        Returns:
            str: 任务ID，可用于后续查询结果
            
        Examples:
        | ${task_id} | Async Click Control | name=LongRunningButton |
        | Wait For Async Task | ${task_id} |
        """
        return self.async_control_operations.async_click_control(control_identifier, timeout)
    
    @keyword("Shutdown Async Executor")
    def shutdown_async_executor(self, wait=True):
        """关闭异步执行器
        
        Args:
            wait: 是否等待所有任务完成后关闭（默认：True）
            
        Examples:
        | Shutdown Async Executor |
        | Shutdown Async Executor | wait=False |
        """
        return self.async_control_operations.shutdown_async_executor(wait)