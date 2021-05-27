from datetime import date
from os import name

from fastapi.exceptions import FastAPIError
from sqlalchemy.sql.sqltypes import Enum
from database import Base
from pydantic import Field,BaseModel


#this is the structure of our JSON file sent from a web

#for authorization/registration
class Role(str):
    ADMIN = "admin"
    ARTIST = "artist"
    USER = "user"


class BaseUser(BaseModel):
    email:str
    username: str
    role:Role

class UserCreate(BaseUser):
    password:str
    # role:Role


class User(BaseUser):
    id:int 
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token:str
    token_type:str = "bearer"


class BaseInformation(BaseModel):
    name:str
    surname:str
    instagram_bio:str
    phone_number:str


class UserInfoUpdate(BaseInformation):
    pass

class UserInfoCreate(BaseInformation):
    register_date:date

class UserInfo(BaseInformation):

    class Config:
        orm_mode=True

class UserInfoUpdateAdmin(BaseInformation):
    subscription:bool
    register_date:date

class UploadPreset(BaseModel):
    title:str
    description:str
    #created_at:date

class LutStatus(str):
    Verified="Verified"
    Unverified="Unverified"
    Delete="Delete"