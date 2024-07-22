from app import oauth2
from .. import models, schemas, oauth2
from fastapi import FastAPI,Body, Response,status,HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]

)

@router.get("/",response_model=List[schemas.PostVote])

def show_posts(db :Session = Depends(get_db),current_user:models.User=Depends(
    oauth2.get_current_user),limit:Optional[int]=5,skip:Optional[int]=0,
               search: Optional[str]="",search_content:Optional[str]=""):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
        
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).filter(
    #     models.Post.content.contains(search_content)).limit(limit).offset(skip).all() # skip helps in pagination

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # pydantic_posts=[]

    # for post in posts:
    #     response=PostResponse.from_orm(post)
    #     pydantic_posts.append(response)

    # return pydantic_posts
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("vote")).join(
        models.Vote,models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).filter(
        models.Post.content.contains(search_content)).limit(limit).offset(skip).all()
    return posts

# @router.get("/posts/latest")
# async def get_latest_post():
#     return my_posts[-1] 

@router.get("/{id}",response_model=schemas.PostVote)
async def get_post(id:int, response:Response, db  :Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)): # fastapi will validate that the parameter of id that we are getting is actually an int & it will convert 
                            #it to int if it can be converted,else it will notify. Now we dont have to convert it to integer at our end
    
    # cursor.execute("SELECT * FROM posts WHERE id = %s"%(str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post,func.count(models.Vote.post_id).label("vote")).join(
        models.Vote,models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"data" : f"Post with id {id} not found"}
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform requested action")
    
    return post



# @app.post("/createpost")
# async def create_post(postLabel=Body(...)):
#     print(postLabel)
#     return postLabel


@router.post("/",status_code=status.HTTP_201_CREATED)
def create_post2(posts:List[schemas.CreatePost],response:Response,db:Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    
    if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

    print(current_user.email)  

    for post in posts:
        # cursor.execute("INSERT INTO posts (title, content) VALUES (%s,%s) RETURNING *",(post.title,post.content))
        # new_post=cursor.fetchall()
        # conn.commit()
        
        new_post = models.Post(owner_id=current_user.id,**post.model_dump())
        db.add(new_post)
        db.commit()
        yield post
        
    return(posts)

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db  :Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    # cursor.execute("DELETE FROM posts WHERE id =%s RETURNING *" %(str(id)))
    # # index=return_post_index(id)
    # deleted_post=cursor.fetchone()
    # conn.commit()
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} is not found")
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform requested action")

    db.delete(deleted_post)
    db.commit()
    return  {"Message" : f"Post with id {id} is deleted from database"}
    # # print(type(index))
    # # my_posts.pop(index)
    # # return {"message" : f"post with id {id} is deleted"} #fastapi doesnot allow returning back a something in case of 204 status code
    # # return Response(status_code=status.HTTP_204_NO_CONTENT)
    # return {"Deleted Post": deleted_post}


@router.put("/{id}")
async def update_post(id:int, post:schemas.CreatePost, db : Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title=%s,content=%s WHERE id =%s RETURNING *" ,(post.title,post.content,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    # index=return_post_index(id)
    
    query = db.query(models.Post).filter(models.Post.id == id)

    post2 = query.first()
    if not post2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} is not found")
    
    if post2.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform requested action")
    
    query.update({
        models.Post.title : post.title,
        models.Post.content : post.content},
        synchronize_session=False
    )
    db.commit()
    return {"message":post}