"""工具类"""
import base64
import contextlib
import ctypes
import hashlib
import hmac
import os
import platform
import socket
from datetime import datetime
from math import inf
from threading import Thread
from typing import Any, Generator, Hashable, Sequence, Union

import distro
import psutil


def is_port_in_use(_port: int, _host: str = '127.0.0.1') -> bool:
    """检查端口是否被占用

    :param _port: 端口号
    :param _host: 主机名
    :return: True/False
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((_host, _port))
        return True
    except OSError:
        return False
    finally:
        if s:
            s.close()


def base_64(file_data: bytes) -> str:
    """计算base64编码"""
    return base64.b64encode(file_data).decode()


def checksum(file: Union[str, bytes], hash_factory=hashlib.md5, chunk_num_blocks=128) -> str:
    """计算校验和

    :param file: 文件路径或文件内容
    :param hash_factory: 哈希算法
    :param chunk_num_blocks: 分块数
    """
    h = hash_factory()
    if isinstance(file, str):
        with open(file, 'rb') as _f:
            while chunk := _f.read(chunk_num_blocks * h.block_size):
                h.update(chunk)
    elif isinstance(file, bytes):
        h.update(file)
    else:
        raise TypeError(f'{type(file)} is not supported')
    return h.hexdigest()


def change_console_title(title: str) -> None:
    """Windows 平台修改控制台标题"""
    with contextlib.suppress(Exception):
        ctypes.windll.kernel32.SetConsoleTitleW(title)


def get_system_description() -> str:
    """获取系统版本"""
    system = platform.system().strip().lower()
    if system.startswith('win'):
        platform_system = 'Windows'
        platform_version = platform.version()
    else:
        platform_system = distro.name(True)
        platform_version = ''
    return f'{platform_system} {platform_version} {platform.machine().strip()}'


def get_system_memory_usage(round_: int = 4) -> float:
    """获取系统内存使用率

    :param round_: 保留小数位数
    """
    platform_memory = psutil.virtual_memory()
    platform_memory_usage = 1 - platform_memory.available / platform_memory.total
    platform_memory_usage *= 100
    return round(platform_memory_usage, round_)


def get_script_memory_usage(round_: int = 4) -> float:
    """获取脚本内存占用率

    :param round_: 保留小数位数
    """
    self_process = psutil.Process(os.getpid())
    return round(self_process.memory_percent(), round_)


def get_system_uptime() -> str:
    """获取系统运行时间

    :return: 系统运行时间 like: 24 days, 18:30:43
    """
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    curr_time = datetime.now()
    uptime = curr_time - boot_time
    return str(uptime).split('.')[0]


def get_script_uptime() -> str:
    """获取脚本运行时间

    :return: 脚本运行时间 like: 24
    """
    self_process = psutil.Process(os.getpid())
    curr_time = datetime.now()
    start_time = self_process.create_time()
    start_time = datetime.fromtimestamp(start_time)
    uptime = curr_time - start_time
    return str(uptime).split('.')[0]


def kill_thread(thread: Thread) -> None:
    """强制结束线程，注意不得设计为对象方法！"""
    if not (thread.is_alive() and thread.ident):
        return
    tid = ctypes.c_long(thread.ident)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit))
    if res == 0:
        raise ValueError('invalid thread id')
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError('PyThreadState_SetAsyncExc failed')


def deep_iter(data: Any, depth=inf, current_depth=1) -> Generator:
    """
    递归深度遍历数据

    :param data: 数据
    :param depth: 遍历深度，默认无限深度
    :param current_depth: 当前深度
    """
    if isinstance(data, dict) and (depth and current_depth <= depth):
        for key, value in data.items():
            for child_path, child_value in deep_iter(value, depth=depth, current_depth=current_depth + 1):
                yield (key, *child_path), child_value
    else:
        yield tuple(), data


def put_into_dict(dict_: dict, path: Sequence[Hashable], value: Any) -> None:
    """将数据放入字典

    :param dict_: 字典
    :param path: 路径
    :param value: 值
    """
    if not path:
        return
    current_key = path[0]
    if len(path) == 1:
        dict_[current_key] = value
    else:
        if current_key not in dict_:
            dict_[current_key] = {}
        put_into_dict(dict_[current_key], path[1:], value)


def hmac_sha1(key: str, data: str) -> str:
    """计算HMAC-SHA1"""
    return hmac.new(key.encode(), data.encode(), hashlib.sha1).hexdigest()


if __name__ == '__main__':
    for i in deep_iter({
        'a': {
            'b': {
                'c': 'd',
                'e': {
                    'f': 'g'
                }
            },
            'e': 'f'
        },
    }):
        print(i)
