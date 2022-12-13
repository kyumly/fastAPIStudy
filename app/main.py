from typing import Optional

from fastapi import FastAPI
from app.common.config import conf
import uvicorn


def create_app():
    """
    앱 함수 실행
    :return:
    """

    c = conf()
    app = FastAPI()

    #데이터베이스 init

    #레이디 init

    #미들웨어 정의


    #라우터 정의

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
