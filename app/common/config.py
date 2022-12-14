from dataclasses import dataclass, asdict
from os import path, environ

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
print(base_dir)

@dataclass
class Config:
    """
    기본 Configuration
    """
    BASE_DIR = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True

@dataclass
class LocalConfig(Config):
    PROJ_RELOAD : bool = False
    DB_URL:str ="mysql+pymysql://root:rootpw@localhost/fastapi?charset=utf8mb4"


@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = True


def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig() , local=LocalConfig())
    return config.get(environ.get("API_ENV", "local"))

#딕셔너리로 변환해준다 => 클래스의 속성들을
#{'DB_POOL_RECYCLE': 900, 'DB_ECHO': True, 'PROJ_RELOAD': False}