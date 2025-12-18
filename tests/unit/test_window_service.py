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

# Now import our library components
from robotframework_robocorp_windows.services.window_service import WindowService
from robotframework_robocorp_windows.drivers.robocorp_driver import RobocorpWindowsDriver
from robotframework_robocorp_windows.utils.exceptions import WindowNotFoundError

class TestWindowService(unittest.TestCase):
    """Unit tests for WindowService"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a mock driver
        self.mock_driver = Mock(spec=RobocorpWindowsDriver)
        self.window_service = WindowService(self.mock_driver)
    
    def test_launch_application_success(self):
        """Test launch_application with successful window find"""
        # Mock driver methods
        self.mock_driver.launch_application.return_value = "notepad.exe"
        self.mock_driver.find_window_by_executable.return_value = Mock()
        self.mock_driver.get_window_title.return_value = "Notepad"
        
        # Call the method
        executable_name, window = self.window_service.launch_application("notepad.exe")
        
        # Verify
        self.assertEqual(executable_name, "notepad.exe")
        self.assertIsNotNone(window)
        self.mock_driver.launch_application.assert_called_once_with("notepad.exe")
        self.mock_driver.find_window_by_executable.assert_called_once()
    
    def test_launch_application_window_not_found(self):
        """Test launch_application when window is not found"""
        # Mock driver methods
        self.mock_driver.launch_application.return_value = "notepad.exe"
        self.mock_driver.find_window_by_executable.side_effect = WindowNotFoundError("Window not found")
        
        # Call the method
        executable_name, window = self.window_service.launch_application("notepad.exe")
        
        # Verify
        self.assertEqual(executable_name, "notepad.exe")
        self.assertIsNone(window)
        self.mock_driver.launch_application.assert_called_once_with("notepad.exe")
    
    def test_connect_to_application_with_title(self):
        """Test connect_to_application with title"""
        # Mock driver methods
        mock_window = Mock()
        self.mock_driver.find_window_by_locator.return_value = mock_window
        
        # Call the method
        locator, window = self.window_service.connect_to_application(title="TestApp")
        
        # Verify
        self.assertEqual(locator, "name:TestApp")
        self.assertEqual(window, mock_window)
        self.mock_driver.find_window_by_locator.assert_called_once_with("name:TestApp", 10)
    
    def test_connect_to_application_with_class_name(self):
        """Test connect_to_application with class name"""
        # Mock driver methods
        mock_window = Mock()
        self.mock_driver.find_window_by_locator.return_value = mock_window
        
        # Call the method
        locator, window = self.window_service.connect_to_application(class_name="TestClass")
        
        # Verify
        self.assertEqual(locator, "class:TestClass")
        self.assertEqual(window, mock_window)
        self.mock_driver.find_window_by_locator.assert_called_once_with("class:TestClass", 10)
    
    def test_connect_to_application_with_process(self):
        """Test connect_to_application with process"""
        # Mock driver methods
        mock_window = Mock()
        self.mock_driver.find_window_by_locator.return_value = mock_window
        
        # Call the method
        locator, window = self.window_service.connect_to_application(process=1234)
        
        # Verify
        self.assertEqual(locator, "pid:1234")
        self.assertEqual(window, mock_window)
        self.mock_driver.find_window_by_locator.assert_called_once_with("pid:1234", 10)
    
    def test_connect_to_application_without_locator(self):
        """Test connect_to_application without any locator"""
        # Call the method and expect ValueError
        with self.assertRaises(ValueError):
            self.window_service.connect_to_application()
    
    def test_set_current_window_with_title(self):
        """Test set_current_window with title"""
        # Mock driver methods
        mock_window = Mock()
        self.mock_driver.find_window_by_locator.return_value = mock_window
        
        # Call the method
        window = self.window_service.set_current_window(title="TestApp")
        
        # Verify
        self.assertEqual(window, mock_window)
        self.mock_driver.find_window_by_locator.assert_called_once_with("name:TestApp", 10)
    
    def test_set_current_window_without_locator(self):
        """Test set_current_window without any locator"""
        # Mock driver methods
        mock_window = Mock()
        self.mock_driver.find_window_by_locator.return_value = mock_window
        
        # Call the method
        window = self.window_service.set_current_window()
        
        # Verify
        self.assertEqual(window, mock_window)
        self.mock_driver.find_window_by_locator.assert_called_once_with("regex:.*", 10)
    
    def test_window_should_be_open_with_locator(self):
        """Test window_should_be_open with locator"""
        # Mock driver methods
        self.mock_driver.get_window_by_locator.return_value = Mock()
        
        # Call the method (should not raise)
        self.window_service.window_should_be_open(title="TestApp", timeout=1)
        
        # Verify
        self.mock_driver.get_window_by_locator.assert_called()
    
    def test_window_should_be_open_with_current_window(self):
        """Test window_should_be_open with current window"""
        # Mock driver methods
        mock_window = Mock()
        self.mock_driver.window_exists.return_value = True
        
        # Call the method (should not raise)
        self.window_service.window_should_be_open(current_window=mock_window, timeout=1)
        
        # Verify
        self.mock_driver.window_exists.assert_called_once_with(mock_window)
    
    def test_window_should_be_closed_with_locator(self):
        """Test window_should_be_closed with locator"""
        # Mock driver methods
        self.mock_driver.get_window_by_locator.return_value = None
        
        # Call the method (should not raise)
        self.window_service.window_should_be_closed(title="TestApp", timeout=1)
        
        # Verify
        self.mock_driver.get_window_by_locator.assert_called()
    
    def test_window_should_be_closed_with_current_window(self):
        """Test window_should_be_closed with current window"""
        # Mock driver methods
        mock_window = Mock()
        self.mock_driver.window_exists.return_value = False
        
        # Call the method (should not raise)
        self.window_service.window_should_be_closed(current_window=mock_window, timeout=1)
        
        # Verify
        self.mock_driver.window_exists.assert_called_once_with(mock_window)

if __name__ == '__main__':
    unittest.main()
