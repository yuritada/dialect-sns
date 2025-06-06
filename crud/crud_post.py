from sqlalchemy.orm import Session
from database import models, schemas

def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    """
    新しい投稿をデータベースに作成する
    """
    # Pydanticモデルをdictに変換し、user_idを追加してDBモデルを作成
    db_post = models.Post(**post.model_dump(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post