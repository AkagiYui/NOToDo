from inspect import get_annotations
from typing import Any

from dotenv import dotenv_values
from pydantic import BaseModel

from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel
from module.singleton_type import SingletonType
from module.utils import deep_iter, put_into_dict
from module.yaml_config import YamlConfig


class UserConfig(metaclass=SingletonType):
    """用户配置"""

    class __Server(BaseModel):
        host: str = '127.0.0.1'  # 监听地址
        port: int = 80  # 监听端口
    server: __Server = __Server()

    def __init__(self, file_path):
        """初始化"""
        self.log = LoggerEx(self.__class__.__name__)
        self.file_path = file_path
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.load()

    def load(self) -> None:
        """加载配置"""
        self.log.debug(f'Loading config file: {self.file_path}')

        try:
            config_data = dict(YamlConfig(self.file_path))
            self.log.debug(f'Config file loaded: {config_data}')
        except FileNotFoundError:
            self.log.warning('Config file not found, using default config')
            config_data = {}
        except TypeError:
            self.log.error('Config file is not a valid yaml file, using default config')
            config_data = {}

        env_config: dict[str, str] = dict(dotenv_values('.env'))
        self.log.debug(f'Env config loaded: {env_config}')
        for k, v in env_config.items():
            match k:
                case 'SERVER_HOST':
                    put_into_dict(config_data, ('server', 'host'), str(v))
                case 'SERVER_PORT':
                    put_into_dict(config_data, ('server', 'port'), int(v))

        # 应用配置
        for k, v in deep_iter(config_data):
            match k:
                case ('server', 'host'):
                    self.server.host = str(v)
                case ('server', 'port'):
                    self.server.port = int(v)
                case _:
                    self.log.warning(f'Unknown config item: {k}')

        self.log.debug(f'Final config loaded: {self.to_dict()}')

    @staticmethod
    def to_dict() -> dict[str, Any]:
        """将配置转换为字典"""
        annotations = get_annotations(UserConfig)
        return {k: getattr(UserConfig, k).dict() for k in annotations}
