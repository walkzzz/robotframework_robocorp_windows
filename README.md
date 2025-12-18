# Robot Framework Robocorp Windows Library

Robot Framework Robocorp Windows Library is a Robot Framework library for Windows automation using the robocorp-windows library. It provides keywords for window management, control operations, keyboard and mouse simulations, and more.

## Features

- **Window Management**: Launch, connect, close, minimize, maximize, and restore windows
- **Control Operations**: Find, click, type into, and get text from controls
- **Keyword-Driven**: Follows Robot Framework's keyword-driven paradigm
- **Easy to Use**: Simple and intuitive keyword names
- **Well Documented**: Detailed documentation for each keyword
- **Compatible**: Works with Robot Framework 4.0+ and Windows 10/11

**Note**: Keyboard and mouse operations are currently not supported in robocorp-windows 1.0.0 and have been temporarily disabled.

## Installation

```bash
pip install robotframework-robocorp-windows
```

## Usage

Import the library in your Robot Framework test case:

```robotframework
*** Settings ***
Library    RobocorpWindows    timeout=10    retry_interval=0.5

*** Test Cases ***
Example Test
    Launch Application    notepad.exe
    Type Into Control    Edit    Hello, Robot Framework!
    Close Application
```

## Keywords

### Window Management
- `Launch Application` - Launch a Windows application
- `Connect To Application` - Connect to an already running application
- `Set Current Window` - Set the current active window
- `Close Application` - Close the currently connected application
- `Minimize Window` - Minimize the current window
- `Maximize Window` - Maximize the current window
- `Restore Window` - Restore the current window
- `Window Should Be Open` - Verify that a window is open
- `Window Should Be Closed` - Verify that a window is closed
- `Get Window Title` - Get the title of the current window

### Control Operations
- `Find Control` - Find a control in the current window
- `Click Control` - Click on a control
- `Double Click Control` - Double click on a control
- `Right Click Control` - Right click on a control
- `Type Into Control` - Type text into a control
- `Get Control Text` - Get text from a control
- `Control Should Exist` - Verify that a control exists
- `Control Should Not Exist` - Verify that a control does not exist
- `Set Control Value` - Set the value of a control
- `Get Control Value` - Get the value of a control

### Keyboard & Mouse Operations

**Note**: Keyboard and mouse operations are currently not supported in robocorp-windows 1.0.0 and have been temporarily disabled. These keywords will be restored in a future release when the underlying library supports them.

## Configuration

The library can be configured with the following parameters:

- `timeout`: Default timeout for waiting operations in seconds (default: 10)
- `retry_interval`: Interval between retries in seconds (default: 0.5)

Example:

```robotframework
Library    RobocorpWindows    timeout=15    retry_interval=1.0
```

## Examples

See the `examples/` directory for sample test cases.

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/robotframework-robocorp-windows.git
cd robotframework-robocorp-windows

# Install development dependencies
pip install -e .

# Run tests
robot tests/
```

### Running Tests

```bash
# Run all tests
robot tests/

# Run only acceptance tests
robot tests/acceptance/

# Run only unit tests
python -m pytest tests/unit/
```

## License

Apache License 2.0
