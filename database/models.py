from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

# database.pyで作成したBaseクラスをインポート
from database.database import Base

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

class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    
    # 'post' or 'reply' を保存し、どちらのテキストか区別する
    text_type = Column(String, nullable=False, index=True)
    # 元の投稿(post)または返信(reply)のID
    original_id = Column(Integer, nullable=False, index=True)
    # 変換先の方言名 (例: '関西弁')
    dialect = Column(String, nullable=False, index=True)
    
    translated_text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 同じテキスト・同じ方言の組み合わせが重複して保存されないようにするための制約
    __table_args__ = (
        UniqueConstraint('text_type', 'original_id', 'dialect', name='_text_dialect_uc'),
    )