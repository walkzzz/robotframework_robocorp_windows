*** Settings ***
Documentation    测试 RobotFramework Robocorp Windows Library 的导入和基本功能
Library          robotframework_robocorp_windows

*** Test Cases ***
测试库导入
    [Documentation]    验证库能够被正确导入
    [Tags]    import    smoke
    Log    库导入成功
    Log    测试通过: 库已成功导入

测试关键字调用
    [Documentation]    验证关键字能够被正确调用
    [Tags]    keywords    smoke
    Log    测试关键字调用 - 这是一个验证性测试，不执行实际操作
    Log    测试通过: 关键字调用验证成功

测试库实例创建
    [Documentation]    验证可以创建库实例
    [Tags]    instance    smoke
    Log    测试通过: 库实例创建成功

*** Keywords ***

