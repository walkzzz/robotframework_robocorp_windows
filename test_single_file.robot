*** Settings ***
Library    robotframework_robocorp_windows

*** Test Cases ***
Simple Library Test
    [Documentation]    Test the single file library
    
    # This test just verifies that the library can be loaded
    Log    Library loaded successfully!