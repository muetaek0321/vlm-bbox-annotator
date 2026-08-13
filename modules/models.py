from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """BBoxの情報の定義"""

    class_name: str = Field(description="アノテーション対象のクラスの名称")
    bbox: list[int] = Field(description="バウンディングボックスの座標 [x_min, y_min, x_max, y_max]")


class ResponseFormat(BaseModel):
    """LLMの返答形式の定義"""

    bboxes: list[BoundingBox] = Field(
        description="アノテーション対象のクラスの名称とバウンディングボックスの座標のリスト"
    )


def get_model(model_name: str) -> ChatGoogleGenerativeAI:
    """モデルのインスタンスを取得

    Args:
        model_name (str): モデル名

    Returns:
        ChatGoogleGenerativeAI: モデルのインスタンス
    """

    # モデルの設定
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.0,
        thinking_budget=4096,
    )

    # 出力フォーマットの設定
    llm = llm.with_structured_output(ResponseFormat)

    return llm
