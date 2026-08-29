import base64
import os
import time
from io import BytesIO
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from PIL import Image

from .models import ResponseFormat, get_model
from .prompt import PROMPT

# 環境変数の読み込み
load_dotenv()


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
        model_name = os.getenv("MODEL_NAME", "gemini-3.5-flash-lite")
        model_type = os.getenv("MODEL_TYPE", "Gemini")
        self.llm = get_model(model_name, model_type)

    def annotate(self, img: Image.Image) -> ResponseFormat:
        """画像に対してアノテーションを行う

        Args:
            img (str): 画像データ

        Returns:
            ResponseFormat: アノテーション結果
        """
        # 入力画像のリサイズ（1000x1000に固定）
        img_resized = img.resize(size=(1000, 1000))

        # base64エンコードする
        img_base64 = self.image_to_bytes(img_resized)

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
        start_time = time.perf_counter()
        response = self.llm.invoke([message])
        end_time = time.perf_counter()

        # 全体の処理時間の表示
        print(f"Elapsed time: {round(end_time - start_time, 2)}s")
        self.calc_token_per_sec(response["raw"].response_metadata)

        return response["parsed"]

    def image_to_bytes(self, img: Image.Image) -> str:
        buffer = BytesIO()

        if img.mode != "RGB":
            img = img.convert("RGB")

        img.save(buffer, format="PNG")

        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        return img_base64

    def calc_token_per_sec(self, response_metadata: dict[Any]) -> None:
        """token/secを計算する

        Args:
            response_metadata (dict[Any]): 返答のメタ情報
            generate_time (float): 生成全体にかかった時間
        """
        # token/secの計算
        eval_count = response_metadata.get("eval_count")
        eval_duration = response_metadata.get("eval_duration")
        if eval_count is not None and eval_duration:
            tokens_per_second = round(eval_count / (eval_duration / 1_000_000_000), 2)
            print(f"{tokens_per_second} token/sec")
