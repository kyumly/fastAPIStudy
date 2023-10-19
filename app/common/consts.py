# DB_URL:str ="mysql+pymysql://root:rootpw@localhost/fastapi?charset=utf8mb4"
DB_URL:str ="sqlite:///../myapi.db"
JWT_SECRET = "ABCD1234!"
JWT_ALGORITHM = "HS256"

EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/redoc|/auth)"


