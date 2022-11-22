import time
from typing import Union

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError, JWTError
from jose.exceptions import JWTClaimsError
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from module.asset import APP_NAME
from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel

from .controller.user_controller import UserController
from .http_result import HttpResult
from .jwt_manager import JWTManager


class HttpServer(FastAPI):
    """HTTP服务器"""

    def __init__(self):
        """初始化"""
        super().__init__(
            docs_url='/docs',  # 文档地址
            redoc_url=None,  # 关闭redoc文档
            title=APP_NAME,  # 文档标题
            openapi_tags=[
                {'name': 'User', 'description': '用户操作'},
            ]
        )
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} initializing...')

        self.add_event_handler('startup', func=self.server_startup)
        self.add_event_handler('shutdown', func=self.server_shutdown)
        self.add_middleware(BaseHTTPMiddleware, dispatch=self.http_middleware)
        self.add_middleware(
            CORSMiddleware,  # 跨域中间件
            allow_origins=[
                '*',
                'http://localhost',
                'http://localhost:3000',
            ],  # 允许跨域的来源
            allow_credentials=True,  # 允许跨域的cookie
            allow_methods=['*'],  # 允许跨域的方法
            allow_headers=['*'],  # 允许跨域的头
        )
        self.add_exception_handler(HTTPException, handler=self.exception_handler_ex)
        self.add_exception_handler(RequestValidationError, handler=self.exception_handler_ex)

        self.router.add_api_route('/', self.route_root, methods=['GET'], include_in_schema=False)
        self.router.include_router(UserController(), tags=['User'])
        # self.router.include_router(AccountController(), tags=['Account'])

        self.no_token_path = {
            (self.docs_url, 'GET'),  # swagger
            (self.openapi_url, 'GET'),  # openapi
            ('/docs/oauth2-redirect', 'GET'),  # swagger oauth2
            ('/', 'GET'),  # 根路径
            ('/user/login', 'POST'),  # 登录
            ('/user/username-available', 'GET'),  # 用户名验证
            ('/user/register', 'POST'),  # 注册
        }  # 不需要token的路径

    @staticmethod
    async def exception_handler_ex(_: Request, exc: Union[HTTPException, RequestValidationError]) -> JSONResponse:
        """异常处理"""
        if isinstance(exc, HTTPException):
            if exc.status_code == 404:
                content = HttpResult.not_found(exc.detail)
            else:
                content = HttpResult.error(exc.detail, code=exc.status_code)
            return content
        return HttpResult.bad_request()

    async def server_startup(self) -> None:
        """事件 服务启动"""
        self.log.debug('HttpServer startup.')

    async def server_shutdown(self) -> None:
        """事件 服务关闭"""
        self.log.debug('HttpServer shutdown.')

    async def http_middleware(self, request: Request, call_next) -> JSONResponse:
        """请求中间件"""
        client = f'{request.client.host}:{request.client.port}'
        self.log.debug(f'{client} -> {request.method:.4s} {request.url.path} {request.query_params}')
        start_time = time.time()

        headers = request.headers
        token = headers.get('Authorization', '').replace('Bearer ', '')

        try:
            token = JWTManager.decode_jwt(token)
            user = token.get('username')
        except (JWTError, ExpiredSignatureError, JWTClaimsError):
            user = None
        request.state.user = user

        if not user and (request.url.path, request.method) not in self.no_token_path:
            response = HttpResult.no_auth('token无效')
        else:
            response = await call_next(request)

        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        self.log.debug(f'{client} <- {response.status_code} ProcessTime: {process_time:.3f}s')
        return response

    @staticmethod
    async def route_root() -> JSONResponse:
        """根路由"""
        return HttpResult.success(f'This is {APP_NAME}!')
