from PySide6.QtGui import QColor

_WHITE = QColor(255, 255, 255)
_BLACK = QColor(0, 0, 0)


def _linearize(channel: int) -> float:
    """Convert an 8-bit sRGB channel to its linear-light value (WCAG 2.x).

    :param channel: sRGB channel value in the range 0-255.
    :return: Linear-light value in the range 0.0-1.0.
    """
    srgb = channel / 255
    if srgb <= 0.04045:
        return srgb / 12.92
    return float(((srgb + 0.055) / 1.055) ** 2.4)


def relative_luminance(color: QColor) -> float:
    """Return the WCAG relative luminance of a color.

    :param color: The color to measure. Alpha is ignored.
    :return: 0.0 for pure black up to 1.0 for pure white.
    """
    return (
        0.2126 * _linearize(color.red())
        + 0.7152 * _linearize(color.green())
        + 0.0722 * _linearize(color.blue())
    )


def get_contrasting_text_color(background: QColor) -> QColor:
    """Pick black or white text, whichever is more readable on a background.

    Both candidates are compared by WCAG contrast ratio and the higher one wins.
    A background is therefore treated as "light" (black text) when its relative
    luminance is above roughly 0.179, and "dark" (white text) otherwise.

    :param background: The background color the text will be drawn on.
    :return: ``QColor`` black or white.
    """
    luminance = relative_luminance(background)
    contrast_with_white = 1.05 / (luminance + 0.05)
    contrast_with_black = (luminance + 0.05) / 0.05
    return QColor(_BLACK if contrast_with_black > contrast_with_white else _WHITE)
