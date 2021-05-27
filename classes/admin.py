from database import get_session
from fastapi import (
    APIRouter,
    Depends,
    status,
    FastAPI
)
from fastapi import File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode, user

import models,tables
from uuid import uuid4

from services.auth import (
    AuthService,
    get_current_user,
    is_admin,
    is_artist
)
from services.crud_users import CRUD 
import shutil
from services.crud_presets import CRUD_luts
from services.filter_verification import TempDB

admin_router = APIRouter(
    tags=['admin'],
    prefix='/admin'
)


@admin_router.get('/info/read',response_model=models.UserInfo)
def get_info_admin(
    user_id:int,
    user:models.User = Depends(is_admin),
    service:CRUD=Depends()):
    return service.read_user_info(user_id)

@admin_router.put('/info/update',response_model=models.UserInfo)
def update_info_admin(
    user_id:int,
    data:models.UserInfoUpdateAdmin,
    user:models.User = Depends(is_admin),
    service:CRUD=Depends(),
    ):
    service.update_user_info_admin(user_id,data)


@admin_router.delete('/info/delete')
def delete_info_admin(
    user_id:int,
    user:models.User = Depends(is_admin),
    service:CRUD=Depends()):
    service.delete_user_info(user_id)

@admin_router.post('/presets/verify')
def verify_preset(
    status:str,
    user:models.User = Depends(is_admin),
    service:TempDB=Depends(),
    file_name:str=None,
    id:int=None):
    service.verify_lut(user,status,file_name,id)

@admin_router.post('/presets/post')
def post_preset_admin(
    title:str=None,
    description:str=None,
    user:models.User = Depends(is_admin),
    preset: UploadFile = File(...),
    service:CRUD_luts=Depends()):
    service.create_preset(user,preset,title,description)

@admin_router.get('/preset/get/{id}')
def get_preset(
    id:int=None,
    file_name:str=None,
    service:CRUD_luts=Depends()):
    service.read_preset(id,file_name)
    pass

@admin_router.delete('/presets/delete/{id}')
def delete_preset(
    id:int=None,
    file_name:str=None,
    service:CRUD_luts=Depends()):
    service.delete_preset(id,file_name)

@admin_router.get('/list_all_temp_presets')
def list_all_temp_presets(
    user:models.User = Depends(is_admin),
    service:TempDB=Depends()
):
    service.list_all_temp_preset()