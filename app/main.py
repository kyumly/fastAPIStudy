from typing import Optional
from dataclasses import dataclass, asdict
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.common.config import conf
import uvicorn
from app.database.conn import db
from app.middlewares.token_validator import AccessControl
from app.router import index, auth
from app.middlewares.trusted_hosts import TrustedHostMiddleware

from app.common.consts import EXCEPT_PATH_LIST,EXCEPT_PATH_REGEX


def create_app():
    """
    앱 함수 실행
    :return:
    """

    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)

    print(conf_dict)
    # 데이터베이스 init
    db.init_app(app, **conf_dict)

    #레이디 init

    #미들웨어 정의
    app.add_middleware(AccessControl, except_path_list=EXCEPT_PATH_LIST, except_path_regex=EXCEPT_PATH_REGEX)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=conf().TRUSTED_HOSTS, except_path=["/health"])

    #라우터 정의
    app.include_router(index.router)
    app.include_router(auth.router)
    return app

app = create_app()

if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, workers=4)
