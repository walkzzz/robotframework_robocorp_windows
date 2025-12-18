from robot.api.deco import keyword
from ..services.control_service import ControlService
from ..utils.exceptions import (
    WindowNotFoundError,
    ControlNotFoundError,
    ControlOperationException
)

class ControlOperationsKeywords:
    """Keywords for control operations."""
    
    def __init__(self, library):
        """Initialize ControlOperationsKeywords with the main library instance."""
        self.library = library
        self.logger = library.logger
        self.builtin = library.builtin
        self.control_service = ControlService()
        self.control_service.set_logger(self.logger)
        
    @keyword("Find Control")
    def find_control(self, control_identifier, timeout=None, use_cache=True):
        """Find a control in the current window.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Control: The found control object
            
        Examples:
        | ${control} | Find Control | Edit |
        | ${control} | Find Control | name=OKButton | timeout=5 |
        | ${control} | Find Control | name=RefreshButton | use_cache=False |
        """
        timeout = timeout or self.library.timeout
        window = self.library._get_current_window()
        
        try:
            control = self.control_service.find_control(window, control_identifier, timeout, use_cache)
            self.library._log(f"Found control: {control_identifier}")
            return control
        except ControlNotFoundError as e:
            raise AssertionError(str(e))
    
    @keyword("Find Control Without Cache")
    def find_control_without_cache(self, control_identifier, timeout=None):
        """Find a control in the current window without using cache.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Returns:
            Control: The found control object
            
        Examples:
        | ${control} | Find Control Without Cache | Edit |
        | ${control} | Find Control Without Cache | name=OKButton | timeout=5 |
        """
        return self.find_control(control_identifier, timeout, use_cache=False)
    
    @keyword("Click Control")
    def click_control(self, control_identifier, timeout=None):
        """Click on a control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Click Control | OKButton |
        | Click Control | name=SubmitButton | timeout=5 |
        """
        control = self.find_control(control_identifier, timeout)
        self.library._log(f"Clicking control: {control_identifier}")
        self.control_service.click_control(control)
    
    @keyword("Double Click Control")
    def double_click_control(self, control_identifier, timeout=None):
        """Double click on a control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Double Click Control | FileIcon |
        | Double Click Control | name=DocumentFile | timeout=5 |
        """
        control = self.find_control(control_identifier, timeout)
        self.library._log(f"Double clicking control: {control_identifier}")
        self.control_service.double_click_control(control)
    
    @keyword("Right Click Control")
    def right_click_control(self, control_identifier, timeout=None):
        """Right click on a control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Right Click Control | FileIcon |
        | Right Click Control | name=ContextMenuButton | timeout=5 |
        """
        control = self.find_control(control_identifier, timeout)
        self.library._log(f"Right clicking control: {control_identifier}")
        self.control_service.right_click_control(control)
    
    @keyword("Type Into Control")
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
        control = self.find_control(control_identifier, timeout)
        self.library._log(f"Typing into control: {control_identifier}, text: {text}")
        self.control_service.type_into_control(control, text)
    
    @keyword("Get Control Text")
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
        control = self.find_control(control_identifier, timeout)
        text = self.control_service.get_control_text(control)
        self.library._log(f"Got text from control {control_identifier}: {text}")
        return text
    
    @keyword("Control Should Exist")
    def control_should_exist(self, control_identifier, timeout=None):
        """Verify that a control exists.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Control Should Exist | OKButton |
        | Control Should Exist | name=SubmitButton | timeout=5 |
        """
        timeout = timeout or self.library.timeout
        window = self.library._get_current_window()
        
        self.control_service.control_should_exist(window, control_identifier, timeout)
        self.library._log(f"Control exists: {control_identifier}")
    
    @keyword("Control Should Not Exist")
    def control_should_not_exist(self, control_identifier, timeout=None):
        """Verify that a control does not exist.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is not available (default: library timeout)
            
        Examples:
        | Control Should Not Exist | ErrorDialog |
        | Control Should Not Exist | name=LoadingSpinner | timeout=5 |
        """
        timeout = timeout or self.library.timeout
        window = self.library._get_current_window()
        
        self.control_service.control_should_not_exist(window, control_identifier, timeout)
        self.library._log(f"Control does not exist: {control_identifier}")
    
    @keyword("Set Control Value")
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
        control = self.find_control(control_identifier, timeout)
        self.library._log(f"Setting control value: {control_identifier} = {value}")
        self.control_service.set_control_value(control, value)
    
    @keyword("Get Control Value")
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
        control = self.find_control(control_identifier, timeout)
        value = self.control_service.get_control_value(control)
        self.library._log(f"Got control value: {control_identifier} = {value}")
        return value
    
    @keyword("Select From Combobox")
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
        control = self.find_control(control_identifier, timeout)
        self.library._log(f"Selecting from combobox {control_identifier}: {item}")
        self.control_service.select_from_combobox(control, item)
    
    @keyword("Check Checkbox")
    def check_checkbox(self, control_identifier, timeout=None):
        """Check a checkbox control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Check Checkbox | AcceptTermsCheckbox |
        | Check Checkbox | name=EnableFeatureCheckbox | timeout=5 |
        """
        control = self.find_control(control_identifier, timeout)
        self.library._log(f"Checking checkbox: {control_identifier}")
        self.control_service.check_checkbox(control)
    
    @keyword("Uncheck Checkbox")
    def uncheck_checkbox(self, control_identifier, timeout=None):
        """Uncheck a checkbox control.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Uncheck Checkbox | AcceptTermsCheckbox |
        | Uncheck Checkbox | name=EnableFeatureCheckbox | timeout=5 |
        """
        control = self.find_control(control_identifier, timeout)
        self.library._log(f"Unchecking checkbox: {control_identifier}")
        self.control_service.uncheck_checkbox(control)
    
    @keyword("Checkbox Should Be Checked")
    def checkbox_should_be_checked(self, control_identifier, timeout=None):
        """Verify that a checkbox is checked.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Checkbox Should Be Checked | AcceptTermsCheckbox |
        | Checkbox Should Be Checked | name=EnableFeatureCheckbox | timeout=5 |
        """
        control = self.find_control(control_identifier, timeout)
        if not self.control_service.is_checkbox_checked(control):
            raise AssertionError(f"Checkbox should be checked but was not: {control_identifier}")
        
        self.library._log(f"Checkbox is checked: {control_identifier}")
    
    @keyword("Checkbox Should Be Unchecked")
    def checkbox_should_be_unchecked(self, control_identifier, timeout=None):
        """Verify that a checkbox is unchecked.
        
        Args:
            control_identifier: Control identifier (name, id, class name, or other criteria)
            timeout: Timeout for waiting until the control is available (default: library timeout)
            
        Examples:
        | Checkbox Should Be Unchecked | AcceptTermsCheckbox |
        | Checkbox Should Be Unchecked | name=EnableFeatureCheckbox | timeout=5 |
        """
        control = self.find_control(control_identifier, timeout)
        if self.control_service.is_checkbox_checked(control):
            raise AssertionError(f"Checkbox should be unchecked but was checked: {control_identifier}")
        
        self.library._log(f"Checkbox is unchecked: {control_identifier}")