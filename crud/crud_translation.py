from sqlalchemy.orm import Session
from database import models

def get_cached_translation(db: Session, text_type: str, original_id: int, dialect: str):
    """キャッシュされた翻訳を検索する"""
    return db.query(models.Translation).filter(
        models.Translation.text_type == text_type,
        models.Translation.original_id == original_id,
        models.Translation.dialect == dialect
    ).first()

def create_translation_cache(db: Session, text_type: str, original_id: int, dialect: str, translated_text: str):
    """新しい翻訳結果をキャッシュに保存する"""
    db_translation = models.Translation(
        text_type=text_type,
        original_id=original_id,
        dialect=dialect,
        translated_text=translated_text
    )
    db.add(db_translation)
    db.commit()
    db.refresh(db_translation)
    return db_translation