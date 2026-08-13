from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from PIL import Image

from .models import BoundingBox


def draw_detection_results(
    image: Image.Image,
    bboxes: Sequence[BoundingBox],
    colors: Sequence[str] | None = None,
    linewidth: int = 2,
    font_size: int = 10,
) -> Figure:
    """PIL画像にバウンディングボックスとクラス名を描画したFigureを返す.

    Args:
        image (Image.Image): 元画像。
        bboxes (Sequence[BoundingBox]): バウンディングボックスの情報
        title (str): 図のタイトル。
        colors (Sequence[str] | None): bboxの色一覧。省略時はデフォルトカラーを使用。
        linewidth (int): bbox線の太さ。
        font_size (int): ラベル文字のフォントサイズ。

    Returns:
        Figure: 描画されたMatplotlib Figure オブジェクト。
    """
    rgb_image = image.convert("RGB") if image.mode != "RGB" else image
    fig, ax = plt.subplots(figsize=(max(5, rgb_image.width / 100), max(4, rgb_image.height / 100)))
    ax.imshow(rgb_image)
    ax.axis("off")
    ax.set_xlim(0, rgb_image.width)
    ax.set_ylim(rgb_image.height, 0)

    default_colors = ["#FF0000", "#00AA00", "#0000FF", "#FF7F0E", "#9C27B0", "#00BCD4"]
    color_list = list(colors) if colors else default_colors

    for index, bbox_info in enumerate(bboxes):
        bbox = bbox_info.bbox
        label = bbox_info.class_name

        if len(bbox) != 4:
            raise ValueError(f"Bounding box at index {index} must have exactly 4 values.")

        x_min, y_min, x_max, y_max = (int(coord) for coord in bbox)
        print(label, [x_min, y_min, x_max, y_max], rgb_image.size)

        color = color_list[index % len(color_list)]
        rect = Rectangle(
            (x_min, y_min),
            x_max - x_min,
            y_max - y_min,
            linewidth=linewidth,
            edgecolor=color,
            facecolor="none",
        )
        ax.add_patch(rect)

        ax.text(
            x_min,
            max(y_min - 5, 0),
            str(label),
            color=color,
            fontsize=font_size,
            fontweight="bold",
            va="bottom",
            ha="left",
            bbox={
                "boxstyle": "round,pad=0.2",
                "facecolor": "white",
                "alpha": 0.7,
                "edgecolor": "none",
            },
        )

    fig.tight_layout()
    plt.show()

    return fig
