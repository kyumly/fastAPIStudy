import jwt
from app.common.consts import JWT_ALGORITHM, JWT_SECRET


def create_access_token(*, data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        from datetime import datetime
        from datetime import timedelta
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM
                             )
    return encoded_jwt
