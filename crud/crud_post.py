from sqlalchemy.orm import Session
from database import models, schemas
from datetime import datetime, timedelta
from sqlalchemy import func

def get_post(db: Session, post_id: int):
    """IDで投稿を1件取得する"""
    return db.query(models.Post).filter(models.Post.id == post_id).first()

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

# ファイルの下部に追加する新しい関数
def get_timeline_posts(db: Session, limit: int = 20):
    """
    タイムラインに表示するための投稿を取得する
    - 過去24時間以内の投稿が対象
    - ランダムな順序で
    - 指定された件数だけ取得
    """
    # 24時間前の時刻を計算
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    
    # データベースクエリを構築
    posts = db.query(models.Post)\
        .filter(models.Post.created_at >= twenty_four_hours_ago)\
        .order_by(func.random()) \
        .limit(limit)\
        .all()
        
    return posts