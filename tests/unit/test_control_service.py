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
    
    class WindowElement:
        """Mock WindowElement"""
        def __init__(self):
            self.name = "Mock Window"
            self.text = "Mock Window Text"
            self.close_window = Mock()
            self.minimize_window = Mock()
            self.maximize_window = Mock()
            self.restore_window = Mock()
            self.exists = Mock(return_value=True)
    
    class ControlElement:
        """Mock ControlElement"""
        def __init__(self):
            self.text = "Mock Control"
            self.click = Mock()
            self.double_click = Mock()
            self.right_click = Mock()
            self.type = Mock()
            self.set_value = Mock()
            self.get_value = Mock(return_value="Mock Value")
            self.select = Mock()
            self.check = Mock()
            self.uncheck = Mock()
            self.is_checked = Mock(return_value=False)
    
    @staticmethod
    def desktop():
        """Mock desktop function"""
        mock_desktop = Mock()
        mock_desktop.find_window = Mock(return_value=MockRobocorpModule.WindowElement())
        return mock_desktop
    
    @staticmethod
    def find_window(locator, raise_error=True, **kwargs):
        """Mock find_window function"""
        if raise_error:
            return MockRobocorpModule.WindowElement()
        return MockRobocorpModule.WindowElement()
    
    @staticmethod
    def find_windows(locator, **kwargs):
        """Mock find_windows function"""
        return [MockRobocorpModule.WindowElement()]

# Create a mock robocorp module
mock_robocorp = MockRobocorpModule()
mock_robocorp.windows = mock_robocorp

# Add to sys.modules to intercept imports
sys.modules['robocorp'] = mock_robocorp
sys.modules['robocorp.windows'] = mock_robocorp
sys.modules['robocorp.windows.ElementNotFound'] = MockRobocorpModule.ElementNotFound

# Now import our library components
from robotframework_robocorp_windows.services.control_service import ControlService
from robotframework_robocorp_windows.drivers.robocorp_driver import RobocorpWindowsDriver
from robotframework_robocorp_windows.utils.exceptions import ControlNotFoundError, ControlOperationException

