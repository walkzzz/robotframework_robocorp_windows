*** Settings ***
Library    RobocorpWindows    timeout=10    retry_interval=0.5
Documentation    Example test case for calculator application
...    This test demonstrates complex control operations and menu navigation
...    using the Windows Calculator application.

*** Test Cases ***
Example: Calculator Basic Operations
    [Documentation]    Test basic calculator operations
    [Tags]    example    calculator    basic
    
    # Launch Calculator application
    Launch Application    calc.exe
    
    # Wait for the calculator window to open
    Window Should Be Open    title=Calculator
    
    # Test basic arithmetic operations
    # 2 + 3 = 5
    Click Control    name=num2Button
    Click Control    name=plusButton
    Click Control    name=num3Button
    Click Control    name=equalsButton
    
    # Verify the result
    ${result}    Get Control Text    name=CalculatorResults
    Should Contain    ${result}    5
    
    # 5 - 1 = 4
    Click Control    name=minusButton
    Click Control    name=num1Button
    Click Control    name=equalsButton
    
    # Verify the result
    ${result}    Get Control Text    name=CalculatorResults
    Should Contain    ${result}    4
    
    # Close the calculator
    Close Application
    
    # Verify the application is closed
    Sleep    1

Example: Calculator Advanced Operations
    [Documentation]    Test advanced calculator operations
    [Tags]    example    calculator    advanced
    
    # Launch Calculator application
    Launch Application    calc.exe
    
    # Wait for the calculator window to open
    Window Should Be Open    title=Calculator
    
    # Switch to Scientific mode using menu
    Click Control    name=TogglePaneButton
    Click Control    name=ScientificCalculatorMenuItem
    
    # Wait for scientific mode to load
    Sleep    1
    
    # Test scientific operations: sin(30) = 0.5
    Click Control    name=num3Button
    Click Control    name=num0Button
    Click Control    name=sinnButton
    
    # Verify the result
    ${result}    Get Control Text    name=CalculatorResults
    Should Contain    ${result}    0.5
    
    # Switch back to Standard mode
    Click Control    name=TogglePaneButton
    Click Control    name=StandardCalculatorMenuItem
    
    # Close the calculator
    Close Application
    
    # Verify the application is closed
    Sleep    1

Example: Calculator Memory Operations
    [Documentation]    Test calculator memory operations
    [Tags]    example    calculator    memory
    
    # Launch Calculator application
    Launch Application    calc.exe
    
    # Wait for the calculator window to open
    Window Should Be Open    title=Calculator
    
    # Test memory operations
    # Store 10 in memory
    Click Control    name=num1Button
    Click Control    name=num0Button
    Click Control    name=memoryStoreButton
    
    # Clear the display
    Click Control    name=clearButton
    
    # Recall from memory and verify
    Click Control    name=memoryRecallButton
    ${result}    Get Control Text    name=CalculatorResults
    Should Contain    ${result}    10
    
    # Add 5 to memory (10 + 5 = 15)
    Click Control    name=plusButton
    Click Control    name=num5Button
    Click Control    name=memoryAddButton
    
    # Recall from memory and verify the new value
    Click Control    name=memoryRecallButton
    ${result}    Get Control Text    name=CalculatorResults
    Should Contain    ${result}    15
    
    # Clear memory
    Click Control    name=memoryClearButton
    
    # Recall from memory and verify it's clear
    Click Control    name=memoryRecallButton
    ${result}    Get Control Text    name=CalculatorResults
    Should Contain    ${result}    0
    
    # Close the calculator
    Close Application
    
    # Verify the application is closed
    Sleep    1
