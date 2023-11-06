import matplotlib as mpl
import numpy as np


def rgb_to_ansi(r: int, g: int, b: int) -> str:
    return f'\33[38;2;{r};{g};{b}m'


def value_to_ansi_color(
        value: float | int,
        vmin: float | int,
        vmax: float | int,
        cmap: str,
) -> str:

    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = mpl.colormaps.get_cmap(cmap)

    color = np.array(cmap(norm(value)))[:3] * 255
    color = color.astype(int)

    return rgb_to_ansi(*color)


def print_rainbow_string(
        text: str,
        end: str = '\n',
        cmap: str = 'rainbow') -> None:

    vmax = len(text)
    for idx, letter in enumerate(text):
        color = value_to_ansi_color(value=idx, vmin=0, vmax=vmax, cmap=cmap)
        print(color + letter + "\033[0m", end='')
    print(end, end='')


if __name__ == '__main__':
    print_rainbow_string('Super niesamowity tekst!')
