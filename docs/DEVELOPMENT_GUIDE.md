# Robocorp Windows Library - 开发指南

## 1. 项目概述

Robocorp Windows Library是一个基于robocorp-windows的Robot Framework库，提供Windows自动化功能，包括窗口管理、控件操作和键盘鼠标操作。

## 2. 架构设计

### 2.1 分层架构

库采用分层架构设计，各层职责明确，便于扩展和维护：

| 层级 | 模块 | 职责 |
|------|------|------|
| 接口层 | keywords/ | 仅负责暴露Robot Framework关键字 |
| 业务层 | services/ | 封装核心业务逻辑 |
| 驱动层 | drivers/ | 统一封装对robocorp-windows底层库的调用 |
| 工具层 | utils/ | 提供通用工具函数 |
| 扩展层 | extensions/ | 支持插件化扩展 |

### 2.2 核心设计原则

1. **单一职责原则**：每个模块只负责一个特定的功能
2. **依赖倒置原则**：高层模块不依赖低层模块，二者都依赖抽象
3. **开放封闭原则**：对扩展开放，对修改封闭
4. **接口隔离原则**：使用多个专门的接口，而不是单一的总接口
5. **里氏替换原则**：子类型必须能够替换掉它们的父类型

## 3. 代码结构

### 3.1 目录结构

```
robotframework-robocorp-windows/
├── robotframework_robocorp_windows/  # 主库目录
│   ├── keywords/                     # 关键字模块
│   │   ├── async_control_operations.py  # 异步控件操作
│   │   ├── control_operations.py     # 控件操作
│   │   ├── keyboard_mouse.py         # 键盘鼠标操作
│   │   └── window_management.py      # 窗口管理
│   ├── services/                     # 服务层
│   │   ├── control_service.py        # 控件服务
│   │   └── window_service.py         # 窗口服务
│   ├── drivers/                      # 驱动层
│   │   ├── robocorp_driver.py        # robocorp-windows封装
│   │   └── version_adapter.py        # 版本适配
│   ├── utils/                        # 工具层
│   │   ├── cache.py                  # 控件缓存
│   │   ├── config.py                 # 配置管理
│   │   ├── exceptions.py             # 自定义异常
│   │   ├── locator_utils.py          # 定位器工具
│   │   └── logger.py                 # 日志工具
│   ├── extensions/                   # 扩展层
│   │   ├── __init__.py
│   │   └── base.py                   # 扩展接口
│   ├── __init__.py
│   └── library.py                    # 主库类
├── tests/                            # 测试目录
│   ├── unit/                         # 单元测试
│   ├── integration/                  # 集成测试
│   └── acceptance/                   # 验收测试
├── docs/                             # 文档目录
└── setup.py                          # 安装配置
```

### 3.2 核心模块说明

#### 3.2.1 主库类 (library.py)

主库类`RobocorpWindows`是Robot Framework库的入口点，负责初始化各个关键字模块，并提供通用的配置和日志功能。

#### 3.2.2 关键字模块 (keywords/)

关键字模块负责将Robot Framework关键字映射到底层服务调用，每个关键字模块对应一类功能：

- **window_management.py**：窗口管理关键字
- **control_operations.py**：控件操作关键字
- **keyboard_mouse.py**：键盘鼠标操作关键字
- **async_control_operations.py**：异步控件操作关键字

#### 3.2.3 服务层 (services/)

服务层封装了核心业务逻辑，提供了对底层驱动的抽象：

- **window_service.py**：窗口管理服务，负责启动应用、连接应用、管理窗口等
- **control_service.py**：控件操作服务，负责查找控件、操作控件等

#### 3.2.4 驱动层 (drivers/)

驱动层统一封装了对robocorp-windows底层库的调用，提供了版本适配能力：

- **robocorp_driver.py**：封装了robocorp-windows的核心功能
- **version_adapter.py**：自动适配不同版本的依赖库

#### 3.2.5 工具层 (utils/)

工具层提供了通用的工具函数：

- **cache.py**：控件查找缓存，减少重复查找开销
- **config.py**：配置管理，支持多级配置覆盖
- **exceptions.py**：自定义异常类
- **locator_utils.py**：定位器工具，支持多种定位策略
- **logger.py**：结构化日志系统

#### 3.2.6 扩展层 (extensions/)

扩展层支持插件化扩展，允许自定义定位策略和关键字：

