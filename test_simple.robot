*** Settings ***
Library    robotframework_robocorp_windows

*** Test Cases ***
Simple Test
    [Documentation]    A simple test to verify library loading
    
    # 这个测试只是验证库是否能被正确加载，不执行实际操作
    Log    Library loaded successfully!
    Log    Available keywords: ${\n}${get_keyword_names()}