from enum import Enum

#from pydantic import BaseModel, validator
#from pydantic import BaseModel, validator
from pydantic import BaseModel, validator, EmailStr
from fastapi import HTTPException
#from pydantic.networks import EmailStr


class UserRegister(BaseModel):
    # pip install 'pydantic[email]'
    email: EmailStr
    pw: str

    @validator('pw', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise HTTPException(status_code=400, detail="빈값이 들어가면 안됩니다.")
        return v


class SnsType(str, Enum):
    email: str = "email"
    facebook: str = "facebook"
    google: str = "google"
    kakao: str = "kakao"


class Token(BaseModel):
    Authorization: str = None


class UserToken(BaseModel):
    id: int
    pw: str = None
    email: str = None
    name: str = None
    phone_number: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode = True
