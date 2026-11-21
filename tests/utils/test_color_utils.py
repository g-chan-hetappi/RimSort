import pytest
from PySide6.QtGui import QColor

from app.utils.color_utils import get_contrasting_text_color, relative_luminance

BLACK = "#000000"
WHITE = "#ffffff"


@pytest.mark.parametrize(
    "background",
    [
        "#ffffff",  # white
        "#ffff00",  # yellow
        "#ffd700",  # gold
        "#00ffff",  # cyan
        "#90ee90",  # light green
        "#ffa500",  # orange
        "#cccccc",  # light grey
    ],
)
def test_light_backgrounds_get_black_text(background: str) -> None:
    assert get_contrasting_text_color(QColor(background)).name() == BLACK


@pytest.mark.parametrize(
    "background",
    [
        "#000000",  # black
        "#000080",  # navy
        "#8b0000",  # dark red
        "#006400",  # dark green
        "#800080",  # purple
        "#0000ff",  # blue
        "#444444",  # dark grey
    ],
)
def test_dark_backgrounds_get_white_text(background: str) -> None:
    assert get_contrasting_text_color(QColor(background)).name() == WHITE


def test_relative_luminance_extremes() -> None:
    assert relative_luminance(QColor("#000000")) == pytest.approx(0.0)
    assert relative_luminance(QColor("#ffffff")) == pytest.approx(1.0)


def test_text_color_is_always_the_more_readable_choice() -> None:
    """The chosen text color never has a lower contrast ratio than the other."""
    for r in range(0, 256, 51):
        for g in range(0, 256, 51):
            for b in range(0, 256, 51):
                bg = QColor(r, g, b)
                lum = relative_luminance(bg)
                black = (lum + 0.05) / 0.05
                white = 1.05 / (lum + 0.05)
                chosen = get_contrasting_text_color(bg).name()
                assert chosen == (BLACK if black >= white else WHITE)
