from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 新しく作成したconfig.pyからsettingsインスタンスをインポート
# ディレクトリ階層が一つ上なので ..config となる
from config import settings


# --- SQLAlchemyのセットアップ ---
# config.pyからDATABASE_URLを読み込む
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# --- DBセッションをAPIリクエストに提供するための依存性注入 ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()