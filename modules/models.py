from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """BBoxの情報の定義"""

    class_name: str = Field(description="アノテーション対象のクラスの名称")
    bbox: list[float] = Field(description="バウンディングボックスの正規化座標(0.0~1.0の範囲)")


class ResponseFormat(BaseModel):
    """LLMの返答形式の定義"""

    bboxes: list[BoundingBox] = Field(
        description="アノテーション対象のクラスの名称とバウンディングボックスの座標のリスト"
    )


def get_model(model_name: str, model_type: str) -> ChatGoogleGenerativeAI:
    """モデルのインスタンスを取得

    Args:
        model_name (str): モデル名
        model_type (str): モデル種別

    Returns:
        ChatGoogleGenerativeAI: モデルのインスタンス
    """

    # モデルの設定
    if model_type == "Gemini":
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.0,
            thinking_budget=4096,
        )
    elif model_type == "Ollama":
        llm = ChatOllama(model=model_name, temperature=0.0)

    # 出力フォーマットの設定
    llm = llm.with_structured_output(ResponseFormat, include_raw=True)

    return llm
