import jwt
from app.common.consts import JWT_ALGORITHM, JWT_SECRET
from datetime import datetime, date, timedelta


def create_access_token(*, data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:

        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM
                             )
    return encoded_jwt




class D:
    def __init__(self, *args):
        self.utc_now = datetime.utcnow()
        self.timedelta = 0

    @classmethod
    def datetime(cls, diff: int=0) -> datetime:
        return cls().utc_now + timedelta(hours=diff) if diff > 0 else cls().utc_now + timedelta(hours=diff)

    @classmethod
    def date(cls, diff: int=0) -> date:
        return cls.datetime(diff=diff).date()

    @classmethod
    def date_num(cls, diff: int=0) -> int:
        return int(cls.date(diff=diff).strftime('%Y%m%d'))
