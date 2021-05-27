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
from classes.admin import admin_router
from classes.artist import artist_router


app=FastAPI(
    title='Backend REDart',
    description='backend for REDart flutter project, with user,artist and admin'
)


@app.post(
    '/sign-up/',
    response_model=models.Token,
    status_code=status.HTTP_201_CREATED,
)
def sign_up(
    user_data: models.UserCreate,
    auth_service: AuthService = Depends(),
):
    return auth_service.register_new_user(user_data)


@app.post(
    '/sign-in/',
    response_model=models.Token,
)
def sign_in(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    return auth_service.authenticate_user(
        auth_data.username,
        auth_data.password,
    )


@app.get(
    '/user/',
    response_model=models.User,
)
def get_user(user: models.User = Depends(get_current_user)):
    print("out of dependency")
    return user


app.include_router(artist_router)
app.include_router(admin_router)
#all below needs to be rearranged
'''
@app.post('/',response_model=models.UserInfo)
def create_info(
    data:models.UserInfoCreate,
    user:models.User = Depends(get_current_user),
    service:CRUD=Depends()):
    service.create_user_info(data)

@app.get('/admin',response_model=models.UserInfo)
def get_info_admin(
    user_id:int,
    user:models.User = Depends(is_admin),
    service:CRUD=Depends()):
    return service.read_user_info(user_id)


@app.get('/',response_model=models.UserInfo)
def get_info(
    user:models.User = Depends(get_current_user),
    service:CRUD=Depends()):
    return service.read_user_info(user.id)


@app.put('/admin',response_model=models.UserInfo)
def update_info_admin(
    user_id:int,
    data:models.UserInfoUpdate,
    user:models.User = Depends(is_admin),
    service:CRUD=Depends(),
    ):
    service.update_user_info(user_id,data)

@app.put('/',response_model=models.UserInfo)
def update_info(
    user_id:int,
    data:models.UserInfoUpdate,
    user:models.User = Depends(get_current_user),
    service:CRUD=Depends(),
    ):
    service.update_user_info(user_id,data)


@app.delete('/admin/{user_id}')
def delete_info_admin(
    user_id:int,
    user:models.User = Depends(is_admin),
    service:CRUD=Depends()):
    service.delete_user_info(user_id)


@app.delete('/{user_id}')
def delete_info(
    user:models.User = Depends(get_current_user),
    service:CRUD=Depends()):
    service.delete_user_info(user.user_id)

@app.post('/presets')
def post_preset(
    info:models.UploadPreset,
    preset: UploadFile = File(...),
    user:models.User = Depends(is_artist),
    session:Session=Depends(get_session)):
    CRUD_luts.create_preset(user,preset,info)

# upload causing some errors when this is writter in clut.py file
@app.post('/admin/presets')
def post_preset_admin(
    info:models.UploadPreset,
    user:models.User = Depends(is_admin),
    preset: UploadFile = File(...),
    session:Session=Depends(get_session)):
    CRUD_luts.create_preset(user,preset)
    pass

@app.post('/admin/presets/verify')
def verify_preset(
    status:str,
    user:models.User = Depends(is_admin),
    file_name:str=None,
    id:int=None):
    TempDB.verify_lut(user,status,file_name,id)

@app.get('/admin/presets/get')
def get_preset():
    pass

@app.delete('/presets')
def delete_preset(
    id:int=None,
    file_name:str=None,):
    CRUD_luts.delete_preset(id,file_name)

@app.get('/list_presets')
def list_owned_presets(
    user:models.User = Depends(get_current_user)):
    CRUD_luts.list_owned_presets(CRUD_luts,user)

@app.get('/admin/list_all_presets')
def list_all_preset(
    user:models.User = Depends(get_current_user)):
    CRUD_luts.list_all_presets()

@app.get('/admin/list_all_temp_presets')
def list_all_temp_presets(
    user:models.User = Depends(is_admin)
):
    TempDB.list_all_temp_luts(TempDB)
'''