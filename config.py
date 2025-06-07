from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator # pydanticからfield_validatorをインポート
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # --- Database Settings ---
    DATABASE_URL: str

    # --- CORS Settings ---
    CORS_ORIGINS: Union[List[str], str] # 一旦、文字列またはリストとして受け入れる

    # --- JWT Settings (追加) ---
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    GEMINI_API_KEY: str


    class Config:
        env_file = ".env"

    # CORS_ORIGINSフィールドを検証・変換するバリデータ
    @field_validator("CORS_ORIGINS", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v: Union[List[str], str]) -> List[str]:
        """
        値が文字列であればカンマで分割し、前後の空白を削除してリストに変換する。
        すでにリスト形式であれば、そのまま返す。
        """
        if isinstance(v, str):
            # 文字列の場合、カンマで分割してリスト化する
            return [item.strip() for item in v.split(',')]
        # 文字列でない場合（すでにリストなど）は、そのまま返す
        return v


# アプリケーション全体でこのインスタンスをインポートして使用する
settings = Settings()