- **base.py**：扩展接口定义

## 4. 开发流程

### 4.1 开发环境搭建

1. 克隆代码仓库
2. 安装依赖：
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt
   ```
3. 运行测试验证环境：
   ```bash
   python -m pytest tests/unit/
   ```

### 4.2 代码开发规范

1. **命名规范**：
   - 模块名：小写字母+下划线
   - 类名：驼峰命名法
   - 函数名：小写字母+下划线
   - 变量名：小写字母+下划线

2. **代码风格**：
   - 遵循PEP 8规范
   - 使用black进行代码格式化
   - 使用flake8进行代码检查

3. **注释规范**：
   - 为每个模块、类、函数添加docstring
   - 使用reStructuredText格式
   - 描述清晰、准确

### 4.3 测试规范

1. **测试类型**：
   - 单元测试：测试单个函数或方法
   - 集成测试：测试模块间的交互
   - 验收测试：测试完整的功能流程

2. **测试覆盖率**：
   - 单元测试覆盖率不低于80%
   - 集成测试覆盖率不低于60%

3. **测试命名规范**：
   - 测试文件：test_*.py
   - 测试类：Test*Keywords或Test*
   - 测试方法：test_*

### 4.4 提交规范

1. **提交信息**：
   - 清晰描述提交内容
   - 使用英文或中文
   - 格式：[类型] 简短描述
   - 类型：feat, fix, docs, style, refactor, test, chore

2. **提交频率**：
   - 每个提交只包含一个功能或修复
   - 频繁提交，保持提交粒度小

## 5. 扩展开发

### 5.1 自定义定位策略

1. 继承`LocatorStrategy`基类
2. 实现必要的方法
3. 注册定位策略

示例：

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

### 5.2 自定义关键字扩展

1. 继承`KeywordExtension`基类
2. 实现必要的方法
3. 注册关键字扩展

示例：

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

## 6. 调试与日志

### 6.1 调试技巧

1. **启用调试日志**：
   ```robotframework
   *** Settings ***
   Library    RobocorpWindows    log_level=DEBUG
   ```

2. **使用断点调试**：
   - 在代码中添加断点
   - 使用Python调试器进行调试

3. **查看日志文件**：
   - Robot Framework会生成日志文件
   - 日志文件中包含详细的执行信息

### 6.2 日志级别

| 级别 | 描述 |
|------|------|
| TRACE | 最详细的日志，包含所有执行细节 |
| DEBUG | 调试信息，包含关键字执行、控件查找等 |
| INFO | 普通信息，包含主要操作步骤 |
| WARN | 警告信息，包含潜在问题 |
| ERROR | 错误信息，包含执行错误 |

## 7. 发布流程

1. 更新版本号：
   - 修改setup.py中的version字段

2. 更新CHANGELOG.md：
   - 记录新功能、修复的bug、变更的API

3. 运行所有测试：
   ```bash
   python -m pytest tests/
   ```

4. 生成打包文件：
   ```bash
   python setup.py bdist_wheel
   ```

5. 验证打包产物：
   - 检查dist目录中的wheel文件
   - 测试安装包在目标环境中的部署

6. 发布到PyPI：
   ```bash
   twine upload dist/*
   ```

## 8. 常见问题

### 8.1 依赖冲突

- **问题**：安装时遇到依赖冲突
- **解决方案**：使用`--no-deps`选项安装，然后手动安装依赖

### 8.2 控件查找失败

- **问题**：无法找到预期的控件
- **解决方案**：
  - 检查控件标识符是否正确
  - 增加超时时间
  - 使用更具体的控件标识符
  - 检查窗口是否正确

### 8.3 异步操作失败

- **问题**：异步操作超时或失败
- **解决方案**：
  - 检查异步任务的实现
  - 增加超时时间
  - 确保线程安全

## 9. 贡献指南

欢迎提交Issue和Pull Request！

### 9.1 提交Issue

1. 描述问题清晰、准确
2. 提供重现步骤
3. 提供相关日志和截图
4. 说明环境信息

### 9.2 提交Pull Request

1. 从main分支创建新分支
2. 实现功能或修复bug
3. 运行所有测试确保通过
4. 更新相关文档
5. 提交Pull Request

## 10. 联系方式

如有问题，请提交Issue到GitHub仓库：https://github.com/walkzzz/robotframework_robocorp_windows.git
