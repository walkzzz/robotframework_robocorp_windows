# 测试文件组织结构规范

## 1. 分类标准

根据测试类型、功能和用途，将测试文件分为以下几类：

| 测试类型 | 描述 | 存放目录 | 文件命名规则 |
|---------|------|---------|-------------|
| **单元测试** | 验证单个模块或函数的功能 | `tests/unit/` | `test_<module_name>.py` |
| **集成测试** | 验证不同模块之间的交互 | `tests/integration/` | `test_<integration_scenario>.py` |
| **验收测试** | 验证整个系统的功能是否符合预期 | `tests/acceptance/` | `<feature>_acceptance.robot` |
| **示例测试** | 展示如何使用库的功能 | `examples/` | `<feature>_example.robot` |
| **开发测试** | 开发过程中用于验证功能的临时测试 | `tests/development/` | `test_<development_test>.robot` 或 `test_<development_test>.py` |

## 2. 目录结构

```
robocorp_winows/
├── examples/                    # 示例测试
│   ├── calculator_example.robot
│   └── notepad_example.robot
├── tests/                       # 测试文件根目录
│   ├── acceptance/              # 验收测试
│   │   └── windows_automation.robot
│   ├── development/             # 开发测试
│   │   ├── test_basic.robot
│   │   ├── test_basic_library.py
│   │   ├── test_library_direct.py
│   │   ├── test_library_import.py
│   │   ├── test_simple.robot
│   │   └── test_single_file.robot
│   ├── integration/             # 集成测试
│   │   ├── test_module_integration.py
│   │   └── test_performance.py
│   └── unit/                    # 单元测试
│       ├── test_control_operations.py
│       ├── test_control_service.py
│       ├── test_exception_scenarios.py
│       ├── test_keyboard_mouse.py
│       ├── test_library.py
│       ├── test_locator_utils.py
│       ├── test_window_management.py
│       └── test_window_service.py
└── TEST_FILE_ORGANIZATION.md    # 测试文件组织结构说明
```

## 3. 文件命名规则

### 3.1 单元测试文件

- 命名格式：`test_<module_name>.py`
- 示例：`test_control_operations.py`、`test_library.py`
- 说明：测试单个模块的功能

### 3.2 集成测试文件

- 命名格式：`test_<integration_scenario>.py`
- 示例：`test_module_integration.py`、`test_performance.py`
- 说明：测试不同模块之间的交互

### 3.3 验收测试文件

- 命名格式：`<feature>_acceptance.robot`
- 示例：`windows_automation.robot`
- 说明：使用Robot Framework验证整个系统的功能

### 3.4 示例测试文件

- 命名格式：`<feature>_example.robot`
- 示例：`notepad_example.robot`、`calculator_example.robot`
- 说明：展示如何使用库的功能

### 3.5 开发测试文件

- 命名格式：`test_<development_test>.robot` 或 `test_<development_test>.py`
- 示例：`test_simple.robot`、`test_exception_scenarios.py`
- 说明：开发过程中用于验证功能的临时测试

## 4. 测试文件迁移说明

### 4.1 已迁移文件

| 原文件路径 | 新文件路径 | 测试类型 |
|-----------|-----------|---------|
| `test_basic.robot` | `tests/development/test_basic.robot` | 开发测试 |
| `test_basic_library.py` | `tests/development/test_basic_library.py` | 开发测试 |
| `test_exception_scenarios.py` | `tests/unit/test_exception_scenarios.py` | 单元测试 |
| `test_library_direct.py` | `tests/development/test_library_direct.py` | 开发测试 |
| `test_library_import.py` | `tests/development/test_library_import.py` | 开发测试 |
| `test_simple.robot` | `tests/development/test_simple.robot` | 开发测试 |
| `test_single_file.robot` | `tests/development/test_single_file.robot` | 开发测试 |

### 4.2 保留文件

| 文件路径 | 测试类型 | 说明 |
|---------|---------|------|
| `tests/acceptance/windows_automation.robot` | 验收测试 | 已按规范存放 |
| `tests/integration/test_module_integration.py` | 集成测试 | 已按规范存放 |
| `tests/integration/test_performance.py` | 集成测试 | 已按规范存放 |
| `tests/unit/test_control_operations.py` | 单元测试 | 已按规范存放 |
| `tests/unit/test_control_service.py` | 单元测试 | 已按规范存放 |
| `tests/unit/test_keyboard_mouse.py` | 单元测试 | 已按规范存放 |
| `tests/unit/test_library.py` | 单元测试 | 已按规范存放 |
| `tests/unit/test_locator_utils.py` | 单元测试 | 已按规范存放 |
| `tests/unit/test_window_management.py` | 单元测试 | 已按规范存放 |
| `tests/unit/test_window_service.py` | 单元测试 | 已按规范存放 |
| `examples/calculator_example.robot` | 示例测试 | 已按规范存放 |
| `examples/notepad_example.robot` | 示例测试 | 已按规范存放 |

## 5. 查找和使用测试文件

### 5.1 查找测试文件

- 若要查找特定模块的单元测试，请查看 `tests/unit/` 目录下的 `test_<module_name>.py` 文件
- 若要查找集成测试，请查看 `tests/integration/` 目录下的相应文件
- 若要查找验收测试，请查看 `tests/acceptance/` 目录下的相应文件
- 若要查找示例测试，请查看 `examples/` 目录下的相应文件
- 若要查找开发测试，请查看 `tests/development/` 目录下的相应文件

### 5.2 运行测试

- 运行所有测试：`python -m pytest tests/`
- 运行单元测试：`python -m pytest tests/unit/`
- 运行集成测试：`python -m pytest tests/integration/`
- 运行验收测试：`robot tests/acceptance/`
- 运行开发测试：`robot tests/development/` 或 `python -m pytest tests/development/`

## 6. 维护规则

1. 新添加的测试文件必须按照上述分类标准存放到相应的目录中
2. 测试文件的命名必须符合上述命名规则
3. 定期清理不再需要的开发测试文件
4. 确保每个测试文件都有清晰的文档说明其功能和用途
5. 测试文件应该与被测代码保持同步更新

## 7. 文档更新

本规范会根据项目的发展和需求变化进行更新。更新时，需要：
1. 修改本文件中的相应内容
2. 更新文件迁移说明
3. 通知团队成员

## 8. 联系方式

如有任何疑问或建议，请联系项目负责人。

---

**版本**: 1.0
**创建日期**: 2025-12-18
**更新日期**: 2025-12-18
