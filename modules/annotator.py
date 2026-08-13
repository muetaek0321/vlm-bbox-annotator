import base64
import os
from io import BytesIO

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from PIL import Image

from .models import ResponseFormat, get_model

# 環境変数の読み込み
load_dotenv()

PROMPT = """
入力画像を確認し、以下の対象クラスに含まれる物体だけを検出してください。
各物体について、クラス名とバウンディングボックスを 1 件ずつ返してください。

# 対象クラス
{classes_info}

# 検出ルール
- 上記の対象クラス以外の物体は検出しないでください。
- 画像中に見つかった対象物体をすべて列挙してください。
- 1 つの物体に対して 1 件の bbox を返してください。
- 物体の境界は画像のピクセル座標で表し、座標は [x_min, y_min, x_max, y_max] の順でください。
- x_min, y_min は左上、x_max, y_max は右下を指します。
- 座標は整数で、x_min < x_max, y_min < y_max を満たしてください。
- すべての bbox は画像内に収まるようにしてください。
- 検出対象が 1 つもない場合は、bbox: [] を返してください。

# 出力形式
出力は JSON 形式のみで、以下のスキーマに厳密に一致させてください。
{{
  "bbox": [
    {{
      "class_name": "対象クラス名",
      "bbox": [x_min, y_min, x_max, y_max]
    }}
  ]
}}

- 追加の説明、見出し、Markdown コードブロックは付けず、JSON のみを返してください。
- 文字列の引用符やコメントは含めないでください。
"""


class VLMAnnotateAssistant:
    def __init__(self, classes: dict[str, str]) -> None:
        """初期化

        Args:
            classes (dict[str, str]): アノテーション対象のクラス名と説明の辞書
        """
        # プロンプトの設定
        self.classes = classes
        classes_info = [f"- {name}: {description}" for name, description in self.classes.items()]
        self.prompt = PROMPT.format(classes_info="\n".join(classes_info))

        # モデルのインスタンスを取得
        self.llm = get_model(model_name=os.getenv("MODEL_NAME", "gemini-3.5-flash-lite"))

    def annotate(self, img: Image.Image) -> ResponseFormat:
        """画像に対してアノテーションを行う

        Args:
            img (str): 画像データ

        Returns:
            ResponseFormat: アノテーション結果
        """
        # base64エンコードする
        img_base64 = self.image_to_bytes(img)

        # プロンプトの設定
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": self.prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img_base64}"},
                },
            ]
        )

        # 返答の生成
        response = self.llm.invoke([message])

        return response

    def image_to_bytes(self, img: Image.Image) -> str:
        buffer = BytesIO()

        if img.mode != "RGB":
            img = img.convert("RGB")

        img.save(buffer, format="PNG")

        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        return img_base64
