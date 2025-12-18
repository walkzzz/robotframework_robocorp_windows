# Robot Framework Robocorp Windows Library

一个基于robocorp-windows的Robot Framework库，提供Windows自动化功能，包括窗口管理、控件操作和键盘鼠标操作。

## 兼容性

### 支持版本
- **Robot Framework**：6.0.0 - 7.x
- **Python**：3.8, 3.9, 3.10, 3.11, 3.12
- **Windows**：Windows 10, Windows 11

### pywin32版本适配
- Python 3.8：pywin32 >= 300, < 304
- Python 3.9+：pywin32 >= 300

## 功能特性

### 核心功能
- **窗口管理**：启动应用程序、连接到已运行的应用程序、设置当前窗口、关闭应用程序等
- **控件操作**：查找控件、点击、双击、右键点击、输入文本、获取文本等
- **键盘鼠标操作**：模拟键盘输入、鼠标点击、鼠标移动等

### 高级功能
- **异步操作支持**：支持异步执行控件操作，提高性能
- **控件查找缓存**：缓存控件查找结果，减少重复查找开销
- **版本适配抽象层**：自动适配不同版本的pywin32，解决依赖冲突
- **插件化扩展机制**：支持自定义定位策略和关键字扩展
- **结构化日志系统**：提供详细的日志记录，便于调试
- **分层配置管理**：支持通过Library参数、环境变量、配置文件多级覆盖配置

## 安装

### 基本安装
```bash
pip install robotframework-robocorp-windows
```

### 解决依赖冲突
如果遇到pywin32版本不兼容问题，可以使用以下方法：

1. 使用--no-deps选项安装wheel包，然后手动安装依赖：
```bash
pip install --no-deps robotframework-robocorp-windows
pip install robocorp-windows>=1.0.0
```

2. 使用--ignore-installed选项强制安装：
```bash
pip install --ignore-installed robotframework-robocorp-windows
```

3. 切换到官方PyPI源：
```bash
pip install robotframework-robocorp-windows --index-url https://pypi.org/simple/
```

## 架构设计

### 分层架构
- **接口层**：关键字模块（keywords/），仅负责暴露Robot Framework关键字
- **业务层**：服务模块（services/），封装核心业务逻辑
- **驱动层**：驱动模块（drivers/），统一封装对robocorp-windows底层库的调用
- **工具层**：工具模块（utils/），提供通用工具函数
- **扩展层**：扩展模块（extensions/），支持插件化扩展

### 目录结构
```
robotframework-robocorp-windows/
├── robotframework_robocorp_windows/
│   ├── __init__.py                   # 库入口点
│   ├── library.py                    # 主库类
│   ├── keywords/                     # 关键字模块目录
│   │   ├── window_management.py      # 窗口管理关键字
│   │   ├── control_operations.py     # 控件操作关键字
│   │   ├── keyboard_mouse.py         # 键盘鼠标操作关键字
│   │   └── async_control_operations.py  # 异步控件操作关键字
│   ├── services/                     # 服务层目录
│   │   ├── window_service.py         # 窗口管理服务
│   │   └── control_service.py        # 控件操作服务
│   ├── drivers/                      # 驱动层目录
│   │   ├── robocorp_driver.py        # robocorp-windows封装
│   │   └── version_adapter.py       # 版本适配
│   ├── utils/                        # 工具层目录
│   │   ├── exceptions.py             # 自定义异常
│   │   ├── cache.py                  # 控件查找缓存
│   │   ├── config.py                 # 配置管理
│   │   └── logger.py                 # 结构化日志
│   └── extensions/                   # 扩展层目录
│       ├── __init__.py
│       └── base.py                   # 扩展接口
├── tests/                            # 测试目录
│   ├── unit/                         # 单元测试
│   ├── integration/                  # 集成测试
│   └── acceptance/                   # 验收测试
├── examples/                         # 示例测试用例
└── setup.py                          # 安装配置
```

## 关键字文档

### 窗口管理关键字

| 关键字 | 描述 | 示例 |
|--------|------|------|
| `Launch Application` | 启动Windows应用程序 | `Launch Application | notepad.exe` |
| `Connect To Application` | 连接到已运行的应用程序 | `Connect To Application | title=Notepad` |
| `Set Current Window` | 设置当前活动窗口 | `Set Current Window | title=Notepad` |
| `Close Application` | 关闭应用程序 | `Close Application` |
| `Minimize Window` | 最小化窗口 | `Minimize Window` |
| `Maximize Window` | 最大化窗口 | `Maximize Window` |
| `Restore Window` | 恢复窗口 | `Restore Window` |
| `Window Should Be Open` | 验证窗口是否打开 | `Window Should Be Open | title=Notepad` |
| `Window Should Be Closed` | 验证窗口是否关闭 | `Window Should Be Closed | title=Notepad` |
| `Get Window Title` | 获取窗口标题 | `${title} | Get Window Title` |

### 控件操作关键字

