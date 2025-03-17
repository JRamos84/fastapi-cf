from pydantic import BaseModel, validator
from pydantic.utils import GetterDict
from typing import Any
from peewee import ModelSelect
from datetime import datetime


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any =None):
        
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        
        return res 







class UserRequestModel(BaseModel):
    
    username: str 
    password: str 
    
    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('La Longitud debe ser entre 3 y 50 caracteres')
        return username

class   ResponseModel(BaseModel):
        
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
     

class UserResponseModel(ResponseModel):
    id: int
    username: str
    
    
    


class MovieRequestModel(ResponseModel):
    id: int
    title: str
    
class MovieResponseModel(ResponseModel):
    id: int
    title: str
    created_at: str
    
    @validator("created_at", pre=True)
    def format_created_at(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()  # Convierte a string formato ISO 8601
        return value
    

    


class ReviewValidator():
    
    @validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5 :
            raise ValueError('El rango de valor para score es de 1 a  5')
        return score
        
class ReviewRequestModel(BaseModel,ReviewValidator):
    user_id: int
    movie : MovieResponseModel
    reviews: str
    score: int
    
    

class ReviewResponseModel(ResponseModel):
    id: int
    movie: MovieResponseModel
    reviews: str
    score: int
    
class ReviewRequestPutModel(BaseModel,ReviewValidator):
    reviews: str
    score: int

    
