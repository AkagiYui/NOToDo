"""资源类"""


from .constant import (APP_DESCRIPTION, APP_NAME, AUTHOR_NAME, JWT_SECRET,
                       VERSION_NUM, VERSION_STR)
from .server_status import ServerStatus

__all__ = [
    'APP_NAME',
    'APP_DESCRIPTION',
    'AUTHOR_NAME',
    'VERSION_NUM',
    'VERSION_STR',
    'JWT_SECRET',
    'ServerStatus',
]
