from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import APIRouter, Depends

# TODO:
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import models
from app.common.consts import JWT_SECRET, JWT_ALGORITHM
from app.common.util import create_access_token
from app.database.conn import db
from app.database.schema import Users
from app.models import SnsType, Token, UserToken

from app.service.UserService import user_login, user_register
from starlette import status

"""
1. 구글 로그인을 위한 구글 앱 준비 (구글 개발자 도구)
2. FB 로그인을 위한 FB 앱 준비 (FB 개발자 도구)
3. 카카오 로그인을 위한 카카오 앱준비( 카카오 개발자 도구)
4. 이메일, 비밀번호로 가입 (v)
5. 가입된 이메일, 비밀번호로 로그인, (v)
6. JWT 발급 (v)

7. 이메일 인증 실패시 이메일 변경
8. 이메일 인증 메일 발송
9. 각 SNS 에서 Unlink 
10. 회원 탈퇴
11. 탈퇴 회원 정보 저장 기간 동안 보유(법적 최대 한도차 내에서, 가입 때 약관 동의 받아야 함, 재가입 방지 용도로 사용하면 가능)
"""


router = APIRouter()


@router.post("/auth/register/{sns_tpe}", status_code=200, response_model=Token)
async def register(sns_type: SnsType, reg_info: models.UserRegister, session: Session = Depends(db.session)):
    """
    회원가입 API
    :param sns_type:
    :param reg_info:
    :param session:
    :return:
    """
    return await user_register(sns_type, reg_info, session)


@router.post("/auth/login/{sns_type}", status_code=200)
async def login(sns_type: SnsType, user_info : models.UserRegister, session: Session = Depends(db.session)):
    print(user_info)
    print(session)
    return await user_login(sns_type, user_info, session)


