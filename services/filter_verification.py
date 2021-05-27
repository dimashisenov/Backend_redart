
from os import write
from types import ModuleType
from fastapi import UploadFile,File
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import roles
from sqlalchemy.sql.expression import delete
from sqlalchemy.sql.functions import mode
from database import get_session
from fastapi import Depends,HTTPException,status
import models, tables
import shutil
from uuid import uuid4
import aiofiles
from typing import List
import os

class TempDB:

    def __init__(self, session :Session = Depends(get_session)):
        self.session = session

    def verify_lut(self , user : models.User , status:str , file_name:str=None , id:int=None):
        # exception = HTTPException(
        # status_code=status.HTTP_403_FORBIDDEN,
        # detail='Permission denied',
        # headers={'WWW-Authenticate': 'Bearer'})
        
        if user.role=='admin' and (file_name is not None):
            info = self.session.query(tables.LutTemp).filter(tables.LutTemp.file == file_name).first()
            if not info:
                raise HTTPException(status.HTTP_404_NOT_FOUND)
            
            if status == 'Verified':
                create = tables.Lut(title=info.title,description=info.description,file=info.file)
                self.session.delete(info)
                self.session.add(create)
                self.session.commit()
            if status == 'Delete':
                self.session.delete(info)
                self.session.commit()
                os.unlink(info.file)
                self.session.delete(info)

        elif user.role=='admin' and (id is not None):
            info = self.session.query(tables.LutTemp).filter(tables.LutTemp.id == id).first()
            if status == 'Verified':
                create = tables.Lut(title=info.title,description=info.description,file=info.file)
                self.session.delete(info)
                self.session.add(create)
                self.session.commit()
            if status == 'Delete':
                #delete with such name 
                self.session.delete(info)
                os.unlink(info.file)
                self.session.commit()

            #push changes and if 
            if not info:
                raise HTTPException(status.HTTP_404_NOT_FOUND)
        else:
            print("idi nahuy")

    def list_all_temp_preset(self,)->List[tables.LutTemp]:
        return self.session.query(tables.LutTemp).all()
