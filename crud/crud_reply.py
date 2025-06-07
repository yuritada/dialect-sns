from sqlalchemy.orm import Session
from database import models, schemas

def create_reply(db: Session, reply: schemas.ReplyCreate, post_id: int, user_id: int):
    """
    新しい返信をデータベースに作成する
    """
    db_reply = models.Reply(
        **reply.model_dump(), 
        post_id=post_id, 
        user_id=user_id
    )
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    return db_reply