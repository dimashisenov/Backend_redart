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


artist_router = APIRouter(
    tags=['artist'],
    prefix='/artist'
)

#all below needs to be rearranged
@artist_router.post('/info/create',response_model=models.UserInfo)
def create_info(
    data:models.UserInfoCreate,
    user:models.User = Depends(get_current_user),
    service:CRUD=Depends()):
    service.create_user_info(user,data)


@artist_router.get('/info/read',response_model=models.UserInfo)
def get_info(
    user:models.User = Depends(get_current_user),
    service:CRUD=Depends()):
    return service.read_user_info(user.id)

@artist_router.put('/info/update',response_model=models.UserInfo)
def update_info(
    data:models.UserInfoUpdate,
    user:models.User = Depends(get_current_user),
    service:CRUD=Depends(),
    ):
    service.update_user_info(user.id,data)

@artist_router.delete('/info/delete')
def delete_info(
    user:models.User = Depends(get_current_user),
    service:CRUD=Depends()):
    service.delete_user_info(user.id)

@artist_router.post('/presets/post')
def post_preset(
    # info:models.UploadPreset,
    title:str=None,
    description:str=None,
    preset: UploadFile = File(...),
    user:models.User = Depends(is_artist),
    session:Session=Depends(get_session),   
    service:CRUD_luts=Depends()):

    service.create_preset(user,preset,title,description)


@artist_router.get('/presets/get')
def get_preset():
    pass

@artist_router.get('/presets/list_presets')
def list_created_presets(
    user:models.User = Depends(get_current_user)):
    CRUD_luts.list_owned_presets(CRUD_luts,user)