| 关键字 | 描述 | 示例 |
|--------|------|------|
| `Find Control` | 查找控件 | `${control} | Find Control | Edit` |
| `Find Control Without Cache` | 不使用缓存查找控件 | `${control} | Find Control Without Cache | Edit` |
| `Click Control` | 点击控件 | `Click Control | OKButton` |
| `Double Click Control` | 双击控件 | `Double Click Control | FileIcon` |
| `Right Click Control` | 右键点击控件 | `Right Click Control | ContextMenuButton` |
| `Type Into Control` | 向控件输入文本 | `Type Into Control | Edit | Hello, Robot Framework!` |
| `Get Control Text` | 获取控件文本 | `${text} | Get Control Text | Edit` |
| `Control Should Exist` | 验证控件是否存在 | `Control Should Exist | OKButton` |
| `Control Should Not Exist` | 验证控件是否不存在 | `Control Should Not Exist | ErrorDialog` |
| `Set Control Value` | 设置控件值 | `Set Control Value | UsernameField | admin` |
| `Get Control Value` | 获取控件值 | `${value} | Get Control Value | UsernameField` |
| `Select From Combobox` | 从组合框中选择项目 | `Select From Combobox | CountryComboBox | United States` |
| `Check Checkbox` | 勾选复选框 | `Check Checkbox | AcceptTermsCheckbox` |
| `Uncheck Checkbox` | 取消勾选复选框 | `Uncheck Checkbox | EnableFeatureCheckbox` |
| `Checkbox Should Be Checked` | 验证复选框是否勾选 | `Checkbox Should Be Checked | AcceptTermsCheckbox` |
| `Checkbox Should Be Unchecked` | 验证复选框是否未勾选 | `Checkbox Should Be Unchecked | EnableFeatureCheckbox` |

### 异步操作关键字

| 关键字 | 描述 | 示例 |
|--------|------|------|
| `Async Type Into Control` | 异步向控件输入文本 | `${task_id} | Async Type Into Control | name=LargeTextArea | ${long_text}` |
| `Async Find All Controls` | 异步查找所有匹配的控件 | `${task_id} | Async Find All Controls | name=ListBoxItem` |
| `Async Click Control` | 异步点击控件 | `${task_id} | Async Click Control | name=LongRunningButton` |
| `Wait For Async Task` | 等待异步任务完成 | `${result} | Wait For Async Task | ${task_id}` |
| `Shutdown Async Executor` | 关闭异步执行器 | `Shutdown Async Executor` |

## 使用示例

### 基本示例
```robotframework
*** Settings ***
Library           robotframework_robocorp_windows    timeout=10

*** Test Cases ***
Notepad Test
    Launch Application    notepad.exe
    Type Into Control      Edit    Hello, Robot Framework!
    Click Control          name=Close
    Click Control          name=Don't Save
```

### 使用异步操作
```robotframework
*** Settings ***
Library           robotframework_robocorp_windows

*** Variables ***
${long_text}    ${SPACE * 1000}Hello, this is a long text!${SPACE * 1000}

*** Test Cases ***
Async Type Test
    Launch Application    notepad.exe
    ${task_id}    Async Type Into Control    Edit    ${long_text}
    Log    执行其他操作...
    ${result}    Wait For Async Task    ${task_id}
    Log    ${result}
    Click Control    name=Close
    Click Control    name=Don't Save
```

### 使用缓存控制
```robotframework
*** Settings ***
Library           robotframework_robocorp_windows

*** Test Cases ***
Cache Test
    Launch Application    notepad.exe
    ${control1}    Find Control    Edit    # 第一次查找，缓存控件
    ${control2}    Find Control    Edit    # 第二次查找，使用缓存
    Log    两个控件是否相同: ${control1 is control2}
    ${control3}    Find Control Without Cache    Edit    # 不使用缓存，重新查找
    Log    缓存控件与非缓存控件是否相同: ${control1 is control3}
    Click Control    name=Close
    Click Control    name=Don't Save
```

## 配置

### Library参数
```robotframework
Library           robotframework_robocorp_windows    timeout=30    retry_interval=1.0    log_level=DEBUG
```

### 环境变量
```bash
# 设置超时时间
set ROBOCORP_WINDOWS_TIMEOUT=30

# 设置日志级别
set ROBOCORP_WINDOWS_LOG_LEVEL=DEBUG
```

### 配置文件
创建`robot_windows_config.yaml`文件：
```yaml
timeout: 30
retry_interval: 1.0
log_level: DEBUG
cache_enabled: true
```

## 扩展机制

### 自定义定位策略
```python
from robotframework_robocorp_windows.extensions import LocatorStrategy, extension_manager

class XPathLocatorStrategy(LocatorStrategy):
    def get_name(self):
        return "xpath"
    
    def find_control(self, window, locator, timeout=10.0):
        # 实现xpath定位逻辑
        pass
    
    def is_available(self):
        return True

# 注册定位策略
extension_manager.register_locator_strategy(XPathLocatorStrategy())
```

### 自定义关键字扩展
```python
from robotframework_robocorp_windows.extensions import KeywordExtension, extension_manager

def custom_keyword():
    """自定义关键字"""
    return "Custom keyword executed"

class CustomKeywordExtension(KeywordExtension):
    def get_name(self):
        return "custom_keywords"
    
    def get_keywords(self):
        return {
            "Custom Keyword": custom_keyword
        }
    
    def is_available(self):
        return True

# 注册关键字扩展
extension_manager.register_keyword_extension(CustomKeywordExtension())
```

## 测试

### 运行单元测试
```bash
pytest tests/unit/ -v
```

### 运行集成测试
```bash
python -m pytest tests/integration/ -v
```

### 运行验收测试
```bash
robot tests/acceptance/
```

## 开发

### 安装开发依赖
```bash
pip install -e .
pip install -r requirements-dev.txt
```

### 运行所有测试
```bash
pytest
```

### 生成覆盖率报告
```bash
pytest --cov=robotframework_robocorp_windows tests/
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请提交Issue到GitHub仓库：https://github.com/walkzzz/robotframework_robocorp_windows.git
