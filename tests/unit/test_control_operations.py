import unittest
from unittest.mock import Mock, patch
import sys

# Mock the entire robocorp module at the sys.modules level
class MockRobocorpModule:
    """Mock robocorp module"""
    # Mock classes and functions used in robocorp-windows 1.0.0
    class ElementNotFound(Exception):
        """Mock ElementNotFound"""
        pass
    
    # Mock WindowElement class
    class WindowElement:
        """Mock WindowElement"""
        def __init__(self):
            self.name = "Mock Window"
            self.text = "Mock Window Text"
            self.click = Mock()
            self.close_window = Mock()
            self.minimize_window = Mock()
            self.maximize_window = Mock()
            self.restore_window = Mock()
            self.find = Mock(return_value=MockRobocorpModule.ControlElement())
            self.text = "Mock Window"
    
    # Mock ControlElement class
    class ControlElement:
        """Mock ControlElement"""
        def __init__(self):
            self.text = "Mock Control"
            self.click = Mock()
            self.double_click = Mock()
            self.right_click = Mock()
            self.type = Mock()
            self.get_text = Mock(return_value="Mock Control Text")
            self.set_value = Mock()
            self.get_value = Mock(return_value="Mock Value")
            self.check = Mock()
            self.uncheck = Mock()
            self.is_checked = Mock(return_value=False)
    
    # Mock desktop function
    @staticmethod
    def desktop():
        """Mock desktop function"""
        mock_desktop = Mock()
        mock_desktop.find_window = Mock(return_value=MockRobocorpModule.WindowElement())
        mock_desktop.find_windows = Mock(return_value=[MockRobocorpModule.WindowElement()])
        return mock_desktop
    
    # Mock find_window function
    @staticmethod
    def find_window(locator, raise_error=True, **kwargs):
        """Mock find_window function"""
        if raise_error:
            return MockRobocorpModule.WindowElement()
        return None
    
    # Mock find_windows function
    @staticmethod
    def find_windows(locator, **kwargs):
        """Mock find_windows function"""
        return [MockRobocorpModule.WindowElement()]
    
    # Mock keyboard module (currently not used in our code)
    class keyboard:
        """Mock keyboard module"""
        press = Mock()
        type = Mock()
        press_and_hold = Mock()
        release = Mock()
    
    # Mock mouse module (currently not used in our code)
    class mouse:
        """Mock mouse module"""
        move = Mock()
        click = Mock()
        double_click = Mock()
        scroll = Mock()

# Create a mock robocorp module
mock_robocorp = MockRobocorpModule()
mock_robocorp.windows = mock_robocorp

# Add to sys.modules to intercept imports
sys.modules['robocorp'] = mock_robocorp
sys.modules['robocorp.windows'] = mock_robocorp

# Now import our library components
from robotframework_robocorp_windows.keywords.control_operations import ControlOperationsKeywords

