import mongoengine

from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel


class Database:
    """数据库"""

    def __init__(self, uri: str):
        """初始化"""
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} initializing...')

        self.uri = uri

    def connect(self) -> bool:
        """连接数据库"""
        mongoengine.connect(host=self.uri)
        self.log.debug(f'Connected to database: {self.uri}')
        return True

    def close(self) -> bool:
        """关闭连接"""
        mongoengine.disconnect()
        self.log.debug(f'Disconnected from database: {self.uri}')
        return True
