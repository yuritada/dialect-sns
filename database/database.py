import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

# --- 設定クラス ---
# .envファイルからデータベース接続URLを読み込む
class DbSettings(BaseSettings):
    # Render Postgresから取得した "Internal Database URL" を設定する
    DATABASE_URL: str = "postgresql://user:password@host/dbname"

    class Config:
        env_file = ".env"

settings = DbSettings()


# --- SQLAlchemyのセットアップ ---
# データベースエンジンを作成。これがDBとの通信の核となる
engine = create_engine(settings.DATABASE_URL)

# データベースセッションを作成するためのファクトリ
# autocommit=False, autoflush=False は標準的な設定
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORMモデル（テーブル定義）が継承するための基本クラス
Base = declarative_base()


# --- DBセッションをAPIリクエストに提供するための依存性注入 ---
def get_db():
    """
    APIエンドポイントで呼び出されると、データベースセッションを提供する。
    処理が完了したら（またはエラーが発生したら）セッションを閉じる。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()