from typing import Optional

from mongoengine import Document, StringField
from pymongo.errors import DuplicateKeyError


class User(Document):
    """用户"""

    username = StringField(required=True, unique=True)  # 用户名
    password = StringField(required=True)  # 密码
    nickname = StringField()  # 昵称
    email = StringField(required=True)  # 邮箱

    @classmethod
    def is_password_correct(cls, username: str, password: str) -> bool:
        """判断密码是否正确"""
        try:
            user = cls.objects(username=username).first()
        except DuplicateKeyError:
            return False
        if user is None:
            return False
        return user.password == password

    @classmethod
    def is_username_exist(cls, username: str) -> bool:
        """判断用户名是否存在"""
        try:
            return cls.objects(username=username).first() is not None
        except DuplicateKeyError:
            return True

    @classmethod
    def get_user_information(cls, username: str) -> Optional['User']:
        """获取用户信息"""
        try:
            user = cls.objects(username=username).first()
        except DuplicateKeyError:
            return None
        if user is None:
            return None
        return user
