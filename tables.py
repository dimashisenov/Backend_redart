from collections import defaultdict, namedtuple
from datetime import datetime
from typing import Collection
from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relation, relationship
from sqlalchemy.sql import base
from sqlalchemy.sql.visitors import iterate
from database import engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role=Column(String)
    


class UserInfo(Base):
    __tablename__='information'

    name=Column(String)
    surname=Column(String)
    register_date=Column(String)
    subscription=Column(Boolean,default=False)
    instagram_bio=Column(String,primary_key=True)
    phone_number=Column(String,primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    user=relationship("User",backref='information')

class Lut(Base):
    __tablename__='luts'

    id=Column(Integer,primary_key=True,autoincrement=True)
    title=Column(String)
    description=Column(String)
    file=Column(String)
    #created_at=Column(String)
    # in_pack=Column() #optional

    user_id=Column(Integer,ForeignKey('user.id'),index=True)
    user=relationship("User",backref='luts')
    
    # owned_by=relationship("User",backref='luts')


class LutTemp(Base):
    __tablename__='luts_temp'

    id=Column(Integer,primary_key=True,autoincrement=True)
    title=Column(String)
    description=Column(String)
    file=Column(String)
    status=Column(String,default='Unverified')
    # created_at=Column(String)
    # in_pack=Column() #optional

    user_id=Column(Integer,ForeignKey('user.id'))
    user=relationship("User",backref='luts_temp')
    

Base.metadata.create_all(bind=engine)
