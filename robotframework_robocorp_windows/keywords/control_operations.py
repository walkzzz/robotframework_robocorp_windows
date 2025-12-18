from robot.api.deco import keyword
from robocorp.windows import ElementNotFound

class ControlOperationsKeywords:
    """Keywords for control operations."""
    
    def __init__(self, library):
        """Initialize ControlOperationsKeywords with the main library instance."""
        self.library = library
        self.logger = library.logger
        self.builtin = library.builtin
        
    @keyword("Find Control")
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
        timeout = timeout or self.library.timeout
        window = self.library._get_current_window()
        
        def find_control_func():
            try:
                control = window.find(control_identifier)
                return control
            except Exception:
                return None
        
        control = self.library._wait_until(find_control_func, timeout)
        if not control:
            raise ElementNotFound(f"Control not found: {control_identifier}")
        
        self.library._log(f"Found control: {control_identifier}")
        return control
    
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
        control.click()
    
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
        control.double_click()
    
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
        control.right_click()
    
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
        control.type(text)
    
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
        text = control.text
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
        try:
            self.find_control(control_identifier, timeout)
            self.library._log(f"Control exists: {control_identifier}")
        except ElementNotFound:
            raise AssertionError(f"Control should exist but was not found: {control_identifier}")
    
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
        window = self.library._get_current_window()
        timeout = timeout or self.library.timeout
        
        def control_not_exists():
            try:
                window.find(control_identifier)
                return False
            except Exception:
                return True
        
        if not self.library._wait_until(control_not_exists, timeout):
            raise AssertionError(f"Control should not exist but was found: {control_identifier}")
        
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
        control.set_value(value)
    
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
        value = control.get_value()
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
        control.select(item)
    
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
        control.check()
    
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
        control.uncheck()
    
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
        if not control.is_checked():
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
        if control.is_checked():
            raise AssertionError(f"Checkbox should be unchecked but was checked: {control_identifier}")
        
        self.library._log(f"Checkbox is unchecked: {control_identifier}")