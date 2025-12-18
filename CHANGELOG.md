# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-18

### Added

- **Custom Exception Hierarchy**: Implemented comprehensive custom exceptions (ApplicationNotConnectedError, NoActiveWindowError, InvalidLocatorError, etc.) for better error handling and debugging
- **Locator Validation**: Added `Validate Locator` keyword and comprehensive locator validation functionality to detect invalid locator formats early
- **Enhanced Locator Strategies**: Extended support for multiple locator strategies including name, id, class, text, xpath, index, and executable
- **Control Caching Mechanism**: Implemented control cache to improve performance by reducing repeated control lookups
- **Advanced Logging**: Added configurable log levels and detailed DEBUG-level logs for key operations
- **Performance Testing**: Added performance test suite to verify system stability under high load
- **Enhanced Examples**: Added calculator_example.robot demonstrating complex control operations and menu navigation
- **Advanced Usage Guide**: Updated USAGE_GUIDE.md with advanced scenarios including complex window switching and dynamic control handling

### Changed

- **Updated Dependency Versions**: Updated Robot Framework compatibility to 6.x/7.x series
- **Improved Test Coverage**: Increased overall test coverage from 68% to 70%
- **Enhanced Cross-Platform Compatibility**: Improved pywin32 version compatibility handling with clearer installation instructions
- **Better Error Messages**: Replaced generic RuntimeError with specific custom exceptions for more informative error messages
- **Optimized Setup Configuration**: Updated setup.py with clearer version constraints and extras_require options
- **Fixed Documentation**: Corrected syntax warnings in documentation by replacing backslashes with forward slashes in paths

### Fixed

- **Test Failures**: Fixed unit tests to expect custom exceptions instead of generic RuntimeError
- **Dependency Conflict Handling**: Improved installation guide with solutions for pywin32 version conflicts
- **验收测试稳定性**: Enhanced acceptance tests with proper setup and teardown procedures to ensure reliable execution

### Deprecated

- **Legacy Keyboard/Mouse Operations**: Temporarily disabled keyboard and mouse operations due to robocorp-windows 1.0.0 limitations (code is ready for future reactivation)

## [0.1.0] - 2025-12-10

### Added

- Initial release of the Robot Framework Robocorp Windows Library
- Basic window management functionality
- Core control operations
- Simple keyboard and mouse operations
- Basic test coverage

## [0.0.1] - 2025-12-01

### Added

- Project initialization
- Basic library structure
- Initial keyword implementation
- Simple test cases

## How to Update

To update to the latest version, run:

```bash
pip install --upgrade robotframework-robocorp-windows
```

For specific version requirements, see the [Installation Guide](INSTALLATION_GUIDE.md) for detailed instructions on handling dependency conflicts.
