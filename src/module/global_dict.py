"""全局字典，存放一些共同使用的数据"""
import platform
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Sequence

import psutil

from module.asset import APP_NAME, VERSION_STR, ServerStatus
from module.singleton_type import SingletonType
from module.utils import (get_script_memory_usage, get_script_uptime,
                          get_system_description, get_system_memory_usage,
                          get_system_uptime)

if TYPE_CHECKING:
    from module.database import Database
    from module.notodo import NOToDo as App
    from module.user_config import UserConfig


class Global(metaclass=SingletonType):
    """全局变量，单例模式"""

    ############
    # 全局的变量 #
    ############

    exit_code = 0  # 退出码
    time_to_exit = False  # 是时候退出了
    debug_mode = False  # 调试模式

    ############
    # 共享的对象 #
    ############

    user_config: 'UserConfig' = None  # 用户配置
    database: 'Database' = None  # 数据库
    application: Optional['App'] = None  # 应用程序

    args_known = ()  # 命令行参数
    args_unknown = ()  # 未知命令

    ############
    # 目录与路径 #
    ############

    root_dir = Path('.')  # 根目录
    # asset_dir = Path(root_dir, 'assets')  # 静态资源目录
    # download_dir = Path(root_dir, 'downloads')  # 下载目录

    def __init__(self):
        """初始化"""
        # 创建目录
        need_create_dirs: Sequence[Path] = ()
        for dir_ in need_create_dirs:
            dir_.mkdir(parents=True, exist_ok=True)

    @property
    def information(self) -> ServerStatus:
        """获取应用信息"""
        return ServerStatus(
            python_version=platform.python_version(),
            system_description=get_system_description(),

            system_cpu_present=psutil.cpu_percent(),
            system_memory_usage=get_system_memory_usage(),
            script_memory_usage=get_script_memory_usage(),

            system_uptime=get_system_uptime(),
            script_uptime=get_script_uptime(),

            app_name=APP_NAME,
            version=VERSION_STR,
        )


if __name__ == '__main__':
    print(Global().debug_mode)
