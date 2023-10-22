from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette.requests import Request
from inspect import currentframe as frame


from app.database.conn import db
from app.database.schema import Users

router = APIRouter()


@router.get("/")
async def index(session : Session = Depends(db.session)):
    """
    ELB 상태 체크용 API
    :return:
    """
    """
        원래
        user = Users(status="active")
        session.add(user)
        session.commit()
    """
    Users().create(session, auto_commit=True, name="코알라")
    current_time = datetime.utcnow()
    print("asd")
    return Response(f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")


@router.get("/index")
async def test(session : Session = Depends(db.session)):
    print(Users.get(id = 1, status= "active"))
    #current_time = datetime.utcnow()
    #print("asd")
    #return Response(f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")


@router.get("/test2")
async def index(request: Request):
    """
    ELB 상태 체크용 API
    :return:
    """
    try:
        a = 1/0
        #print("유저 정보 : ", request.state.user)
    except Exception as e:
        #request.state.inspect = frame()
        raise e

    current_time = datetime.utcnow()
    return Response(f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")


