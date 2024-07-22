from fastapi import status,HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from .. import schemas, models, database, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db : Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            current_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} with email '{current_user.email}' has already voted for post title '{current_post.title}' with post id {vote.post_id} "
                )

                                
        else:
            
            post_is_valid = False
            if db.query(models.Post).filter(models.Post.id == vote.post_id).first():
                post_is_valid = True
            if post_is_valid:
                new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
                db.add(new_vote)
                db.commit()
                return {"message" : "successfully added vote"}
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with post id {vote.post_id} not found")
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {vote.post_id} not found")
        else:
            vote_delete=db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).first()
            db.delete(vote_delete)
            db.commit()
            return {"message": "vote successfully deleted"}
            