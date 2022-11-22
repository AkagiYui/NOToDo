from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from module.database.user import User
from module.global_dict import Global
from module.http_server.http_result import HttpResult
from module.http_server.jwt_manager import JWTManager
from module.http_server.model.check_username_valid_model import \
    CheckUsernameValidModel
from module.http_server.model.login_request_model import LoginRequestModel
from module.http_server.model.register_request_model import \
    RegisterRequestModel
from module.logger_ex import LoggerEx, LogLevel
from module.utils import hmac_sha1


class UserController(APIRouter):
    """信息接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(prefix='/user', *args, **kwargs)
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} Initializing...')

        self.add_api_route(response_model=HttpResult, path='/login', endpoint=self.login,
                           methods=['POST'], name='登录')
        self.add_api_route(response_model=HttpResult, path='/register', endpoint=self.register,
                           methods=['POST'], name='注册')
        self.add_api_route(response_model=HttpResult, path='/username-available', endpoint=self.is_username_available,
                           methods=['GET'], name='检查用户名是否未注册并可用')
        self.add_api_route(response_model=HttpResult, path='/info', endpoint=self.get_user_info,
                           methods=['GET'], name='获取用户信息')

    async def login(self, lrm: LoginRequestModel) -> JSONResponse:
        """登录，返回JWT"""
        if User.is_password_correct(lrm.username, hmac_sha1(lrm.username, lrm.password)):
            self.log.info(f'login success: {lrm.username}')
            return HttpResult.success(JWTManager.create_jwt(lrm.username))
        return HttpResult.no_auth('用户名或密码错误')

    async def register(self, rrm: RegisterRequestModel) -> JSONResponse:
        """注册"""
        if User.is_username_exist(rrm.username):
            return HttpResult.bad_request('用户名已存在')
        encrypted_password = hmac_sha1(rrm.username, rrm.password)
        new_user = User(
            username=rrm.username,
            password=encrypted_password,
            nickname=rrm.nickname,
            email=rrm.email
        )
        if new_user.save(force_insert=True):
            self.log.info(f'new register user: {new_user.id}')
            return HttpResult.success()
        return HttpResult.error()

    async def is_username_available(self, cuv: CheckUsernameValidModel) -> JSONResponse:
        """检查用户名是否合法"""
        self.log.info(f'check username: {cuv.username}')
        return HttpResult.success(not User.is_username_exist(cuv.username))

    async def get_user_info(self, req: Request) -> JSONResponse:
        """获取用户信息"""
        user: User = req.state.user
        self.log.info(f'get user info: {user}')
        return HttpResult.success(User.get_user_information(user.username))
