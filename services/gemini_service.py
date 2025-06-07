import google.generativeai as genai
import json
from typing import List
from config import settings

# APIキーを設定
genai.configure(api_key=settings.GEMINI_API_KEY)

# 使用するモデルをインスタンス化
model = genai.GenerativeModel('gemini-1.5-flash')

def translate_texts_with_gemini(texts: List[str], dialect: str) -> List[str]:
    """
    複数のテキストをまとめて指定された方言に変換する
    """
    if not texts:
        return []

    # Geminiに渡すためのプロンプトを構築
    # JSON形式での応答を要求することで、安定した出力を得やすくする
    prompt = f"""
あなたは日本の様々な方言を巧みに話すAIです。
以下の日本語の文章を、すべて「{dialect}」に自然に変換してください。
返答は、変換後の文章だけを要素とするJSON配列の形式で、必ずお願いします。他の余計なテキストは一切含めないでください。

入力する文章の数: {len(texts)}
入力する文章リスト:
{json.dumps(texts, ensure_ascii=False)}

期待する出力形式の例:
["変換後の文章1", "変換後の文章2", ...]
"""

    try:
        response = model.generate_content(prompt)
        # Geminiからの返答テキストからJSON部分を抽出
        response_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        # JSONをパースしてリストとして返す
        translated_list = json.loads(response_text)
        
        if isinstance(translated_list, list) and len(translated_list) == len(texts):
            return translated_list
        else:
            # 形式が正しくない場合は元のテキストを返す
            print(f"Error: Unexpected response format from Gemini. Response: {response.text}")
            return texts

    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        # エラー発生時は元のテキストを返す
        return texts