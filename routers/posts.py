from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import database, schemas
from crud import crud_post
from services import auth_service

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_new_post(
    post: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(auth_service.get_current_user)
):
    """
    新しい投稿を作成する。認証が必要。
    """
    return crud_post.create_post(db=db, post=post, user_id=current_user.id)