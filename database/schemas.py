from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# --- Reply Schemas ---

# 返信の基本となるスキーマ
class ReplyBase(BaseModel):
    original_text: str

# 返信を作成する際に使用するスキーマ
class ReplyCreate(ReplyBase):
    pass

# APIから返信する際に使用するスキーマ（DBから読み取る）
class Reply(ReplyBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        # SQLAlchemyモデルなどのORMオブジェクトからPydanticモデルを生成する設定
        from_attributes = True


# --- Post Schemas ---

# 投稿の基本となるスキーマ
class PostBase(BaseModel):
    original_text: str

# 投稿を作成する際に使用するスキーマ
class PostCreate(PostBase):
    pass

# APIから返信する際に使用するスキーマ（DBから読み取る）
# 返信(Reply)の情報もネストして含める
class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime
    replies: List[Reply] = []  # この投稿に紐づく返信のリスト

    class Config:
        from_attributes = True


# --- User Schemas ---

# ユーザーの基本となるスキーマ
class UserBase(BaseModel):
    username: str

# ユーザーを作成する際に使用するスキーマ（パスワードを含む）
class UserCreate(UserBase):
    password: str

# APIから返信する際に使用するスキーマ（DBから読み取る）
# ★重要★ パスワードなどの秘密情報は絶対に含めない
class User(UserBase):
    id: int
    
    # ユーザーに紐づく投稿と返信のリスト（今回は使わないが、拡張性のために定義）
    # posts: List[Post] = []
    # replies: List[Reply] = []

    class Config:
        from_attributes = True

# --- Token Schemas (認証用) ---

# トークンそのもののスキーマ
class Token(BaseModel):
    access_token: str
    token_type: str

# トークンのペイロード（中身）のスキーマ
class TokenData(BaseModel):
    username: Optional[str] = None