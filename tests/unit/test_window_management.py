import unittest
import subprocess
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
            self.find = Mock()
            self.text = "Mock Window"
    
    # Mock ControlElement class
    class ControlElement:
        """Mock ControlElement"""
        def __init__(self):
            self.text = "Mock Control"
            self.click = Mock()
            self.type = Mock()
    
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
from robotframework_robocorp_windows.keywords.window_management import WindowManagementKeywords

class TestWindowManagementKeywords(unittest.TestCase):
    """Unit tests for WindowManagementKeywords"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a mock library instance
        self.mock_library = Mock()
        self.mock_library.timeout = 5
        self.mock_library.retry_interval = 0.5
        self.mock_library.app = None
        self.mock_library.current_window = None
        self.mock_library.cache = Mock()
        self.mock_library.cache.register = Mock(return_value="app_123")
        self.mock_library._log = Mock()
        self.mock_library._wait_until = Mock()
        
        # Create the keyword instance
        self.window_management = WindowManagementKeywords(self.mock_library)
    
    def test_launch_application(self):
        """Test launch_application keyword"""
        # Mock subprocess.Popen
        mock_process = Mock()
        mock_process.pid = 123
        
        # Mock find_windows function
        mock_window = Mock()
        mock_window.name = "Test Application"
        
        with patch('subprocess.Popen', return_value=mock_process) as mock_popen, \
             patch('robotframework_robocorp_windows.keywords.window_management.find_windows', return_value=[mock_window]) as mock_find_windows:
            # Mock _wait_until to return our mock window
            self.mock_library._wait_until = Mock(return_value=mock_window)
            # Mock cache.register to return a dummy app_id
            self.mock_library.cache.register = Mock(return_value="app_123")
            
            result = self.window_management.launch_application("test.exe")
            
            # Verify the result
            self.assertEqual(result, "app_123")
            mock_popen.assert_called_once_with("test.exe")
            self.mock_library._log.assert_called()
    
    def test_connect_to_application(self):
        """Test connect_to_application keyword"""
        # Mock the find_window function
        mock_window = Mock()
        mock_window.name = "Connected App"
        mock_window.close_window = Mock()
        
        # Mock cache.register to return a dummy app_id
        self.mock_library.cache.register = Mock(return_value="app_123")
        # Mock _wait_until to return our mock window
        self.mock_library._wait_until = Mock(return_value=mock_window)
        
        result = self.window_management.connect_to_application(title="TestApp")
        
        # Verify the result
        self.assertEqual(result, "app_123")
        self.assertEqual(self.mock_library.current_window, mock_window)
        self.mock_library._log.assert_called()
    
    def test_set_current_window(self):
        """Test set_current_window keyword"""
        # Mock the application and window
        mock_window = Mock()
        mock_window.title = "Test Window"
        mock_window.exists = Mock(return_value=True)
        
        mock_app = Mock()
        mock_app.window = Mock(return_value=mock_window)
        mock_app.top_window = Mock(return_value=mock_window)
        
        self.mock_library.app = mock_app
        self.mock_library._wait_until = Mock(return_value=mock_window)
        
        # Call the method
        self.window_management.set_current_window(title="Test")
        
        # Verify
        self.assertEqual(self.mock_library.current_window, mock_window)
        self.mock_library._log.assert_called()
    
    def test_close_application(self):
        """Test close_application keyword"""
        # Mock the current window
        mock_window = Mock()
        mock_window.name = "Test Window"
        mock_window.close_window = Mock()
        self.mock_library.current_window = mock_window
        
        # Call the method
        self.window_management.close_application()
        
        # Verify
        mock_window.close_window.assert_called_once()
        self.assertIsNone(self.mock_library.current_window)
        self.mock_library._log.assert_called()
    
    def test_minimize_window(self):
        """Test minimize_window keyword"""
        # Mock the current window
        mock_window = Mock()
        mock_window.name = "Test Window"
        mock_window.minimize_window = Mock()
        self.mock_library.current_window = mock_window
        self.mock_library._get_current_window = Mock(return_value=mock_window)
        
        # Call the method
        self.window_management.minimize_window()
        
        # Verify
        mock_window.minimize_window.assert_called_once()
        self.mock_library._log.assert_called()
    
    def test_maximize_window(self):
        """Test maximize_window keyword"""
        # Mock the current window
        mock_window = Mock()
        mock_window.name = "Test Window"
        mock_window.maximize_window = Mock()
        self.mock_library._get_current_window = Mock(return_value=mock_window)
        
        # Call the method
        self.window_management.maximize_window()
        
        # Verify
        mock_window.maximize_window.assert_called_once()
        self.mock_library._log.assert_called()
    
    def test_restore_window(self):
        """Test restore_window keyword"""
        # Mock the current window
        mock_window = Mock()
        mock_window.name = "Test Window"
        mock_window.restore_window = Mock()
        self.mock_library._get_current_window = Mock(return_value=mock_window)
        
        # Call the method
        self.window_management.restore_window()
        
        # Verify
        mock_window.restore_window.assert_called_once()
        self.mock_library._log.assert_called()
    
    def test_window_should_be_open(self):
        """Test window_should_be_open keyword"""
        # Mock the library methods
        mock_window = Mock()
        mock_window.exists = Mock(return_value=True)
        self.mock_library.current_window = mock_window
        self.mock_library._get_application = Mock(return_value=Mock())
        self.mock_library._wait_until = Mock(return_value=True)
        
        # Call the method
        self.window_management.window_should_be_open(title="Test")
        
        # Verify
        self.mock_library._wait_until.assert_called()
        self.mock_library._log.assert_called()
    
    def test_window_should_be_closed(self):
        """Test window_should_be_closed keyword"""
        # Mock the library methods
        self.mock_library._get_application = Mock(return_value=Mock())
        self.mock_library._wait_until = Mock(return_value=True)
        
        # Call the method
        self.window_management.window_should_be_closed(title="Test")
        
        # Verify
        self.mock_library._wait_until.assert_called()
        self.mock_library._log.assert_called()
    
    def test_get_window_title(self):
        """Test get_window_title keyword"""
        # Mock the current window
        mock_window = Mock()
        mock_window.name = "Test Window"
        self.mock_library._get_current_window = Mock(return_value=mock_window)
        
        # Call the method
        result = self.window_management.get_window_title()
        
        # Verify
        self.assertEqual(result, "Test Window")
        self.mock_library._log.assert_called()
