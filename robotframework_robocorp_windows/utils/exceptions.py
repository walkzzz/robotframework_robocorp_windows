# robotframework_robocorp_windows/utils/exceptions.py

"""
自定义异常体系，用于标准化库的异常处理
"""


class RobocorpWindowsError(Exception):
    """所有库异常的基类"""
    pass


class WindowError(RobocorpWindowsError):
    """窗口操作相关异常的基类"""
    pass


class WindowNotFoundError(WindowError):
    """当目标窗口未找到时抛出"""
    pass


class WindowOperationException(WindowError):
    """窗口操作失败时抛出"""
    pass


class ControlError(RobocorpWindowsError):
    """控件操作相关异常的基类"""
    pass


class ControlNotFoundError(ControlError):
    """当目标控件未找到时抛出"""
    pass


class ControlOperationException(ControlError):
    """控件操作失败时抛出"""
    pass


class ApplicationError(RobocorpWindowsError):
    """应用程序操作相关异常的基类"""
    pass


class ApplicationLaunchError(ApplicationError):
    """应用程序启动失败时抛出"""
    pass


class ApplicationConnectionError(ApplicationError):
    """连接应用程序失败时抛出"""
    pass


class ApplicationNotConnectedError(ApplicationError):
    """应用程序未连接时抛出"""
    pass


class WindowError(RobocorpWindowsError):
    """窗口操作相关异常的基类"""
    pass


class WindowNotFoundError(WindowError):
    """当目标窗口未找到时抛出"""
    pass


class WindowOperationException(WindowError):
    """窗口操作失败时抛出"""
    pass


class NoActiveWindowError(WindowError):
    """没有活动窗口时抛出"""
    pass


class ControlError(RobocorpWindowsError):
    """控件操作相关异常的基类"""
    pass


class ControlNotFoundError(ControlError):
    """当目标控件未找到时抛出"""
    pass


class ControlOperationException(ControlError):
    """控件操作失败时抛出"""
    pass


class AsyncOperationException(ControlError):
    """异步操作失败时抛出"""
    pass


class TimeoutError(RobocorpWindowsError):
    """操作超时异常"""
    pass
