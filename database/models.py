from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

# database.pyで作成したBaseクラスをインポート
from .database import Base

# --- users テーブルの定義 ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # UserとPost/Replyのリレーションシップ（1対多）
    # user.posts や user.replies でそのユーザーの投稿/返信一覧にアクセスできる
    posts = relationship("Post", back_populates="owner")
    replies = relationship("Reply", back_populates="owner")

# --- posts テーブルの定義 ---
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_text = Column(String(140), nullable=False) # 140字制限を反映
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # PostとUser/Replyのリレーションシップ
    # post.owner で投稿者の情報にアクセスできる
    owner = relationship("User", back_populates="posts")
    # post.replies でこの投稿への返信一覧にアクセスできる
    # cascade="all, delete-orphan" は、投稿が削除されたら関連する返信も全て削除する設定
    replies = relationship("Reply", back_populates="parent_post", cascade="all, delete-orphan")

# --- replies テーブルの定義 ---
class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_text = Column(String(140), nullable=False) # 140字制限を反映
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ReplyとPost/Userのリレーションシップ
    parent_post = relationship("Post", back_populates="replies")
    owner = relationship("User", back_populates="replies")