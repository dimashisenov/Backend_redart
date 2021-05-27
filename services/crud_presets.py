from os import write
from types import ModuleType
from fastapi import UploadFile,File,Request
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import roles
from sqlalchemy.sql.expression import table
from starlette.requests import Request
from fastapi.responses import FileResponse
from database import get_session
from fastapi import Depends,HTTPException,status
import models, tables
import shutil
from uuid import uuid4
import aiofiles
from services.filter_verification import TempDB
from pathlib import Path
import os

class CRUD_luts:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_preset(self, user:models.User,preset: UploadFile,title:str,description:str):
        save_path='/presets'
        # file_name=f'media/{user.id}_{uuid4()}.png' #encrypting name based on id of user find more efficient way
        with open(preset.filename, "wb") as buffer:
            shutil.copyfileobj(preset.file, buffer)

        if user.role =='admin':
            info = tables.Lut(file=preset.filename,user_id=user.id,title=title,description=description)
            self.session.add(info)    
            self.session.commit()
        if user.role =='artist':
            info = tables.LutTemp(file=preset.filename,user_id=user.id,title=title,description=description)
            self.session.add(info)    
            self.session.commit()

        return 1
    
    def read_preset(self, id:int =None, file_name:str=None):
        try:
            if id is not None:
                file = self.session.query(tables.Lut).filter(tables.Lut.id == id).first()
            elif file_name is not None:
                #how to deal with files with the same name
                file = self.session.query(tables.Lut).filter(tables.Lut.file == file_name).first()
        except:
            raise HTTPException(status_code=404,detail='Not found')
        return FileResponse(file.file,media_type='image/png')
    
    def update_preset():
        pass

    def delete_preset(self,id:int=None,file_name:str=None):
        if id is not None:
            info = self.session.query(tables.Lut).filter(tables.Lut.id == id).first()
        elif file_name is not None:
            info = self.session.query(tables.Lut).filter(tables.Lut.file == file_name).first()
        if not info:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        self.session.delete(info)
        self.session.commit()
        os.unlink(info.file)

    def list_owned_presets(self,user:models.User):
        return self.session.query(tables.Lut).filter(tables.Lut.owned_by==user).all()

    def list_all_presets(self,):
        return self.session.query(tables.Lut).all()


