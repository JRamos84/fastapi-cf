from fastapi import FastAPI, APIRouter
from project.database import User, Movie, UserReview
from project.database import database as connection
from .routers import user_router, user_review, user_movie

app = FastAPI(
    title='Proyecto para reseñar peliculas',
    description="En este proyecto seremos capaces reseñar peliculas",
    version='1',
    
)

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(user_review)
api_v1.include_router(user_movie)


app.include_router(api_v1)

@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
    connection.create_tables([User, Movie, UserReview])
        

@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        





