# robotframework_robocorp_windows/keywords/async_control_operations.py

"""
异步控件操作关键字，使用concurrent.futures实现线程池，避免单线程阻塞
"""

from robot.api.deco import keyword
from concurrent.futures import ThreadPoolExecutor
import time
from ..services.control_service import ControlService
from ..utils.exceptions import (
    WindowNotFoundError,
    ControlNotFoundError,
    ControlOperationException
)


class AsyncControlOperationsKeywords:
    """异步控件操作关键字，提供异步版本的控件操作方法"""
    
    def __init__(self, library):
        """初始化异步控件操作关键字
        
        Args:
            library: 主库实例
        """
        self.library = library
        self.logger = library.logger
        self.builtin = library.builtin
        self.control_service = ControlService()
        self.control_service.set_logger(self.logger)
        self.executor = ThreadPoolExecutor(max_workers=5)  # 创建线程池，最大5个线程
    
    @keyword("Async Type Into Control")
    def async_type_into_control(self, control_identifier, text, timeout=None):
        """异步向控件输入文本
        
        Args:
            control_identifier: 控件标识符
            text: 要输入的文本
            timeout: 超时时间（秒）
            
        Returns:
            str: 任务ID，可用于后续查询结果
            
        Examples:
        | ${task_id} | Async Type Into Control | name=LargeTextArea | ${long_text} |
        | # 执行其他操作 |
        | Wait For Async Task | ${task_id} |
        """
        timeout = timeout or self.library.timeout
        
        def type_task():
            """实际的文本输入任务"""
            window = self.library._get_current_window()
            control = self.control_service.find_control(window, control_identifier, timeout)
            self.control_service.type_into_control(control, text)
            return f"Successfully typed into control {control_identifier}"
        
        # 提交任务到线程池
        future = self.executor.submit(type_task)
        # 返回future对象的标识，用于后续查询
        return id(future)
    
    @keyword("Async Find All Controls")
    def async_find_all_controls(self, control_identifier, timeout=None):
        """异步查找所有匹配的控件
        
        Args:
            control_identifier: 控件标识符
            timeout: 超时时间（秒）
            
        Returns:
            str: 任务ID，可用于后续查询结果
            
        Examples:
        | ${task_id} | Async Find All Controls | name=ListBoxItem |
        | ${controls} | Wait For Async Task | ${task_id} |
        | Log | Found ${len(controls)} controls |
        """
        timeout = timeout or self.library.timeout
        
        def find_all_task():
            """实际的查找所有控件任务"""
            window = self.library._get_current_window()
            # 这里假设robocorp-windows支持find_all方法，返回所有匹配的控件
            # 如果不支持，我们可以模拟实现
            controls = []
            # 简单实现：多次尝试查找，直到超时
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    control = self.control_service.find_control(window, control_identifier, timeout=0.5)
                    if control and control not in controls:
                        controls.append(control)
                    # 短暂等待，避免CPU占用过高
                    time.sleep(0.1)
                except ControlNotFoundError:
                    pass
            return controls
        
        # 提交任务到线程池
        future = self.executor.submit(find_all_task)
        return id(future)
    
    @keyword("Wait For Async Task")
    def wait_for_async_task(self, task_id, timeout=None):
        """等待异步任务完成并返回结果
        
        Args:
            task_id: 异步任务的ID
            timeout: 等待超时时间（秒），如果为None则使用默认超时
            
        Returns:
            Any: 异步任务的返回结果
            
        Examples:
        | ${task_id} | Async Type Into Control | name=LargeTextArea | ${long_text} |
        | ${result} | Wait For Async Task | ${task_id} | timeout=30 |
        | Log | ${result} |
        """
        timeout = timeout or self.library.timeout
        
        # 查找对应的future对象
        future = None
        for thread in self.executor._threads:
            for obj in thread._tstate_lock._waiters:
                if id(obj) == task_id:
                    future = obj
                    break
            if future:
                break
        
        if not future:
            raise ValueError(f"Task with ID {task_id} not found")
        
        try:
            # 等待任务完成并返回结果
            return future.result(timeout=timeout)
        except Exception as e:
            raise RuntimeError(f"Async task failed: {str(e)}")
    
    @keyword("Async Click Control")
    def async_click_control(self, control_identifier, timeout=None):
        """异步点击控件
        
        Args:
            control_identifier: 控件标识符
            timeout: 超时时间（秒）
            
        Returns:
            str: 任务ID，可用于后续查询结果
            
        Examples:
        | ${task_id} | Async Click Control | name=LongRunningButton |
        | Wait For Async Task | ${task_id} |
        """
        timeout = timeout or self.library.timeout
        
        def click_task():
            """实际的点击任务"""
            window = self.library._get_current_window()
            control = self.control_service.find_control(window, control_identifier, timeout)
            self.control_service.click_control(control)
            return f"Successfully clicked control {control_identifier}"
        
        # 提交任务到线程池
        future = self.executor.submit(click_task)
        return id(future)
    
    @keyword("Shutdown Async Executor")
    def shutdown_async_executor(self, wait=True):
        """关闭异步执行器
        
        Args:
            wait: 是否等待所有任务完成后关闭（默认：True）
            
        Examples:
        | Shutdown Async Executor |
        | Shutdown Async Executor | wait=False |
        """
        self.executor.shutdown(wait=wait)
        # 重新创建一个新的执行器，以便后续使用
        self.executor = ThreadPoolExecutor(max_workers=5)
        return "Async executor shutdown completed"
