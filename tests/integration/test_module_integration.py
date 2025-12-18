# tests/integration/test_module_integration.py

"""
集成测试，验证模块间的交互是否正常工作
"""

import pytest
from unittest.mock import MagicMock, patch
from robotframework_robocorp_windows.library import RobocorpWindows
from robotframework_robocorp_windows.services.window_service import WindowService
from robotframework_robocorp_windows.services.control_service import ControlService
from robotframework_robocorp_windows.drivers.robocorp_driver import RobocorpWindowsDriver


class TestModuleIntegration:
    """测试模块集成"""
    
    def test_keyword_to_service_integration(self):
        """测试关键字到服务层的集成"""
        # 创建库实例
        lib = RobocorpWindows()
        
        # 模拟窗口和控件
        mock_window = MagicMock()
        mock_window.name = "Test Window"
        mock_control = MagicMock()
        
        # 设置当前窗口
        lib.current_window = mock_window
        
        # 模拟服务层
        with patch.object(lib.control_operations.control_service.driver, 'find_control', return_value=mock_control):
            # 调用关键字
            control = lib.control_operations.find_control("test_control")
            
            # 验证服务层被调用
            assert control == mock_control
    
    def test_service_to_driver_integration(self):
        """测试服务层到驱动层的集成"""
        # 创建服务实例
        control_service = ControlService()
        
        # 模拟驱动层
        with patch.object(control_service.driver, 'find_control') as mock_find_control:
            mock_control = MagicMock()
            mock_find_control.return_value = mock_control
            
            # 调用服务方法
            mock_window = MagicMock()
            control = control_service.find_control(mock_window, "test_control")
            
            # 验证驱动层被调用
            mock_find_control.assert_called_once()
            assert control == mock_control
    
    def test_full_call_chain(self):
        """测试完整的调用链：关键字→服务→驱动"""
        # 创建库实例
        lib = RobocorpWindows()
        
        # 模拟窗口和控件
        mock_window = MagicMock()
        mock_window.name = "Test Window"
        mock_control = MagicMock()
        
        # 设置当前窗口
        lib.current_window = mock_window
        
        # 模拟驱动层
        with patch.object(lib.control_operations.control_service.driver, 'find_control', return_value=mock_control):
            with patch.object(lib.control_operations.control_service, 'click_control') as mock_click_control:
                # 调用点击控件关键字
                lib.control_operations.click_control("test_control")
                
                # 验证完整调用链
                lib.control_operations.control_service.driver.find_control.assert_called_once()
                mock_click_control.assert_called_once_with(mock_control)
    
    def test_window_service_integration(self):
        """测试窗口服务的集成"""
        # 创建服务实例
        window_service = WindowService()
        
        # 模拟驱动层
        with patch.object(window_service.driver, 'launch_application', return_value="test_app.exe"):
            with patch.object(window_service.driver, 'find_window_by_executable', return_value=MagicMock()):
                # 调用服务方法
                executable_name, window = window_service.launch_application("test_app.exe")
                
                # 验证结果
                assert executable_name == "test_app.exe"
                assert window is not None
    
    def test_cache_integration(self):
        """测试缓存机制的集成"""
        # 创建库实例
        lib = RobocorpWindows()
        
        # 模拟窗口和控件
        mock_window = MagicMock()
        mock_window.name = "Test Window"
        mock_control = MagicMock()
        
        # 设置当前窗口
        lib.current_window = mock_window
        
        # 模拟驱动层
        with patch.object(lib.control_operations.control_service.driver, 'find_control', return_value=mock_control) as mock_find_control:
            # 第一次调用，应该从驱动层获取
            control1 = lib.control_operations.find_control("test_control")
            assert mock_find_control.call_count == 1
            
            # 第二次调用，应该从缓存获取
            control2 = lib.control_operations.find_control("test_control")
            assert mock_find_control.call_count == 1  # 调用次数不变，说明使用了缓存
            assert control1 == control2
    
    def test_async_operations_integration(self):
        """测试异步操作的集成"""
        # 创建库实例
        lib = RobocorpWindows()
        
        # 模拟窗口和控件
        mock_window = MagicMock()
        mock_window.name = "Test Window"
        mock_control = MagicMock()
        
        # 设置当前窗口
        lib.current_window = mock_window
        
        # 模拟驱动层
        with patch.object(lib.async_control_operations.control_service.driver, 'find_control', return_value=mock_control):
            # 调用异步关键字
            task_id = lib.async_control_operations.async_click_control("test_control")
            
            # 验证任务ID是整数
            assert isinstance(task_id, int)
    
    def test_exception_propagation(self):
        """测试异常从驱动层到关键字层的传播"""
        # 创建库实例
        lib = RobocorpWindows()
        
        # 模拟窗口
        mock_window = MagicMock()
        lib.current_window = mock_window
        
        # 模拟驱动层抛出异常
        from robotframework_robocorp_windows.utils.exceptions import ControlNotFoundError
        with patch.object(lib.control_operations.control_service.driver, 'find_control', side_effect=ControlNotFoundError("Control not found")):
            # 调用关键字，应该抛出AssertionError
            with pytest.raises(AssertionError):
                lib.control_operations.find_control("test_control")
