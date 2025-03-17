from fastapi import HTTPException, APIRouter
from fastapi.security import HTTPBasicCredentials
from fastapi import Response, Cookie
from ..database import User
from typing import List
from ..schemas import UserRequestModel, UserResponseModel, ReviewResponseModel
from fastapi import Depends
from common import ouath2_schema
router = APIRouter(prefix='/users')



@router.post('', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    
    ### Aquí el where comparar los valores de username de la solictud con lo que hay en l tabla user 
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El username ya se encuentra en uso')
    
    hash_password = User.create_password(user.password)
    user = User.create(
        username  = user.username,
        password = hash_password 
        )
    return user



@router.post('/login', response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    
    user = User.select().where(User.username == credentials.username).first()
    
    if user is None:
        raise HTTPException(404, detail="User not found")
    
    if user.password != User.create_password(credentials.password):
        raise HTTPException(404, "Password Error")
    
    response.set_cookie(key='user_id', value=user.id)
    
    return user 

@router.get('/reviews',response_model= List[ReviewResponseModel])
async def get_reviews(token: str = Depends(ouath2_schema)):
    return {
        'token': token    
    }
    


# @router.get('/reviews',response_model= List[ReviewResponseModel])
# async def get_reviews(user_id: int = Cookie(None)):
#     user = User.select().where(User.id == user_id).first()
#     if user is None:
#         raise HTTPException(404, "Not found")
   
#     return [ user_review for user_review in user.reviews]
    


