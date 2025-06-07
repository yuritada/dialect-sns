from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import database, schemas
from crud import crud_translation
from services import gemini_service

router = APIRouter(
    prefix="/translate",
    tags=["Translation"],
)

@router.post("/", response_model=schemas.TranslationResponse)
def translate_texts(request: schemas.TranslationRequest, db: Session = Depends(database.get_db)):
    """
    複数のテキストを指定された方言に変換する。
    まずキャッシュを確認し、なければGemini APIを呼び出す。
    """
    final_results = []
    items_to_translate = []
    
    # 1. キャッシュ確認
    for item in request.texts:
        cached = crud_translation.get_cached_translation(
            db, text_type=item.type, original_id=item.id, dialect=request.dialect
        )
        if cached:
            final_results.append(
                schemas.TranslationResponseItem(
                    type=cached.text_type, id=cached.original_id, translated_text=cached.translated_text
                )
            )
        else:
            items_to_translate.append(item)

    # 2. キャッシュになかったものをまとめてGeminiに問い合わせ
    if items_to_translate:
        original_texts = [item.text for item in items_to_translate]
        translated_texts = gemini_service.translate_texts_with_gemini(original_texts, request.dialect)
        
        # 3. 結果をキャッシュに保存し、最終結果に追加
        for i, item in enumerate(items_to_translate):
            translated_text = translated_texts[i]
            crud_translation.create_translation_cache(
                db, text_type=item.type, original_id=item.id, dialect=request.dialect, translated_text=translated_text
            )
            final_results.append(
                schemas.TranslationResponseItem(
                    type=item.type, id=item.id, translated_text=translated_text
                )
            )

    return {"results": final_results}