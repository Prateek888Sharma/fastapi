from typing import Optional
from pydantic import BaseModel,EmailStr, conint
from datetime import datetime

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class CreatePost(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime


    class Config:
        orm_mode=True

# class VotePost(BaseModel):
#     id :int
#     title : str
#     content : str
#     published : bool
#     created_at: datetime
#     owner_id : int
#     owner : UserOut
#     count : int

#     class Config:
#         orm_mode=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

        
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):

    access_token:str
    token_type:str

class TokenData(BaseModel):  

    id :Optional[str] = None


class PostResponse(PostBase):
    id:int
    created_at:datetime
    owner_id:int

    owner: UserOut

    # @classmethod
    # def from_orm(cls, obj):
    #     return cls(
    #         id=obj.id,
    #         title=obj.title,
    #         content=obj.content,
    #         published=obj.published,
    #         created_at=obj.created_at
    #     )
    
    class Config:
        orm_mode=True

class PostVote(BaseModel):
    Post : PostResponse
    vote : int

    class Config:
        orm_mode=True

class Vote(BaseModel):
    post_id : int
    dir : conint(le=1) # type: ignore
    
    
