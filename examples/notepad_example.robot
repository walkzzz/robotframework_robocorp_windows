*** Settings ***
Library    RobocorpWindows    timeout=10    retry_interval=0.5
Documentation    Example test case for Robocorp Windows Library
...    This test demonstrates basic Windows automation using the library
...    with Notepad application.

*** Test Cases ***
Example: Notepad Automation
    [Documentation]    Example test case that automates Notepad
    [Tags]    example    notepad
    
    # Launch Notepad application
    Launch Application    notepad.exe
    
    # Wait for the window to open
    Window Should Be Open    title=Untitled - Notepad
    
    # Get the window title
    ${title}    Get Window Title
    Should Contain    ${title}    Untitled - Notepad
    
    # Type into the edit control
    Type Into Control    Edit    Hello, Robot Framework!
    Type Into Control    Edit    \nThis is an example of using Robocorp Windows Library.
    
    # Get the text from the edit control and verify it
    ${text}    Get Control Text    Edit
    Should Contain    ${text}    Hello, Robot Framework!
    Should Contain    ${text}    Robocorp Windows Library
    
    # Maximize the window
    Maximize Window
    Sleep    1
    
    # Minimize the window
    Minimize Window
    Sleep    1
    
    # Restore the window
    Restore Window
    Sleep    1
    
    # Close the application
    Close Application
    
    # Verify the application is closed
    Sleep    1

*** Keywords ***
# This section can contain custom keywords specific to this test suite
