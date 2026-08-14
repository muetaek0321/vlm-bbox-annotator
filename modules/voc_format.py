import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Literal

from PIL import Image

from .models import BoundingBox


def create_voc_xml(
    img_path: str | Path,
    annotations: list[BoundingBox],
    output_dir: str | Path | None = None,
    bbox_format: Literal["pixel", "normalized"] = "normalized",
) -> None:
    """画像とBBox情報からPascal VOC形式のXMLファイルを作成する

    Args:
        img_path (str, Path): 対象の画像のファイルパス
        annotations (list[BoundingBox]): LLMが検出したBBoxの情報
        output_dir (str, Path, None): xmlファイルの出力先フォルダ
        bbox_format (Literal["pixel", "normalized"]): BBoxのデータ形式
    """
    # 画像ファイルの存在確認
    img_path = Path(img_path)
    if not img_path.exists():
        raise FileNotFoundError(f"画像ファイルが見つかりません: {img_path}")

    # 画像サイズ取得
    with Image.open(img_path) as image:
        width, height = image.size
        depth = len(image.getbands())

    # 出力先
    if output_dir is None:
        output_dir = img_path.parent
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    xml_path = output_dir / f"{img_path.stem}.xml"

    # Pascal VOC形式のXMLファイルを作成
    annotation = ET.Element("annotation")

    # folder
    folder = ET.SubElement(annotation, "folder")
    folder.text = img_path.parent.name

    # filename
    filename = ET.SubElement(annotation, "filename")
    filename.text = img_path.name

    # path
    path = ET.SubElement(annotation, "path")
    path.text = str(img_path.resolve())

    # source
    source = ET.SubElement(annotation, "source")

    database = ET.SubElement(source, "database")
    database.text = "Unknown"

    # size
    size = ET.SubElement(annotation, "size")

    width_elem = ET.SubElement(size, "width")
    width_elem.text = str(width)

    height_elem = ET.SubElement(size, "height")
    height_elem.text = str(height)

    depth_elem = ET.SubElement(size, "depth")
    depth_elem.text = str(depth)

    # segmented
    segmented = ET.SubElement(annotation, "segmented")
    segmented.text = "0"

    # BBox情報
    for bbox_info in annotations:
        bbox = bbox_info.bbox
        class_name = bbox_info.class_name

        if len(bbox) != 4:
            raise ValueError(f"BBoxは4要素 [xmin, ymin, xmax, ymax] で指定してください: {bbox}")

        xmin, ymin, xmax, ymax = bbox

        # 正規化座標 → ピクセル座標
        if bbox_format == "normalized":
            xmin = xmin * width
            xmax = xmax * width
            ymin = ymin * height
            ymax = ymax * height

        elif bbox_format != "pixel":
            raise ValueError(
                f"bbox_formatは 'pixel' または 'normalized' を指定してください: {bbox_format}"
            )

        # 座標を整数化
        xmin = round(xmin)
        ymin = round(ymin)
        xmax = round(xmax)
        ymax = round(ymax)

        # 画像範囲内にクリップ
        xmin = max(0, min(xmin, width - 1))
        ymin = max(0, min(ymin, height - 1))
        xmax = max(0, min(xmax, width - 1))
        ymax = max(0, min(ymax, height - 1))

        if xmin >= xmax or ymin >= ymax:
            raise ValueError(f"不正なBBoxです: {bbox} -> [{xmin}, {ymin}, {xmax}, {ymax}]")

        # object
        obj = ET.SubElement(annotation, "object")

        name = ET.SubElement(obj, "name")
        name.text = class_name

        pose = ET.SubElement(obj, "pose")
        pose.text = "Unspecified"

        truncated = ET.SubElement(obj, "truncated")
        truncated.text = "0"

        difficult = ET.SubElement(obj, "difficult")
        difficult.text = "0"

        # bndbox
        bndbox = ET.SubElement(obj, "bndbox")

        xmin_elem = ET.SubElement(bndbox, "xmin")
        xmin_elem.text = str(xmin)

        ymin_elem = ET.SubElement(bndbox, "ymin")
        ymin_elem.text = str(ymin)

        xmax_elem = ET.SubElement(bndbox, "xmax")
        xmax_elem.text = str(xmax)

        ymax_elem = ET.SubElement(bndbox, "ymax")
        ymax_elem.text = str(ymax)

    # XMLを書き出す
    tree = ET.ElementTree(annotation)

    # XML宣言 + インデント
    ET.indent(tree, space="    ")

    tree.write(
        xml_path,
        encoding="utf-8",
        xml_declaration=True,
    )
