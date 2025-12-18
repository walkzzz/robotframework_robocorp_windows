from robot.api.deco import keyword, library

@library
class BasicLibrary:
    """A basic Robot Framework library."""
    
    ROBOT_LIBRARY_VERSION = '1.0.0'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self):
        """Initialize the library."""
        pass
    
    @keyword
    def hello_world(self):
        """Print Hello, World!"""
        print("Hello, World!")
        return "Hello, World!"
    
    @keyword
    def add_numbers(self, a, b):
        """Add two numbers."""
        return int(a) + int(b)