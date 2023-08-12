from typing import Optional
from dataclasses import dataclass, asdict
from fastapi import FastAPI
from app.common.config import conf
import uvicorn
from app.database.conn import db
from app.router import index, auth

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


    #라우터 정의
    app.include_router(index.router)
    app.include_router(auth.router)
    return app

app = create_app()

if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
