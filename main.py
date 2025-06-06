import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
from dotenv import load_dotenv
from database.database import engine
from .database import models



# .envファイルから環境変数を読み込む
load_dotenv()

# --- 設定クラス ---
# 環境変数から設定を読み込むためのクラス
# .envファイルやシステムの環境変数を自動で読み込んでくれる
class Settings(BaseSettings):
    # デプロイしたVercelのURLや、ローカル開発用のURLを記述する
    # 環境変数ではカンマ区切りで設定 -> CORS_ORIGINS="http://localhost:3000,https://your-frontend.vercel.app"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]


    class Config:
        # .envファイルを読み込む設定
        env_file = ".env"

# 設定クラスのインスタンスを作成
settings = Settings()

models.Base.metadata.create_all(bind=engine)


# --- FastAPIアプリケーションのインスタンス化 ---
app = FastAPI(
    title="方言ガチャSNS API",
    description="投稿がランダムな方言に変換されて表示される、匿名風SNSのバックエンドAPI",
    version="0.1.0"
)


# --- CORSミドルウェアの設定 ---
# フロントエンド（Vercel）からのAPIリクエストを許可するための設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # 許可するオリジン（フロントエンドのURL）
    allow_credentials=True,             # クレデンシャル（Cookieなど）を許可するか
    allow_methods=["*"],                # すべてのHTTPメソッドを許可
    allow_headers=["*"],                # すべてのHTTPヘッダーを許可
)


# --- ルートエンドポイント（動作確認用） ---
@app.get("/", tags=["Root"])
def read_root():
    """
    サーバーが正常に起動しているか確認するためのエンドポイント
    """
    return {"message": "ようこそ、方言ガチャSNSのバックエンドへ！"}

# 以降、ここに各ルーターを登録していく
# from .routers import users, posts, translate
# app.include_router(users.router)
# ...