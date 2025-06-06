





from fastapi import APIRouter, Depends, HTTPException, status
# OAuth2PasswordRequestFormを追加
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from database import database, schemas
from crud import crud_user
from services import auth_service # auth_serviceをインポート
from config import settings

router = APIRouter(
    tags=["Users"], # /users プレフィックスを削除し、タグで管理
)
@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    新しいユーザーを登録するためのAPIエンドポイント。
    - ユーザー名が既に存在する場合はエラーを返す。
    - 成功した場合は、作成されたユーザー情報を返す（パスワードは含まない）。
    """
    # 既存ユーザーのチェック
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このユーザー名は既に使用されています",
        )
    
    # ユーザーの作成
    return crud_user.create_user(db=db, user=user)

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    ユーザー名とパスワードでログインし、アクセストークンを取得する。
    form_dataは "username" と "password" を持つ。
    """
    user = crud_user.get_user_by_username(db, username=form_data.username)
    if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}