from PIL import Image

from modules.visualize import draw_detection_results


def test_draw_detection_results_creates_boxes_for_image() -> None:
    image = Image.new("RGB", (100, 100), color=(255, 255, 255))
    bboxes = [[10, 20, 40, 60], [50, 10, 90, 50]]
    labels = ["cat", "dog"]

    fig = draw_detection_results(image, bboxes, labels)

    assert fig is not None
    assert len(fig.axes) == 1
    assert len(fig.axes[0].patches) == 2
    assert fig.axes[0].get_title() == "Detection Results"
