from fastapi import  FastAPI
from . import models
from .database import engine
from .routers import posts,users,auth
from .config import setting


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)



    