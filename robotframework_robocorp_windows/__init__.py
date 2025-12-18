# -*- coding: utf-8 -*-
"""
Robot Framework library for Windows automation using robocorp-windows.
"""

# Import the library class directly
from .library import RobocorpWindows

# Robot Framework looks for this variable to identify the library class
ROBOT_LIBRARY_CLASS = RobocorpWindows

# These are the keywords that will be available to Robot Framework
# Robot Framework will look for these attributes in the module
# and use them as keywords.

# Import keyword modules
from .keywords.window_management import WindowManagementKeywords
from .keywords.control_operations import ControlOperationsKeywords
from .keywords.keyboard_mouse import KeyboardMouseKeywords

# Create an instance of the library to get access to the keywords
_lib = RobocorpWindows()

# List all the keywords we want to expose
keywords = [
    'launch_application', 'connect_to_application', 'set_current_window',
    'close_application', 'minimize_window', 'maximize_window', 'restore_window',
    'window_should_be_open', 'window_should_be_closed', 'get_window_title',
    'find_control', 'click_control', 'double_click_control', 'right_click_control',
    'type_into_control', 'get_control_text', 'control_should_exist',
    'control_should_not_exist', 'set_control_value', 'get_control_value',
    'select_from_combobox', 'check_checkbox', 'uncheck_checkbox',
    'checkbox_should_be_checked', 'checkbox_should_be_unchecked'
]

# Expose the keywords as module attributes
for keyword in keywords:
    if hasattr(_lib, keyword):
        globals()[keyword] = getattr(_lib, keyword)

__version__ = '1.0.0'
__all__ = ['RobocorpWindows'] + keywords
