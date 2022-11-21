from mongoengine import Document, StringField


class User(Document):
    """用户"""
    username = StringField(required=True)  # 用户名
    password = StringField(required=True)  # 密码
    nickname = StringField()  # 昵称
    email = StringField(required=True)  # 邮箱
