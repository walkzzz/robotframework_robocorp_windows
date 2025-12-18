import unittest
from unittest.mock import Mock, patch, MagicMock
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

# Now import our library
from robotframework_robocorp_windows.library import RobocorpWindows

class TestRobocorpWindowsLibrary(unittest.TestCase):
    """Unit tests for RobocorpWindows library"""
    
    def setUp(self):
        """Set up test fixtures"""
        # No need for additional patches as we've already mocked robocorp.windows at the module level
        pass
    
    def tearDown(self):
        """Clean up test fixtures"""
        # No need for cleanup as we've already mocked robocorp.windows at the module level
        pass
    
    def test_library_initialization(self):
        """Test that the library initializes correctly"""
        library = RobocorpWindows()
        self.assertIsInstance(library, RobocorpWindows)
        self.assertEqual(library.timeout, 10)
        self.assertEqual(library.retry_interval, 0.5)
        self.assertIsNone(library.app)
        self.assertIsNone(library.current_window)
    
    def test_library_initialization_with_custom_timeout(self):
        """Test that the library initializes correctly with custom timeout"""
        library = RobocorpWindows(timeout=5)
        self.assertEqual(library.timeout, 5)
    
    def test_library_initialization_with_custom_retry_interval(self):
        """Test that the library initializes correctly with custom retry interval"""
        library = RobocorpWindows(retry_interval=1)
        self.assertEqual(library.retry_interval, 1)
    
    def test_library_initialization_with_custom_values(self):
        """Test that the library initializes correctly with custom values"""
        library = RobocorpWindows(timeout=7, retry_interval=0.2)
        self.assertEqual(library.timeout, 7)
        self.assertEqual(library.retry_interval, 0.2)
    
    def test_keyword_modules_initialized(self):
        """Test that keyword modules are initialized"""
        library = RobocorpWindows()
        self.assertTrue(hasattr(library, 'window_management'))
        self.assertTrue(hasattr(library, 'control_operations'))
        self.assertTrue(hasattr(library, 'keyboard_mouse'))
    
    @patch('robotframework_robocorp_windows.library.WindowManagementKeywords')
    @patch('robotframework_robocorp_windows.library.ControlOperationsKeywords')
    @patch('robotframework_robocorp_windows.library.KeyboardMouseKeywords')
    def test_keyword_modules_instantiated(self, mock_keyboard_mouse, mock_control_ops, mock_window_management):
        """Test that keyword modules are instantiated correctly"""
        RobocorpWindows()
        
        # Check that each keyword module was instantiated
        mock_window_management.assert_called_once()
        mock_control_ops.assert_called_once()
        mock_keyboard_mouse.assert_called_once()
    
    def test_get_application_without_app(self):
        """Test that get_application raises RuntimeError when no app is connected"""
        library = RobocorpWindows()
        with self.assertRaises(RuntimeError) as context:
            library._get_application()
        self.assertIn("No application connected", str(context.exception))
    
    def test_get_current_window_without_window(self):
        """Test that get_current_window raises RuntimeError when no window is active"""
        library = RobocorpWindows()
        with self.assertRaises(RuntimeError) as context:
            library._get_current_window()
        self.assertIn("No active window", str(context.exception))
    
    def test_wait_until_condition_true(self):
        """Test that wait_until returns True when condition becomes true"""
        library = RobocorpWindows(timeout=1, retry_interval=0.1)
        
        # Mock condition that returns True immediately
        def condition():
            return True
        
        result = library._wait_until(condition)
        self.assertTrue(result)
    
    def test_wait_until_condition_false(self):
        """Test that wait_until returns False when condition remains false"""
        library = RobocorpWindows(timeout=0.5, retry_interval=0.1)
        
        # Mock condition that returns False always
        def condition():
            return False
        
        result = library._wait_until(condition)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
