from datetime import datetime

from app.models import UserRegister
from sqlalchemy.orm import Session
from app.database.schema import  Users
def create_user(db : Session, pw , user_info : dict):
    user = Users(pw=pw, **user_info)
    db.add(user)
    db.commit()
    return user



def get_user(db : Session, id : int):
    return db.get(Users, id)

def get_user_all(db : Session):
    return db.query(Users).all()

def get_user_email(db : Session, email : str):
    return db.query(Users).filter(Users.email == email).all()