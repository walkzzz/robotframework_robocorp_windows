import unittest
from robotframework_robocorp_windows.utils.locator_utils import LocatorUtils, locator_utils

class TestLocatorUtils(unittest.TestCase):
    """Unit tests for LocatorUtils"""
    
    def test_validate_valid_locator_with_strategy(self):
        """Test validating a valid locator with strategy"""
        # Test with various valid strategies
        valid_locators = [
            "name:OKButton",
            "id:12345",
            "class:Edit",
            "text:Hello, World!",
            "xpath://div[@id='container']/button",
            "index:0",
            "executable:notepad.exe"
        ]
        
        for locator in valid_locators:
            with self.subTest(locator=locator):
                is_valid, message = locator_utils.validate_locator(locator)
                self.assertTrue(is_valid, f"Locator should be valid: {locator}")
                self.assertIn("Valid", message)
    
    def test_validate_valid_locator_without_strategy(self):
        """Test validating a valid locator without strategy (default name)"""
        locator = "OKButton"
        is_valid, message = locator_utils.validate_locator(locator)
        self.assertTrue(is_valid)
        self.assertIn("default 'name' strategy", message)
    
    def test_validate_invalid_locator_invalid_strategy(self):
        """Test validating an invalid locator with invalid strategy"""
        locator = "invalid:Button"
        is_valid, message = locator_utils.validate_locator(locator)
        self.assertFalse(is_valid)
        self.assertIn("Invalid locator strategy", message)
    
    def test_validate_invalid_locator_empty(self):
        """Test validating an empty locator"""
        locator = ""
        is_valid, message = locator_utils.validate_locator(locator)
        self.assertFalse(is_valid)
        self.assertIn("cannot be empty", message)
    
    def test_validate_invalid_locator_non_string(self):
        """Test validating a non-string locator"""
        invalid_locators = [123, None, [], {}]
        for locator in invalid_locators:
            with self.subTest(locator=locator):
                is_valid, message = locator_utils.validate_locator(locator)
                self.assertFalse(is_valid)
                self.assertIn("must be a string", message)
    
    def test_validate_locator_format(self):
        """Test validate_locator_format method"""
        # Test valid locator
        valid_locator = "name:OKButton"
        result = locator_utils.validate_locator_format(valid_locator)
        self.assertIn("Valid", result)
        
        # Test invalid locator
        invalid_locator = "invalid:Button"
        with self.assertRaises(ValueError) as context:
            locator_utils.validate_locator_format(invalid_locator)
        self.assertIn("Invalid locator strategy", str(context.exception))
    
    def test_get_locator_strategy(self):
        """Test get_locator_strategy method"""
        # Test with strategy prefix
        locator = "xpath://div[@id='container']"
        strategy, value = locator_utils.get_locator_strategy(locator)
        self.assertEqual(strategy, "xpath")
        self.assertEqual(value, "//div[@id='container']")
        
        # Test without strategy prefix (default name)
        locator = "Button"
        strategy, value = locator_utils.get_locator_strategy(locator)
        self.assertEqual(strategy, "name")
        self.assertEqual(value, "Button")
    
    def test_format_locator(self):
        """Test format_locator method"""
        strategy = "name"
        value = "OKButton"
        formatted_locator = locator_utils.format_locator(strategy, value)
        self.assertEqual(formatted_locator, "name:OKButton")
        
        # Test with invalid strategy
        invalid_strategy = "invalid_strategy"
        with self.assertRaises(ValueError) as context:
            locator_utils.format_locator(invalid_strategy, value)
        self.assertIn("Invalid locator strategy", str(context.exception))
    
    def test_get_supported_strategies(self):
        """Test get_supported_strategies method"""
        strategies = locator_utils.get_supported_strategies()
        self.assertIsInstance(strategies, list)
        self.assertIn("name", strategies)
        self.assertIn("id", strategies)
        self.assertIn("xpath", strategies)
        self.assertIn("executable", strategies)
    
    def test_get_valid_locator_examples(self):
        """Test get_valid_locator_examples method"""
        examples = locator_utils.get_valid_locator_examples()
        self.assertIsInstance(examples, list)
        self.assertGreater(len(examples), 0)
        for example in examples:
            self.assertIsInstance(example, str)
            is_valid, _ = locator_utils.validate_locator(example)
            self.assertTrue(is_valid, f"Example should be valid: {example}")

if __name__ == '__main__':
    unittest.main()
