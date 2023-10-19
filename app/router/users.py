from fastapi import APIRouter, Depends
from starlette.requests import  Request

from app.database.conn import db
from app.models import UserMe
from app.repository.UserDAO import *


router = APIRouter()


@router.get("/me", response_model=UserMe)
async def get_user_router(req : Request, session: Session = Depends(db.session)):
    print(session)
    user = req.state.user
    user_info = get_user(session, user['id'])
    return user_info
