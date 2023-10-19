import time
import typing
import jwt
import re


from fastapi.params import Header
from jwt import PyJWTError
from pydantic import BaseModel
from starlette.requests import Request
from starlette.datastructures import URL, Headers
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse, RedirectResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from app.common import config
from app.common.config import conf
from app.models import UserToken

from app.common.util import D
from app.common import consts


class AccessControl:
    def __init__(
        self,
        app: ASGIApp,
        except_path_list: typing.Sequence[str] = None,
        except_path_regex: str = None,
    ) -> None:
        if except_path_list is None:
            except_path_list = ["*"]
        self.app = app
        self.except_path_list = except_path_list
        self.except_path_regex = except_path_regex

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        print(self.except_path_regex)
        print(self.except_path_list)

        request = Request(scope=scope)
        headers = Headers(scope=scope)

        request.state.start = time.time()
        request.state.inspect = None
        request.state.user = None
        request.state.is_admin_access = None

        # User 아이피 체크한다.
        ip_from = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else None

        #URL 패턴 체크를 한다.
        if await self.url_pattern_check(request.url.path, self.except_path_regex) or request.url.path in self.except_path_list:
            return await self.app(scope, receive, send)


        #API
        if request.url.path.startswith("/api"):
            print("이거")
            print(request.headers)
            # api 인경우 헤더로 토큰 검사
            if "authorization" in request.headers.keys():
                request.state.user = await self.token_decode(access_token=request.headers.get("authorization"))
                # 토큰 없음
            else:
                if "authorization" not in request.headers.keys():
                    response = JSONResponse(status_code=401, content=dict(msg="AUTHORIZATION_REQUIRED"))
                    return await response(scope, receive, send)
        else:
            print("저거")

            # 템플릿 렌더링인 경우 쿠키에서 토큰 검사
            print(request.cookies)
            # request.cookies["Authorization"] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTQsImVtYWlsIjoia29hbGFAZGluZ3JyLmNvbSIsIm5hbWUiOm51bGwsInBob25lX251bWJlciI6bnVsbCwicHJvZmlsZV9pbWciOm51bGwsInNuc190eXBlIjpudWxsfQ.4vgrFvxgH8odoXMvV70BBqyqXOFa2NDQtzYkGywhV48"

            if "Authorization" not in request.cookies.keys():
                response = JSONResponse(status_code=401, content=dict(msg="AUTHORIZATION_REQUIRED"))
                return await response(scope, receive, send)

            request.state.user = await self.token_decode(access_token=request.cookies.get("Authorization"))

        request.state.req_time = D.datetime()
        print(D.datetime())
        print(D.date())
        print(D.date_num())

        print(request.cookies)
        print(headers)
        res = await self.app(scope, receive, send)
        print()
        print()
        return res

    #URL 패턴 체크하는 방법
    @staticmethod
    async def url_pattern_check(path, pattern):

        result = re.match(pattern, path)
        print(result)
        if result:
            return True
        return False

    @staticmethod
    async def token_decode(access_token):
        """
        :param access_token:
        :return:
        """
        try:
            access_token = access_token.replace("Bearer ", "")
            payload = jwt.decode(access_token, key=consts.JWT_SECRET, algorithms=[consts.JWT_ALGORITHM])
        except PyJWTError as e:
            print("에러 발생 : ", e)
            # Raise Error
        return payload
