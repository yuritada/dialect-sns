from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from typing import List
from database import schemas

from database import database, schemas
from crud import crud_post ,crud_reply
from services import auth_service
from fastapi import HTTPException

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

@router.get("/timeline", response_model=List[schemas.Post], tags=["Timeline"])
def get_timeline(db: Session = Depends(database.get_db)):
    """
    タイムラインに表示する投稿スレッド（投稿＋返信）のリストを取得する。
    - 過去24時間以内の投稿からランダムに20件。
    - 認証は不要。
    """
    timeline_posts = crud_post.get_timeline_posts(db)
    return timeline_posts


@router.post("/{post_id}/replies", response_model=schemas.Reply, status_code=status.HTTP_201_CREATED, tags=["Replies"])
def create_new_reply(
    post_id: int,
    reply: schemas.ReplyCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(auth_service.get_current_user)
):
    """
    特定の投稿に返信する。認証が必要。
    - {post_id} : 返信先の投稿ID
    """
    # 返信先の投稿が存在するか確認
    db_post = crud_post.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 返信を作成
    return crud_reply.create_reply(db=db, reply=reply, post_id=post_id, user_id=current_user.id)