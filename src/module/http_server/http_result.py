from typing import Any

from pydantic import BaseModel, Field
from starlette.responses import JSONResponse


class HttpResult(BaseModel):
    """HTTP请求结果类"""

    code: int = Field(..., example=200)  # 响应码
    msg: str = Field(..., example='')  # 响应信息
    data: Any = Field(None, example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC'
                                    'J9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXh'
                                    'wIjoxNjY1MDQ1MjExfQ.y4mM2P5lhReMfa'
                                    'Ubkp-3laMJ0weWiIAeNsSqbB_c9J8')  # 响应数据

    @staticmethod
    def success(data=None, msg='', code=200) -> JSONResponse:
        """200"""
        return JSONResponse(content=HttpResult(code=code, msg=msg, data=data).dict(), status_code=code)

    @staticmethod
    def nothing_changed(msg='Nothing changed.') -> JSONResponse:
        """304"""
        return JSONResponse(content=HttpResult(code=304, msg=msg).dict(), status_code=304)

    @staticmethod
    def bad_request(msg='Bad request.') -> JSONResponse:
        """400"""
        return JSONResponse(content=HttpResult(code=400, msg=msg).dict(), status_code=400)

    @staticmethod
    def no_auth(msg='Not authorized.') -> JSONResponse:
        """401"""
        return JSONResponse(content=HttpResult(code=401, msg=msg).dict(), status_code=401)

    @staticmethod
    def forbidden(msg='Forbidden.') -> JSONResponse:
        """403"""
        return JSONResponse(content=HttpResult(code=403, msg=msg).dict(), status_code=403)

    @staticmethod
    def not_found(msg='Not found.') -> JSONResponse:
        """404"""
        return JSONResponse(content=HttpResult(code=404, msg=msg).dict(), status_code=404)

    @staticmethod
    def error(msg='System error.', code=500) -> JSONResponse:
        """500"""
        return JSONResponse(content=HttpResult(code=code, msg=msg).dict(), status_code=code)
