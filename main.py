import json
from pathlib import Path

from PIL import Image

from modules.annotator import VLMAnnotateAssistant
from modules.visualize import draw_detection_results
from modules.voc_format import create_voc_xml


def main() -> None:
    data_path = Path("./data")

    # クラス情報の読み込み
    with open("classes_info.json", mode="r", encoding="utf-8") as f:
        classes_info = json.load(f)

    # アノテーターの初期化
    annotator = VLMAnnotateAssistant(classes_info)

    # 画像1枚ずつに処理を適用
    for img_path in data_path.iterdir():
        if img_path.suffix.lower() not in [".jpg", ".bmp", ".png", ".jpeg"]:
            continue

        # 画像の読み込み
        img = Image.open(img_path)

        # VLMによる物体検出を実行
        res = annotator.annotate(img)

        # 可視化して確認
        draw_detection_results(img, res.bboxes, classes=list(classes_info.keys()))

        # Pascal VOC形式のXMLファイルを作成
        create_voc_xml(img_path=img_path, annotations=res.bboxes)


if __name__ == "__main__":
    main()
