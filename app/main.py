from fastapi import FastAPI,Body, Response,status,HTTPException,Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import List
from .database import engine,get_db
from sqlalchemy.orm import Session
from .models import Base
from app import models

Base.metadata.create_all(bind=engine)

app=FastAPI()



class Post(BaseModel):
    title :str
    content:str
    number:int = 4
    published : bool = True
    rating: Optional[int] = None
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='playrakion123',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database Connection Established")
        break
    except Exception as error:
        print("Database connection failed")
        print(error)
        time.sleep(2)

my_posts =[{"title":"title of post 1","content":"content of post 1","id":1},
           {"title":"favourite food","content":"pizza it is","id":2}]  # variable to store data in memory instead of database

def find_post(id):
    for p in my_posts:
        if p["id"] == id :
            return p
        
def return_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"]==id:
            return i

@app.get("/")
async def root():
    return {"message":"Welcome !"}

@app.get("/posts")
async def show_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return{"data":posts}

@app.get("/posts/latest")
async def get_latest_post():
    return my_posts[-1] 

@app.get("/posts/{id}")
async def get_post(id:int, response:Response): # fastapi will validate that the parameter of id that we are getting is actually an int & it will convert 
                            #it to int if it can be converted,else it will notify. Now we dont have to convert it to integer at our end
    
    cursor.execute("SELECT * FROM posts WHERE id = %s"%(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"data" : f"Post with id {id} not found"}
    return {"data": post}



# @app.post("/createpost")
# async def create_post(postLabel=Body(...)):
#     print(postLabel)
#     return postLabel

@app.get("/sqlalchemy")
async def test_posts(db:Session=Depends(get_db)):  # Depends is dependency injection utility function. if we directly use get_db() here
    #then it will call the function as soon as code is loaded. Using Depends it will inject the dependency only when this api endpoint
    #is hit and this route handler is activated
    posts = db.query(models.Post).all()
    return {"status":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post2(posts:List[Post],response:Response):
    
    # for i in range(0,post.number+1):
    #     post.title=post.title+str(i)
    #     post.content=post.content+str(i*10)
    #     # print(post.title)
    #     # print(post.content)
    #     yield post
    #     yield post.model_dump()
    # print(post)
    # print(post.model_dump())
    # post_dict=post.model_dump()
    # post_dict["id"]=randrange(0,10000000)
    # my_posts.append(post_dict)
    # # response.status_code=status.HTTP_201_CREATED
    # cursor.execute(f"INSERT INTO posts (title, content) VALUES ({post.title},{post.content})")  #thi shud be avoided as it is 
    # #prone to SQL injection
    
    for post in posts:
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s,%s) RETURNING *",(post.title,post.content))
        new_post=cursor.fetchall()
        conn.commit()

    return(posts)

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):

    cursor.execute("DELETE FROM posts WHERE id =%s RETURNING *" %(str(id)))
    # index=return_post_index(id)
    deleted_post=cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} is not found")
    # print(type(index))
    # my_posts.pop(index)
    # return {"message" : f"post with id {id} is deleted"} #fastapi doesnot allow returning back a something in case of 204 status code
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    return {"Deleted Post": deleted_post}

@app.put("/posts/{id}")
async def update_post(id:int, post:Post):
    cursor.execute("UPDATE posts SET title=%s,content=%s WHERE id =%s RETURNING *" ,(post.title,post.content,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    # index=return_post_index(id)
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} is not found")
    # else:
    #     my_posts[index]=post.model_dump()
    return {"message":updated_post}