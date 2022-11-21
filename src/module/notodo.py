from threading import Thread
from typing import Optional

import uvicorn as uvicorn

from module.asset import APP_DESCRIPTION, APP_NAME, VERSION_NUM, VERSION_STR
from module.database import Database
from module.exception import PortInUseError
from module.global_dict import Global
from module.http_server import HttpServer
from module.logger_ex import LoggerEx, LogLevel
from module.user_config import UserConfig
from module.utils import is_port_in_use, kill_thread


class NOToDo:
    """主功能模块"""

    def __init__(self, config: UserConfig):
        """初始化"""
        self.config = config

        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        # 一定要严格按照顺序初始化，否则可能会出现异常
        self.database = Database(self.config.mongodb.uri)
        Global().database = self.database
        self.http_app = HttpServer()
        self.http_thread: Optional[Thread] = None

        # 打印版本信息
        self.log.info(f'{APP_NAME} - {APP_DESCRIPTION}')
        self.log.info(f'Version: {VERSION_STR}')
        self.log.debug(f'Version Num: {VERSION_NUM}')

    def start(self) -> None:
        """启动NOToDo"""
        if is_port_in_use(self.config.server.port):  # 检查端口是否被占用
            raise PortInUseError(f'Port {self.config.server.port} already in use')
        self.database.connect()
        self.start_asgi()

    def stop(self) -> None:
        """停止NOToDo"""
        self.log.debug(f'{APP_NAME} stopping.')
        self.stop_asgi()
        self.database.close()
        self.log.info(f'{APP_NAME} stopped, see you next time.')

    def start_asgi(self) -> None:
        """启动ASGI"""
        self.log.debug(f'{APP_NAME} starting ASGI.')
        self.http_thread = Thread(
            target=uvicorn.run,
            daemon=True,
            kwargs={
                'app': self.http_app,
                'host': self.config.server.host,
                'port': self.config.server.port,
                'log_level': 'warning' if Global().debug_mode else 'critical',
            }
        )
        self.http_thread.start()

    def stop_asgi(self) -> None:
        """停止ASGI"""
        self.log.debug(f'{APP_NAME} stopping ASGI.')
        if isinstance(self.http_thread, Thread) and self.http_thread.is_alive():
            kill_thread(self.http_thread)
