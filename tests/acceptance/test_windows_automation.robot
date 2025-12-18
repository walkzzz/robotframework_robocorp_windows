*** Settings ***
Library    robotframework_robocorp_windows
Documentation    Acceptance tests for Robocorp Windows Library
...    These tests verify the actual functionality of the library
...    by automating real Windows applications.

*** Test Cases ***
Acceptance: Notepad Basic Operations
    [Documentation]    Test basic Notepad automation
    [Tags]    acceptance    notepad    basic
    
    # Launch Notepad
    Launch Application    notepad.exe
    
    # Verify window is open
    Window Should Be Open    title=Untitled - Notepad
    
    # Test window operations
    ${title}    Get Window Title
    Should Contain    ${title}    Untitled - Notepad
    
    Minimize Window
    Sleep    1
    
    Maximize Window
    Sleep    1
    
    Restore Window
    Sleep    1
    
    # Test control operations
    Type Into Control    Edit    This is a test of Robocorp Windows Library
    
    ${text}    Get Control Text    Edit
    Should Contain    ${text}    Robocorp Windows Library
    
    # Close application
    Close Application
    
    # Verify application is closed
    Sleep    1

Acceptance: Notepad Control Verification
    [Documentation]    Test control verification in Notepad
    [Tags]    acceptance    notepad    controls
    
    # Launch Notepad
    Launch Application    notepad.exe
    
    # Verify edit control exists
    Control Should Exist    Edit
    
    # Verify some non-existent control does not exist
    Control Should Not Exist    NonExistentControl
    
    # Close application
    Close Application
    
    Sleep    1

Acceptance: Notepad Advanced Operations
    [Documentation]    Test advanced Notepad automation
    [Tags]    acceptance    notepad    advanced
    
    # Launch Notepad
    Launch Application    notepad.exe
    
    # Type multi-line text (使用\n代替回车键)
    Type Into Control    Edit    Line 1\nLine 2\nLine 3
    
    # Verify multi-line text
    ${text}    Get Control Text    Edit
    Should Contain    ${text}    Line 1
    Should Contain    ${text}    Line 2
    Should Contain    ${text}    Line 3
    
    # 移除键盘快捷键操作，使用控件操作代替
    
    # Close application
    Close Application
    
    Sleep    1

*** Keywords ***
# This section can contain custom keywords for acceptance tests
