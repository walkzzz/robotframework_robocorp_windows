# robotframework_robocorp_windows/utils/locator_utils.py

"""
定位器工具函数，用于验证和处理控件定位器
"""


class LocatorUtils:
    """定位器工具类，提供定位器验证和处理功能"""
    
    # 支持的定位策略
    SUPPORTED_LOCATOR_STRATEGIES = {
        'name',      # 控件名称
        'id',        # 控件ID
        'class',     # 控件类名
        'text',      # 控件文本
        'xpath',     # XPath定位
        'index',     # 控件索引
        'executable' # 可执行文件名
    }
    
    @classmethod
    def validate_locator(cls, locator):
        """验证定位器格式是否有效
        
        Args:
            locator: 要验证的定位器字符串
            
        Returns:
            tuple: (is_valid, message)
            - is_valid: 定位器是否有效
            - message: 验证结果消息
        """
        if not isinstance(locator, str):
            return False, f"Locator must be a string, got {type(locator).__name__}"
        
        if not locator:
            return False, "Locator cannot be empty"
        
        # 检查定位器是否包含支持的策略前缀
        if locator.count(':') >= 1:
            strategy = locator.split(':', 1)[0].strip()
            if strategy in cls.SUPPORTED_LOCATOR_STRATEGIES:
                return True, f"Valid locator with strategy: {strategy}"
            else:
                return False, f"Invalid locator strategy: {strategy}. Valid strategies: {', '.join(cls.SUPPORTED_LOCATOR_STRATEGIES)}"
        else:
            # 没有策略前缀，默认使用name策略
            return True, "Valid locator (using default 'name' strategy)"
    
    @classmethod
    def validate_locator_format(cls, locator):
        """验证定位器格式是否有效，并在无效时抛出异常
        
        Args:
            locator: 要验证的定位器字符串
            
        Raises:
            ValueError: 定位器格式无效时
        """
        is_valid, message = cls.validate_locator(locator)
        if not is_valid:
            raise ValueError(message + f". Valid locator formats: {', '.join([f'{strategy}:value' for strategy in cls.SUPPORTED_LOCATOR_STRATEGIES])}")
        return message
    
    @classmethod
    def get_locator_strategy(cls, locator):
        """获取定位器的策略
        
        Args:
            locator: 定位器字符串
            
        Returns:
            tuple: (strategy, value)
            - strategy: 定位策略
            - value: 定位值
        """
        if ':' in locator:
            strategy, value = locator.split(':', 1)
            return strategy.strip(), value.strip()
        # 默认使用name策略
        return 'name', locator
    
    @classmethod
    def format_locator(cls, strategy, value):
        """格式化定位器字符串
        
        Args:
            strategy: 定位策略
            value: 定位值
            
        Returns:
            str: 格式化后的定位器
        """
        if strategy not in cls.SUPPORTED_LOCATOR_STRATEGIES:
            raise ValueError(f"Invalid locator strategy: {strategy}")
        return f"{strategy}:{value}"
    
    @classmethod
    def get_supported_strategies(cls):
        """获取支持的定位策略列表
        
        Returns:
            list: 支持的定位策略列表
        """
        return sorted(list(cls.SUPPORTED_LOCATOR_STRATEGIES))
    
    @classmethod
    def get_valid_locator_examples(cls):
        """获取有效的定位器示例
        
        Returns:
            list: 有效的定位器示例列表
        """
        examples = [
            "name:OKButton",
            "id:12345",
            "class:Edit",
            "text:Hello, World!",
            "xpath://div[@id='container']/button[1]",
            "index:0",
            "executable:notepad.exe"
        ]
        return examples


# 创建工具类实例，方便直接使用
locator_utils = LocatorUtils()