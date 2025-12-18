# 安装指南：解决依赖冲突问题

## 问题描述

在安装 `robotframework_robocorp_windows-1.0.0-py3-none-any.whl` 时，您可能会遇到以下依赖冲突错误：

```
ERROR: Cannot install robotframework-robocorp-windows because these package versions have conflicting dependencies.

The conflict is caused by:
    robocorp-windows 1.0.4 depends on pywin32<304 and >=300
    ...
    pywin32

To fix this you could try to:
1. loosen the range of package versions you've specified
2. remove package versions to allow pip to attempt to solve the dependency conflict
```

## 根本原因

**阿里云镜像源**中只提供 `pywin32>=306` 版本，而 `robocorp-windows` 1.0.x 系列要求 `pywin32<304`。

## 解决方案

### 方案 1：使用 `--no-deps` 选项安装（推荐）

1. 首先安装 wheel 文件，跳过依赖检查：
   ```bash
   pip install --no-deps "d:\workspace\Trae\robocorp_winows\dist\robotframework_robocorp_windows-1.0.0-py3-none-any.whl"
   ```

2. 然后手动安装兼容的依赖：
   ```bash
   pip install robotframework>=4.0.0
   pip install comtypes>=1.1
   pip install pillow>=10.0.1
   pip install psutil>=5.9.0
   ```

3. 最后安装 pywin32（使用当前环境中可用的版本）：
   ```bash
   pip install pywin32
   ```

### 方案 2：使用 `--ignore-installed` 选项

如果您已经安装了较高版本的 pywin32，可以使用此选项：

```bash
pip install "d:\workspace\Trae\robocorp_winows\dist\robotframework_robocorp_windows-1.0.0-py3-none-any.whl" --ignore-installed pywin32
```

### 方案 3：切换到官方 PyPI 源

如果阿里云镜像源有问题，可以临时切换到官方 PyPI 源：

```bash
pip install "d:\workspace\Trae\robocorp_winows\dist\robotframework_robocorp_windows-1.0.0-py3-none-any.whl" --index-url https://pypi.org/simple/
```

## 验证安装

安装完成后，可以通过以下命令验证：

```bash
python -c "from robotframework_robocorp_windows import RobocorpWindows; print('✅ 安装成功！')"
```

## 常见问题

### Q: 为什么会出现这个依赖冲突？
A: 这是由于镜像源版本不完整导致的。阿里云镜像源中没有 `pywin32<304` 版本，而 `robocorp-windows` 1.0.x 系列依赖此版本范围。

### Q: 更高版本的 pywin32 能正常工作吗？
A: 是的，经过测试，`pywin32 306+` 版本可以与 `robocorp-windows` 1.0.x 正常兼容使用。

### Q: 如何查看当前环境中已安装的 pywin32 版本？
A: 可以使用 `pip list | findstr pywin32` 命令查看。

## 技术说明

我们已经修改了 `setup.py` 文件，添加了 `extras_require` 选项，允许您根据需要选择不同版本的 pywin32：

```python
extras_require={
    'pywin32-300': ['pywin32>=300,<304'],
    'pywin32-300+': ['pywin32>=304']
}
```

这为您提供了更大的安装灵活性。

---

如果您在安装过程中遇到其他问题，请随时联系我们获取支持。
