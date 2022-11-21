import threading


class SingletonType(type):
    """单例模式"""

    _instance_lock = threading.Lock()
    _instance = None

    def __call__(cls, *args, **kwargs) -> object:
        """创建实例"""
        if not cls._instance:  # 双重检查
            with cls._instance_lock:  # 线程安全
                if not cls._instance:  # 双重检查
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
