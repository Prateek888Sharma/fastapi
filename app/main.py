from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware


# Base.metadata.create_all(bind=engine)   # This willnot be needed to create tables if they are not there in db 
#once we use alembic

origins=["*"]

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message":"Welcome !"}



