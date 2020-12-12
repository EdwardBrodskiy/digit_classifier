from math import fmod
from typing import List


def generate_color_set(size: int) -> List[str]:
    color_set = []
    saturation, light = 1, 0.5
    step = 360 // size
    for hue in range(0, 360, step):
        color_set.append(hsl_to_rgb(hue, saturation, light))
    return color_set


def hsl_to_rgb(hue: float, saturation: float, light: float) -> str:
    c = (1.0 - abs(2.0 * light - 1.0)) * saturation
    x = c * (1.0 - abs(fmod(hue / 60, 2) - 1.0))
    m = light - c / 2.0

    inverse_color = [0, 0, 0]
    if hue < 60.0:
        inverse_color = [c, x, 0]
    elif hue < 120.0:
        inverse_color = [x, c, 0]
    elif hue < 180.0:
        inverse_color = [0, c, x]
    elif hue < 240.0:
        inverse_color = [0, x, c]
    elif hue < 300.0:
        inverse_color = [x, 0, c]
    elif hue < 360.0:
        inverse_color = [c, 0, x]

    color = "#"
    for i in range(3):
        sub_col = hex(int(round((inverse_color[i] + m) * 255, 0)))[2:]
        if len(sub_col) == 1:
            sub_col = '0' + sub_col
        color += sub_col

    return color

