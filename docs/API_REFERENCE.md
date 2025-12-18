# Robocorp Windows Library - API Reference

This document provides detailed documentation for all keywords available in the Robocorp Windows Library.

## Table of Contents

1. [Window Management Keywords](#window-management-keywords)
2. [Control Operations Keywords](#control-operations-keywords)
3. [Keyboard & Mouse Keywords](#keyboard--mouse-keywords)

## 1. Window Management Keywords

### Launch Application

**Launch a Windows application and connect to it.**

**Arguments:**
- `app_path`: Path to the application executable
- `timeout`: Timeout for waiting until the application is ready (default: library timeout)

**Returns:**
- `str`: Application identifier that can be used with other keywords

**Examples:**
```robotframework
Launch Application    notepad.exe
${app_id}    Launch Application    C:/Program Files/MyApp/myapp.exe    timeout=5
```

### Connect To Application

**Connect to an already running application.**

**Arguments:**
- `title`: Window title or partial title to match (optional)
- `class_name`: Window class name to match (optional)
- `process`: Process ID to connect to (optional)
- `timeout`: Timeout for waiting until the application is ready (default: library timeout)

**Returns:**
- `str`: Application identifier that can be used with other keywords

**Examples:**
```robotframework
Connect To Application    title=Notepad
Connect To Application    process=${PID}
Connect To Application    title=MyApp    class_name=MyAppMainWindow
```

### Set Current Window

**Set the current active window.**

**Arguments:**
- `title`: Window title or partial title to match (optional)
- `class_name`: Window class name to match (optional)
- `timeout`: Timeout for waiting until the window is available (default: library timeout)

**Examples:**
```robotframework
Set Current Window    title=Untitled - Notepad
Set Current Window    title=MyApp    class_name=MyAppMainWindow
```

### Close Application

**Close the currently connected application.**

**Examples:**
```robotframework
Close Application
```

### Minimize Window

**Minimize the current window.**

**Examples:**
```robotframework
Minimize Window
```

### Maximize Window

**Maximize the current window.**

**Examples:**
```robotframework
Maximize Window
```

### Restore Window

**Restore the current window from minimized or maximized state.**

**Examples:**
```robotframework
Restore Window
```

### Window Should Be Open

**Verify that a window is open.**

**Arguments:**
- `title`: Window title or partial title to match (optional)
- `class_name`: Window class name to match (optional)
- `timeout`: Timeout for waiting until the window is available (default: library timeout)

**Examples:**
```robotframework
Window Should Be Open    title=Untitled - Notepad
Window Should Be Open    title=MyApp    class_name=MyAppMainWindow    timeout=5
```

### Window Should Be Closed

**Verify that a window is closed.**

**Arguments:**
- `title`: Window title or partial title to match (optional)
- `class_name`: Window class name to match (optional)
- `timeout`: Timeout for waiting until the window is closed (default: library timeout)

**Examples:**
```robotframework
Window Should Be Closed    title=Notepad
Window Should Be Closed    title=MyApp    class_name=MyAppDialog    timeout=5
```

### Get Window Title

**Get the title of the current window.**

**Returns:**
- `str`: Title of the current window

**Examples:**
```robotframework
${title}    Get Window Title
Should Contain    ${title}    Notepad
```

## 2. Control Operations Keywords

### Find Control

**Find a control in the current window.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Returns:**
- `Control`: The found control object

**Examples:**
```robotframework
${control}    Find Control    Edit
${control}    Find Control    name=OKButton    timeout=5
```

### Click Control

**Click on a control.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Examples:**
```robotframework
Click Control    OKButton
Click Control    name=SubmitButton    timeout=5
```

### Double Click Control

**Double click on a control.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Examples:**
```robotframework
Double Click Control    FileIcon
Double Click Control    name=DocumentFile    timeout=5
```

### Right Click Control

**Right click on a control.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Examples:**
```robotframework
Right Click Control    FileIcon
Right Click Control    name=ContextMenuButton    timeout=5
```

### Type Into Control

**Type text into a control.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `text`: Text to type into the control
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Examples:**
```robotframework
Type Into Control    Edit    Hello, Robot Framework!
Type Into Control    name=UsernameField    admin    timeout=5
```

### Get Control Text

**Get text from a control.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Returns:**
- `str`: Text from the control

**Examples:**
```robotframework
${text}    Get Control Text    Edit
${text}    Get Control Text    name=StatusLabel    timeout=5
```

### Control Should Exist

**Verify that a control exists.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Examples:**
```robotframework
Control Should Exist    OKButton
Control Should Exist    name=SubmitButton    timeout=5
```

### Control Should Not Exist

**Verify that a control does not exist.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `timeout`: Timeout for waiting until the control is not available (default: library timeout)

**Examples:**
```robotframework
Control Should Not Exist    ErrorDialog
Control Should Not Exist    name=LoadingSpinner    timeout=5
```

### Set Control Value

**Set the value of a control.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `value`: Value to set for the control
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Examples:**
```robotframework
Set Control Value    UsernameField    admin
Set Control Value    name=PasswordField    secret    timeout=5
```

### Get Control Value

**Get the value of a control.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Returns:**
- `str`: Value of the control

**Examples:**
```robotframework
${value}    Get Control Value    UsernameField
${value}    Get Control Value    name=ComboBox    timeout=5
```

### Select From Combobox

**Select an item from a combobox control.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `item`: Item to select from the combobox
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Examples:**
```robotframework
Select From Combobox    CountryComboBox    United States
Select From Combobox    name=LanguageComboBox    English    timeout=5
```

### Check Checkbox

**Check a checkbox control.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Examples:**
```robotframework
Check Checkbox    AcceptTermsCheckbox
Check Checkbox    name=EnableFeatureCheckbox    timeout=5
```

### Uncheck Checkbox

**Uncheck a checkbox control.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Examples:**
```robotframework
Uncheck Checkbox    AcceptTermsCheckbox
Uncheck Checkbox    name=EnableFeatureCheckbox    timeout=5
```

### Checkbox Should Be Checked

**Verify that a checkbox is checked.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Examples:**
```robotframework
Checkbox Should Be Checked    AcceptTermsCheckbox
Checkbox Should Be Checked    name=EnableFeatureCheckbox    timeout=5
```

### Checkbox Should Be Unchecked

**Verify that a checkbox is unchecked.**

**Arguments:**
- `control_identifier`: Control identifier (name, id, class name, or other criteria)
- `timeout`: Timeout for waiting until the control is available (default: library timeout)

**Examples:**
```robotframework
Checkbox Should Be Unchecked    AcceptTermsCheckbox
Checkbox Should Be Unchecked    name=EnableFeatureCheckbox    timeout=5
```

## 3. Keyboard & Mouse Keywords

### Press Keys

**Press keyboard keys.**

**Arguments:**
- `keys`: Keys to press (can be multiple keys)

**Examples:**
```robotframework
Press Keys    ENTER
Press Keys    CTRL    C
Press Keys    WIN    R
```

### Type Text

**Type text.**

**Arguments:**
- `text`: Text to type
- `delay`: Delay between keystrokes in seconds (default: 0)

**Examples:**
```robotframework
Type Text    Hello, World!
Type Text    Password123    delay=0.1
```

### Mouse Move To

**Move the mouse to a specific position.**

**Arguments:**
- `x`: X coordinate
- `y`: Y coordinate

**Examples:**
```robotframework
Mouse Move To    100    200
Mouse Move To    ${x}    ${y}
```

### Mouse Click

**Click the mouse.**

**Arguments:**
- `x`: X coordinate (optional, if not provided clicks at current position)
- `y`: Y coordinate (optional, if not provided clicks at current position)
- `button`: Mouse button to click ("left", "right", "middle", default: "left")

**Examples:**
```robotframework
Mouse Click
Mouse Click    100    200
Mouse Click    button=right
Mouse Click    ${x}    ${y}    button=middle
```

### Mouse Double Click

**Double click the mouse.**

**Arguments:**
- `x`: X coordinate (optional, if not provided clicks at current position)
- `y`: Y coordinate (optional, if not provided clicks at current position)
- `button`: Mouse button to click ("left", "right", "middle", default: "left")

**Examples:**
```robotframework
Mouse Double Click
Mouse Double Click    100    200
Mouse Double Click    button=right
```

### Mouse Right Click

**Right click the mouse.**

**Arguments:**
- `x`: X coordinate (optional, if not provided clicks at current position)
- `y`: Y coordinate (optional, if not provided clicks at current position)

**Examples:**
```robotframework
Mouse Right Click
Mouse Right Click    100    200
```

### Scroll Mouse Wheel

**Scroll the mouse wheel.**

**Arguments:**
- `amount`: Scroll amount (positive for up, negative for down)
- `x`: X coordinate (optional, if not provided scrolls at current position)
- `y`: Y coordinate (optional, if not provided scrolls at current position)

**Examples:**
```robotframework
Scroll Mouse Wheel    10    # Scroll up 10 units
Scroll Mouse Wheel    -5    # Scroll down 5 units
Scroll Mouse Wheel    3    100    200    # Scroll up at specific position
```

### Press And Hold Keys

**Press and hold keyboard keys.**

**Arguments:**
- `keys`: Keys to press and hold (can be multiple keys)

**Examples:**
```robotframework
Press And Hold Keys    SHIFT
Press And Hold Keys    CTRL    ALT
```

### Release Keys

**Release keyboard keys.**

**Arguments:**
- `keys`: Keys to release (can be multiple keys)

**Examples:**
```robotframework
Release Keys    SHIFT
Release Keys    CTRL    ALT
```

### Type Special Key

**Type a special key.**

**Arguments:**
- `key`: Special key to type (ENTER, TAB, ESC, etc.)

**Examples:**
```robotframework
Type Special Key    ENTER
Type Special Key    TAB
Type Special Key    ESC
```
