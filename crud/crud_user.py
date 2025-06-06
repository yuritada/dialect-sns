from sqlalchemy.orm import Session
from database import models, schemas
from services.auth_service import get_password_hash

def get_user_by_username(db: Session, username: str):
    """ユーザー名でユーザーを検索する"""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """新しいユーザーを作成する"""
    # 平文のパスワードをハッシュ化
    hashed_password = get_password_hash(user.password)
    
    # DBモデルオブジェクトを作成
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    
    # データベースへの登録
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # DBに登録された情報をdb_userオブジェクトに反映（IDなど）
    
    return db_user