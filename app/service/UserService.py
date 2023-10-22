import bcrypt
from starlette.responses import JSONResponse

from app.common.util import create_access_token
from app.models import SnsType, UserToken
from app.repository.UserDAO import *
from app import models
from app.error import exceptions as ex

async def user_login(sms_type : models.SnsType, user_info : models.UserRegister, session : Session):
    if sms_type == SnsType.email:
        user = get_user_email(session, user_info.email)
        if len(user) == 1:
            is_verified = bcrypt.checkpw(user_info.pw.encode("utf-8"), user[0].pw)
            if is_verified:
                token = dict(
                    Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(user[0]).dict(exclude={'pw', 'marketing_agree'}), )}")
                return token
            else:
                return JSONResponse(status_code=400, content=dict(
                    msg = "패스워드가 틀렸습니다."
                ))
        else:
            raise ex.TokenDecodeEx()
            #return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))






async def user_register(sns_type : models.SnsType, user_info : models.UserRegister, session:Session):

    if sns_type.email == sns_type:
        user_exist = get_user_email(session,email=user_info.email)
        if len(user_exist) == 0 :
            user_info_dict = user_info.dict()
            pw = user_info_dict.pop('pw')
            hash_pw = bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt())
            user = create_user(session, hash_pw, user_info_dict)
            token = dict(Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(user).dict(exclude={'pw', 'marketing_agree'}),)}")
            return token

        else :
            return JSONResponse(
                status_code=400, content=(dict(msg = "이메일 중복"))
            )

        # user = Users(**user_info.dict())
        # print(user.email)
        # print(user.pw)

