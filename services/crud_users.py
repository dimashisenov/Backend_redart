from typing import List
from fastapi import Depends,status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session, session
from typing import List,Optional
from database import get_session
import tables,models



class CRUD:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
    
    def create_user_info(self,user:tables.User,data:models.UserInfoCreate) -> tables.UserInfo :
        check = self.session.query(tables.UserInfo).filter(tables.UserInfo.user_id==user.id).first()
        if check:
            raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED)
        info = tables.UserInfo(**data.dict(),user_id=user.id)
        self.session.add(info)
        self.session.commit()
        return info

    def read_user_info(self,user_id:int)->tables.UserInfo:
        info = self.session.query(tables.UserInfo).filter(tables.UserInfo.user_id == user_id).first()
        if not info:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return info

    def update_user_info(self,user_id:int,data:models.UserInfoUpdate):
        info = self.session.query(tables.UserInfo).filter(tables.UserInfo.user_id==user_id).first()
        if not info:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        for field, value in data:
            setattr(info,field,value)
        self.session.commit()
        return info
    def update_user_info_admin(self,user_id:int,data:models.UserInfoUpdateAdmin):
        info = self.session.query(tables.UserInfo).filter(tables.UserInfo.user_id==user_id).first()
        if not info:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        for field, value in data:
            setattr(info,field,value)
        self.session.commit()
        return info

    def delete_user_info(self,user_id:int):
        info=self.session.query(tables.UserInfo).filter(tables.UserInfo.user_id==user_id).first()
        if not info:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        self.session.delete(info)
        self.session.commit()

    def delete_user(self,user_id:int):
        pass

    def list_all_info(self,) -> List[tables.UserInfo]:
        return self.session.query(tables.UserInfo).all()

    