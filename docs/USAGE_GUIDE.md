# Robocorp Windows Library - Usage Guide

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Library Configuration](#library-configuration)
4. [Window Management](#window-management)
5. [Control Operations](#control-operations)
6. [Keyboard & Mouse Operations](#keyboard--mouse-operations)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## 1. Installation

### Prerequisites

- Python 3.8 or later
- Robot Framework 4.0 or later
- Windows 10 or Windows 11

### Installing the Library

You can install the library using pip:

```bash
pip install robotframework-robocorp-windows
```

Or, if you're installing from the source code:

```bash
cd robotframework-robocorp-windows
pip install -e .
```

## 2. Basic Usage

### Importing the Library

To use the library in your Robot Framework test cases, import it in the Settings section:

```robotframework
*** Settings ***
Library    RobocorpWindows
```

### Example Test Case

```robotframework
*** Settings ***
Library    RobocorpWindows

*** Test Cases ***
Example Test
    Launch Application    notepad.exe
    Type Into Control    Edit    Hello, Robot Framework!
    Close Application
```

## 3. Library Configuration

The library can be configured with the following parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| timeout | 10 | Default timeout for waiting operations in seconds |
| retry_interval | 0.5 | Interval between retries in seconds |

### Example Configuration

```robotframework
*** Settings ***
Library    RobocorpWindows    timeout=15    retry_interval=1.0
```

## 4. Window Management

### Launching Applications

```robotframework
Launch Application    notepad.exe
${app_id}    Launch Application    C:\\Program Files\\MyApp\\myapp.exe    timeout=5
```

### Connecting to Running Applications

```robotframework
Connect To Application    title=Notepad
Connect To Application    process=${PID}
Connect To Application    title=MyApp    class_name=MyAppMainWindow
```

### Window Operations

```robotframework
Set Current Window    title=Untitled - Notepad
Minimize Window
Maximize Window
Restore Window
Close Application
```

### Window Verification

```robotframework
Window Should Be Open    title=Untitled - Notepad
Window Should Be Closed    title=DialogBox
${title}    Get Window Title
```

## 5. Control Operations

### Finding Controls

```robotframework
${control}    Find Control    Edit
${control}    Find Control    name=OKButton    timeout=5
```

### Clicking Controls

```robotframework
Click Control    OKButton
Double Click Control    FileIcon
Right Click Control    ContextMenuButton
```

### Text Operations

```robotframework
Type Into Control    Edit    Hello, World!
${text}    Get Control Text    StatusLabel
```

### Control Verification

```robotframework
Control Should Exist    OKButton
Control Should Not Exist    ErrorDialog
```

### Advanced Control Operations

```robotframework
Set Control Value    UsernameField    admin
${value}    Get Control Value    ComboBox
Select From Combobox    CountryComboBox    United States

Check Checkbox    AcceptTermsCheckbox
Uncheck Checkbox    EnableFeatureCheckbox

Checkbox Should Be Checked    AcceptTermsCheckbox
Checkbox Should Be Unchecked    EnableFeatureCheckbox
```

## 6. Keyboard & Mouse Operations

### Keyboard Operations

```robotframework
Press Keys    ENTER
Press Keys    CTRL    C
Press Keys    WIN    R

Type Text    Hello, World!
Type Text    Password123    delay=0.1

Press And Hold Keys    SHIFT
Release Keys    SHIFT

Type Special Key    TAB
Type Special Key    ESC
```

### Mouse Operations

```robotframework
Mouse Move To    100    200
Mouse Click
Mouse Click    150    250
Mouse Click    button=right

Mouse Double Click
Mouse Right Click

Scroll Mouse Wheel    10    # Scroll up
Scroll Mouse Wheel    -5    # Scroll down
Scroll Mouse Wheel    3    100    200    # Scroll at specific position
```

## 7. Best Practices

### 7.1 Timeout Handling

- Always set appropriate timeouts for operations that might take longer
- Use the `timeout` parameter for individual keywords when needed
- Avoid using `Sleep` unless absolutely necessary

### 7.2 Control Identification

- Use unique and stable control identifiers
- Prefer using control names or IDs over coordinates
- Use `Control Should Exist` to verify controls before interacting with them

### 7.3 Error Handling

- Use `Run Keyword And Expect Error` for expected error scenarios
- Implement proper cleanup in `Teardown` sections
- Log important information using `Log` keyword

### 7.4 Test Organization

- Organize tests by functionality
- Use tags to categorize tests
- Implement reusable keywords for common operations

### 7.5 Performance Considerations

- Minimize the number of operations
- Use `Control Should Exist` instead of multiple `Find Control` calls
- Close applications properly to free up resources

## 8. Troubleshooting

### Common Issues

#### 1. Application Not Found

**Symptom**: `Launch Application` fails with "Application not found" error

**Solution**: 
- Verify the application path is correct
- Check if the application requires administrative privileges
- Ensure the application is installed on the system

#### 2. Control Not Found

**Symptom**: `Find Control` or other control operations fail with "Control not found" error

**Solution**:
- Verify the control identifier is correct
- Use a more specific control identifier
- Increase the timeout value
- Check if the control is in a different window

#### 3. Application Not Responding

**Symptom**: Tests hang or take too long to execute

**Solution**:
- Check if the application is responsive
- Increase the timeout value
- Add appropriate delays between operations
- Verify the application is not waiting for user input

#### 4. Permission Issues

**Symptom**: Operations fail with "Permission denied" or similar errors

**Solution**:
- Run the test with administrative privileges
- Check if the application requires special permissions
- Verify file and directory permissions

### Debugging Tips

1. **Enable Debug Logging**:
   ```robotframework
   *** Settings ***
   Library    RobocorpWindows
   
   *** Test Cases ***
   Debug Test
       Log Level    DEBUG
       # Your test steps here
   ```

2. **Use `Get Window Title` to verify the active window**

3. **Use `Control Should Exist` to check control availability**

4. **Add temporary `Sleep` statements to see what's happening**

5. **Check the Robot Framework log file for detailed information**

## 9. Examples

For more examples, see the `examples/` directory in the library source code.

## 10. API Reference

For a complete list of keywords and their documentation, see the [API Reference](API_REFERENCE.md).
