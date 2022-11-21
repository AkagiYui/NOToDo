from datetime import datetime, timedelta

from jose import jwt

from module.asset import JWT_SECRET


class JWTManager:
    """JWT管理器"""

    @classmethod
    def create_jwt(cls, username: str) -> str:
        """创建JWT"""
        return jwt.encode({
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=2)
        }, JWT_SECRET, algorithm='HS256')

    @classmethod
    def decode_jwt(cls, token: str) -> dict:
        """解码JWT"""
        return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
