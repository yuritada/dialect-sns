from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 新しく作成したconfig.pyからsettingsインスタンスをインポート
from config import settings
from database.database import engine
from database import models

from routers import users, posts

# データベースにテーブルを自動作成する処理
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
app.include_router(users.router)
app.include_router(posts.router)
# ...