class TestControlOperationsKeywords(unittest.TestCase):
    """Unit tests for ControlOperationsKeywords"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a mock library instance
        self.mock_library = Mock()
        self.mock_library.timeout = 5
        self.mock_library.retry_interval = 0.5
        self.mock_library.app = Mock()
        self.mock_library.current_window = MockRobocorpModule.WindowElement()
        self.mock_library._log = Mock()
        self.mock_library._wait_until = Mock()
        self.mock_library._get_current_window = Mock(return_value=self.mock_library.current_window)
        
        # Create the keyword instance
        self.control_operations = ControlOperationsKeywords(self.mock_library)
    
    def test_find_control(self):
        """Test find_control keyword"""
        # Mock the window.find method
        mock_control = MockRobocorpModule.ControlElement()
        self.mock_library.current_window.find = Mock(return_value=mock_control)
        self.mock_library._wait_until = Mock(return_value=mock_control)
        
        # Call the method
        result = self.control_operations.find_control("Edit")
        
        # Verify
        self.assertEqual(result, mock_control)
        self.mock_library._log.assert_called()
    
    def test_click_control(self):
        """Test click_control keyword"""
        # Mock the find_control method
        mock_control = MockRobocorpModule.ControlElement()
        self.control_operations.find_control = Mock(return_value=mock_control)
        
        # Call the method
        self.control_operations.click_control("OKButton")
        
        # Verify
        mock_control.click.assert_called_once()
        self.mock_library._log.assert_called()
    
    def test_double_click_control(self):
        """Test double_click_control keyword"""
        # Mock the find_control method
        mock_control = MockRobocorpModule.ControlElement()
        self.control_operations.find_control = Mock(return_value=mock_control)

        # Call the method
        self.control_operations.double_click_control("FileIcon")

        # Verify
        mock_control.double_click.assert_called_once()
        self.mock_library._log.assert_called()
    
    def test_right_click_control(self):
        """Test right_click_control keyword"""
        # Mock the find_control method
        mock_control = MockRobocorpModule.ControlElement()
        self.control_operations.find_control = Mock(return_value=mock_control)

        # Call the method
        self.control_operations.right_click_control("ContextMenu")

        # Verify
        mock_control.right_click.assert_called_once()
        self.mock_library._log.assert_called()
    
    def test_type_into_control(self):
        """Test type_into_control keyword"""
        # Mock the find_control method
        mock_control = MockRobocorpModule.ControlElement()
        self.control_operations.find_control = Mock(return_value=mock_control)
        
        # Call the method
        self.control_operations.type_into_control("Edit", "Hello, World!")
        
        # Verify
        mock_control.type.assert_called_once_with("Hello, World!")
        self.mock_library._log.assert_called()
    
    def test_get_control_text(self):
        """Test get_control_text keyword"""
        # Mock the find_control method
        mock_control = MockRobocorpModule.ControlElement()
        mock_control.text = "Test Text"
        self.control_operations.find_control = Mock(return_value=mock_control)
        
        # Call the method
        result = self.control_operations.get_control_text("Edit")
        
        # Verify
        self.assertEqual(result, "Test Text")
        self.mock_library._log.assert_called()
    
    def test_control_should_exist(self):
        """Test control_should_exist keyword"""
        # Mock the find_control method
        mock_control = MockRobocorpModule.ControlElement()
        self.control_operations.find_control = Mock(return_value=mock_control)
        
        # Call the method
        self.control_operations.control_should_exist("Edit")
        
        # Verify
        self.mock_library._log.assert_called()
    
    def test_control_should_not_exist(self):
        """Test control_should_not_exist keyword"""
        # Mock the window.find method to raise an exception
        self.mock_library.current_window.find = Mock(side_effect=Exception())
        self.mock_library._wait_until = Mock(return_value=True)
        
        # Call the method
        self.control_operations.control_should_not_exist("NonExistentControl")
        
        # Verify
        self.mock_library._log.assert_called()
    
    def test_set_control_value(self):
        """Test set_control_value keyword"""
        # Mock the find_control method
        mock_control = MockRobocorpModule.ControlElement()
        self.control_operations.find_control = Mock(return_value=mock_control)
        
        # Call the method
        self.control_operations.set_control_value("Edit", "New Value")
        
        # Verify
        mock_control.set_value.assert_called_once_with("New Value")
        self.mock_library._log.assert_called()
    
    def test_get_control_value(self):
        """Test get_control_value keyword"""
        # Mock the find_control method
        mock_control = MockRobocorpModule.ControlElement()
        mock_control.get_value = Mock(return_value="Current Value")
        self.control_operations.find_control = Mock(return_value=mock_control)
        
        # Call the method
        result = self.control_operations.get_control_value("Edit")
        
        # Verify
        self.assertEqual(result, "Current Value")
        self.mock_library._log.assert_called()
    
    def test_check_checkbox(self):
        """Test check_checkbox keyword"""
        # Mock the find_control method
        mock_control = MockRobocorpModule.ControlElement()
        self.control_operations.find_control = Mock(return_value=mock_control)
        
        # Call the method
        self.control_operations.check_checkbox("Checkbox")
        
        # Verify
        mock_control.check.assert_called_once()
        self.mock_library._log.assert_called()
    
    def test_uncheck_checkbox(self):
        """Test uncheck_checkbox keyword"""
        # Mock the find_control method
        mock_control = MockRobocorpModule.ControlElement()
        self.control_operations.find_control = Mock(return_value=mock_control)
        
        # Call the method
        self.control_operations.uncheck_checkbox("Checkbox")
        
        # Verify
        mock_control.uncheck.assert_called_once()
        self.mock_library._log.assert_called()
    
    def test_checkbox_should_be_checked(self):
        """Test checkbox_should_be_checked keyword"""
        # Mock the find_control method
        mock_control = MockRobocorpModule.ControlElement()
        mock_control.is_checked = Mock(return_value=True)
        self.control_operations.find_control = Mock(return_value=mock_control)
        
        # Call the method
        self.control_operations.checkbox_should_be_checked("Checkbox")
        
        # Verify
        mock_control.is_checked.assert_called_once()
        self.mock_library._log.assert_called()
    
    def test_checkbox_should_be_unchecked(self):
        """Test checkbox_should_be_unchecked keyword"""
        # Mock the find_control method
        mock_control = MockRobocorpModule.ControlElement()
        mock_control.is_checked = Mock(return_value=False)
        self.control_operations.find_control = Mock(return_value=mock_control)
        
        # Call the method
        self.control_operations.checkbox_should_be_unchecked("Checkbox")
        
        # Verify
        mock_control.is_checked.assert_called_once()
        self.mock_library._log.assert_called()