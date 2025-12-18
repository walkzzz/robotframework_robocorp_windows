# tests/integration/test_performance.py

"""
性能测试，验证系统在高负载下的稳定性和响应时间
"""

import time
import pytest
from unittest.mock import MagicMock, patch
from robotframework_robocorp_windows.library import RobocorpWindows
from robotframework_robocorp_windows.services.control_service import ControlService


class TestPerformance:
    """性能测试类"""
    
    def test_control_caching_performance(self):
        """测试控件缓存对性能的影响
        
        验证使用缓存能显著提高重复查找相同控件的速度
        """
        # 创建服务实例
        control_service = ControlService()
        
        # 模拟窗口和控件
        mock_window = MagicMock()
        mock_window.name = "Test Window"
        mock_window.handle = 12345
        mock_control = MagicMock()
        
        # 模拟驱动层，添加一个小延迟来模拟实际查找开销
        def mock_find_control(window, control_identifier, timeout=10):
            time.sleep(0.05)  # 模拟50ms的查找延迟
            return mock_control
        
        # 应用模拟
        control_service.driver.find_control = mock_find_control
        
        # 测试1: 不使用缓存，多次查找同一控件
        control_service.disable_cache()
        start_time = time.time()
        
        for _ in range(10):
            control_service.find_control(mock_window, "test_control", use_cache=False)
        
        non_cached_time = time.time() - start_time
        
        # 测试2: 使用缓存，多次查找同一控件
        control_service.enable_cache()
        start_time = time.time()
        
        for _ in range(10):
            control_service.find_control(mock_window, "test_control")
        
        cached_time = time.time() - start_time
        
        # 验证缓存带来的性能提升
        assert cached_time < non_cached_time, f"缓存应该更快，实际: 缓存={cached_time:.3f}s, 非缓存={non_cached_time:.3f}s"
        # 预期至少快50%
        assert cached_time < non_cached_time * 0.5, f"缓存提升不明显，实际: 缓存={cached_time:.3f}s, 非缓存={non_cached_time:.3f}s"
    
    def test_consecutive_control_operations(self):
        """测试连续控件操作的性能
        
        验证连续执行100次Find Control操作的稳定性
        """
        # 创建库实例
        lib = RobocorpWindows()
        
        # 模拟窗口和控件
        mock_window = MagicMock()
        mock_window.name = "Test Window"
        mock_window.handle = 12345
        mock_control = MagicMock()
        
        # 设置当前窗口
        lib.current_window = mock_window
        
        # 模拟驱动层
        with patch.object(lib.control_operations.control_service.driver, 'find_control', return_value=mock_control):
            # 连续执行100次查找操作
            start_time = time.time()
            
            for i in range(100):
                control = lib.control_operations.find_control(f"test_control_{i}")
                assert control == mock_control
            
            total_time = time.time() - start_time
            avg_time_per_operation = total_time / 100
            
            # 验证性能指标
            assert total_time < 5.0, f"100次操作总耗时超过5秒，实际: {total_time:.3f}s"
            assert avg_time_per_operation < 0.1, f"单次操作平均耗时超过100ms，实际: {avg_time_per_operation:.3f}s"
    
    def test_keyword_execution_time(self):
        """测试关键字执行时间
        
        验证关键关键字的执行时间符合预期
        """
        # 创建库实例
        lib = RobocorpWindows()
        
        # 模拟窗口和控件
        mock_window = MagicMock()
        mock_window.name = "Test Window"
        mock_window.handle = 12345
        mock_control = MagicMock()
        
        # 设置当前窗口
        lib.current_window = mock_window
        
        # 模拟驱动层
        with patch.object(lib.control_operations.control_service.driver, 'find_control', return_value=mock_control):
            # 测试不同关键字的执行时间
            keywords_to_test = [
                ("find_control", lambda: lib.control_operations.find_control("test_control")),
                ("click_control", lambda: lib.control_operations.click_control("test_control")),
                ("type_into_control", lambda: lib.control_operations.type_into_control("test_control", "test text")),
                ("get_control_text", lambda: lib.control_operations.get_control_text("test_control")),
            ]
            
            for keyword_name, keyword_callable in keywords_to_test:
                start_time = time.time()
                keyword_callable()
                execution_time = time.time() - start_time
                
                # 验证每个关键字的执行时间都在合理范围内
                assert execution_time < 1.0, f"关键字 {keyword_name} 执行时间超过1秒，实际: {execution_time:.3f}s"
    
    def test_window_operation_performance(self):
        """测试窗口操作的性能
        
        验证窗口相关操作的执行时间
        """
        # 创建库实例
        lib = RobocorpWindows()
        
        # 模拟窗口
        mock_window = MagicMock()
        mock_window.name = "Test Window"
        mock_window.handle = 12345
        
        # 设置当前窗口
        lib.current_window = mock_window
        
        # 模拟服务层
        with patch.object(lib.window_management.window_service.driver, 'minimize_window'):
            with patch.object(lib.window_management.window_service.driver, 'maximize_window'):
                with patch.object(lib.window_management.window_service.driver, 'restore_window'):
                    # 测试窗口操作链的性能
                    start_time = time.time()
                    
                    lib.window_management.minimize_window()
                    lib.window_management.maximize_window()
                    lib.window_management.restore_window()
                    
                    total_time = time.time() - start_time
                    
                    # 验证窗口操作链的执行时间
                    assert total_time < 2.0, f"窗口操作链执行时间超过2秒，实际: {total_time:.3f}s"
    
    def test_async_operation_performance(self):
        """测试异步操作的性能
        
        验证异步操作能提高并行处理能力
        """
        # 创建库实例
        lib = RobocorpWindows()
        
        # 模拟窗口和控件
        mock_window = MagicMock()
        mock_window.name = "Test Window"
        mock_window.handle = 12345
        mock_control = MagicMock()
        
        # 设置当前窗口
        lib.current_window = mock_window
        
        # 模拟驱动层，添加延迟来模拟耗时操作
        def mock_type_into_control(control, text):
            time.sleep(0.2)  # 模拟200ms的输入延迟
        
        with patch.object(lib.control_operations.control_service.driver, 'find_control', return_value=mock_control):
            with patch.object(lib.control_operations.control_service, 'type_into_control', side_effect=mock_type_into_control):
                with patch.object(lib.async_control_operations.control_service, 'type_into_control', side_effect=mock_type_into_control):
                    with patch.object(lib.async_control_operations.control_service.driver, 'find_control', return_value=mock_control):
                        # 测试1: 同步执行3个耗时操作
                        start_time = time.time()
                        
                        for _ in range(3):
                            lib.control_operations.type_into_control("test_control", "test text")
                        
                        sync_time = time.time() - start_time
                        
                        # 测试2: 异步执行3个耗时操作
                        start_time = time.time()
                        
                        task_ids = []
                        for _ in range(3):
                            task_id = lib.async_control_operations.async_type_into_control("test_control", "test text")
                            task_ids.append(task_id)
                        
                        # 等待所有异步任务完成
                        for task_id in task_ids:
                            lib.async_control_operations.wait_for_async_task(task_id)
                        
                        async_time = time.time() - start_time
                        
                        # 验证异步执行比同步执行更快
                        assert async_time < sync_time, f"异步执行应该比同步执行快，实际: 异步={async_time:.3f}s, 同步={sync_time:.3f}s"
                        # 预期至少快30%
                        assert async_time < sync_time * 0.7, f"异步执行提升不明显，实际: 异步={async_time:.3f}s, 同步={sync_time:.3f}s"