class TestControlService(unittest.TestCase):
    """Unit tests for ControlService"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a mock driver
        self.mock_driver = Mock(spec=RobocorpWindowsDriver)
        self.control_service = ControlService(self.mock_driver)
        
        # Create mock window and control
        self.mock_window = Mock()
        self.mock_control = MockRobocorpModule.ControlElement()
    
    def test_find_control_with_cache(self):
        """Test find_control with cache enabled"""
        # Mock driver methods
        self.mock_driver.find_control.return_value = self.mock_control
        
        # Call the method twice (second call should use cache)
        control1 = self.control_service.find_control(self.mock_window, "Button")
        control2 = self.control_service.find_control(self.mock_window, "Button")
        
        # Verify
        self.assertEqual(control1, self.mock_control)
        self.assertEqual(control2, self.mock_control)
        # Driver should be called only once
        self.mock_driver.find_control.assert_called_once()
    
    def test_find_control_without_cache(self):
        """Test find_control with cache disabled"""
        # Mock driver methods
        self.mock_driver.find_control.return_value = self.mock_control
        
        # Disable cache
        self.control_service.disable_cache()
        
        # Call the method twice (both calls should use driver)
        control1 = self.control_service.find_control(self.mock_window, "Button")
        control2 = self.control_service.find_control(self.mock_window, "Button")
        
        # Verify
        self.assertEqual(control1, self.mock_control)
        self.assertEqual(control2, self.mock_control)
        # Driver should be called twice
        self.assertEqual(self.mock_driver.find_control.call_count, 2)
    
    def test_find_control_with_use_cache_false(self):
        """Test find_control with use_cache=False"""
        # Mock driver methods
        self.mock_driver.find_control.return_value = self.mock_control
        
        # Call the method with use_cache=False
        control = self.control_service.find_control(self.mock_window, "Button", use_cache=False)
        
        # Verify
        self.assertEqual(control, self.mock_control)
        self.mock_driver.find_control.assert_called_once()
    
    def test_cache_control_disable_enable(self):
        """Test disabling and enabling cache"""
        # Verify cache is enabled by default
        self.assertTrue(self.control_service.is_cache_enabled())
        
        # Disable cache
        self.control_service.disable_cache()
        self.assertFalse(self.control_service.is_cache_enabled())
        
        # Enable cache
        self.control_service.enable_cache()
        self.assertTrue(self.control_service.is_cache_enabled())
    
    def test_clear_cache(self):
        """Test clear_cache method"""
        # Mock driver methods
        self.mock_driver.find_control.return_value = self.mock_control
        
        # Call find_control to populate cache
        self.control_service.find_control(self.mock_window, "Button")
        
        # Clear cache
        self.control_service.clear_cache()
        
        # Call find_control again (should use driver again)
        self.control_service.find_control(self.mock_window, "Button")
        
        # Verify driver was called twice (once before clear, once after)
        self.assertEqual(self.mock_driver.find_control.call_count, 2)
    
    def test_click_control(self):
        """Test click_control method"""
        # Call the method
        self.control_service.click_control(self.mock_control)
        
        # Verify
        self.mock_control.click.assert_called_once()
    
    def test_double_click_control(self):
        """Test double_click_control method"""
        # Call the method
        self.control_service.double_click_control(self.mock_control)
        
        # Verify
        self.mock_control.double_click.assert_called_once()
    
    def test_right_click_control(self):
        """Test right_click_control method"""
        # Call the method
        self.control_service.right_click_control(self.mock_control)
        
        # Verify
        self.mock_control.right_click.assert_called_once()
    
    def test_type_into_control(self):
        """Test type_into_control method"""
        # Call the method
        self.control_service.type_into_control(self.mock_control, "Test Text")
        
        # Verify
        self.mock_control.type.assert_called_once_with("Test Text")
    
    def test_get_control_text(self):
        """Test get_control_text method"""
        # Call the method
        text = self.control_service.get_control_text(self.mock_control)
        
        # Verify
        self.assertEqual(text, "Mock Control")
    
    def test_set_control_value(self):
        """Test set_control_value method"""
        # Call the method
        self.control_service.set_control_value(self.mock_control, "New Value")
        
        # Verify
        self.mock_control.set_value.assert_called_once_with("New Value")
    
    def test_get_control_value(self):
        """Test get_control_value method"""
        # Call the method
        value = self.control_service.get_control_value(self.mock_control)
        
        # Verify
        self.assertEqual(value, "Mock Value")
        self.mock_control.get_value.assert_called_once()
    
    def test_select_from_combobox(self):
        """Test select_from_combobox method"""
        # Call the method
        self.control_service.select_from_combobox(self.mock_control, "Item1")
        
        # Verify
        self.mock_control.select.assert_called_once_with("Item1")
    
    def test_check_checkbox(self):
        """Test check_checkbox method"""
        # Call the method
        self.control_service.check_checkbox(self.mock_control)
        
        # Verify
        self.mock_control.check.assert_called_once()
    
    def test_uncheck_checkbox(self):
        """Test uncheck_checkbox method"""
        # Call the method
        self.control_service.uncheck_checkbox(self.mock_control)
        
        # Verify
        self.mock_control.uncheck.assert_called_once()
    
    def test_is_checkbox_checked(self):
        """Test is_checkbox_checked method"""
        # Call the method
        result = self.control_service.is_checkbox_checked(self.mock_control)
        
        # Verify
        self.assertFalse(result)
        self.mock_control.is_checked.assert_called_once()
    
    def test_control_should_exist(self):
        """Test control_should_exist method"""
        # Mock driver methods
        self.mock_driver.find_control.return_value = self.mock_control
        
        # Call the method (should not raise)
        self.control_service.control_should_exist(self.mock_window, "Button", timeout=1)
        
        # Verify
        self.mock_driver.find_control.assert_called()
    
    def test_control_should_exist_not_found(self):
        """Test control_should_exist when control is not found"""
        # Mock driver methods
        self.mock_driver.find_control.side_effect = ControlNotFoundError("Control not found")
        
        # Call the method and expect AssertionError
        with self.assertRaises(AssertionError):
            self.control_service.control_should_exist(self.mock_window, "NonExistentControl", timeout=1)
    
    def test_control_should_not_exist(self):
        """Test control_should_not_exist method"""
        # Mock driver methods
        self.mock_driver.find_control.side_effect = ControlNotFoundError("Control not found")
        
        # Call the method (should not raise)
        self.control_service.control_should_not_exist(self.mock_window, "NonExistentControl", timeout=1)
        
        # Verify
        self.mock_driver.find_control.assert_called()
    
    def test_control_should_not_exist_found(self):
        """Test control_should_not_exist when control is found"""
        # Mock driver methods
        self.mock_driver.find_control.return_value = self.mock_control
        
        # Call the method and expect AssertionError
        with self.assertRaises(AssertionError):
            self.control_service.control_should_not_exist(self.mock_window, "ExistingControl", timeout=1)
    
    def test_control_operations_with_exception(self):
        """Test control operations when they raise exceptions"""
        # Mock control methods to raise exceptions
        self.mock_control.click.side_effect = Exception("Click failed")
        self.mock_control.double_click.side_effect = Exception("Double click failed")
        
        # Test click_control
        with self.assertRaises(ControlOperationException):
            self.control_service.click_control(self.mock_control)
        
        # Test double_click_control
        with self.assertRaises(ControlOperationException):
            self.control_service.double_click_control(self.mock_control)

if __name__ == '__main__':
    unittest.main()
