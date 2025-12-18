*** Settings ***
Library    test_basic_library.py

*** Test Cases ***
Hello World Test
    [Documentation]    Test the Hello World keyword
    
    ${result}    Hello World
    Log    ${result}
    Should Be Equal    ${result}    Hello, World!

Add Numbers Test
    [Documentation]    Test the Add Numbers keyword
    
    ${result}    Add Numbers    2    3
    Log    ${result}
    Should Be Equal    ${result}    5