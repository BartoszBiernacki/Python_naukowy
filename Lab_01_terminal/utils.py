from collections import Counter
import ascii_graph
import matplotlib as mpl
import numpy as np
from ascii_graph import colordata
import os
import glob
import re


def contains_any_substring(text: str, substrings: list[str]) -> bool:
    return any(substring in text for substring in substrings)


def contains_all_substrings(text: str, substrings: list[str]) -> bool:
    return all(substring in text for substring in substrings)


def rgb_to_ansi(r: int, g: int, b: int) -> str:
    return f'\33[38;2;{r};{g};{b}m'


def value_to_ansi_color(
        value: float | int,
        vmin: float | int,
        vmax: float | int,
        cmap_name: str,
) -> str:

    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = mpl.colormaps.get_cmap(cmap_name)

    color = np.array(cmap(norm(value)))[:3] * 255
    color = color.astype(int)

    return rgb_to_ansi(*color)


def count_words(
        text: str,
        n_words: int = None,
        min_word_length: int = 0,
        ignored_words: list[str] = None,
        illegal_substrings: list[str] = None,
        obligatory_substrings: list[str] = None,
) -> list[tuple[str, int]]:

    text = re.sub(r'\s+', ' ', text).strip()

    words = (text
             .replace(',', '').replace(';', '').replace(':', '')
             .replace('.', '').replace('?', '').replace('!', '')
             .replace('[', '').replace(']', '')
             .replace('(', '').replace(')', '')
             .replace('"', '')
             .lower()
             .split(' ')
             )

    if ignored_words is not None:
        words = [w for w in words if w not in ignored_words]

    counts = Counter(words).most_common()
    counts = [count for count in counts if len(count[0]) >= min_word_length]

    if ignored_words is not None:
        counts = [count for count in counts if count[0] not in ignored_words]

    if illegal_substrings is not None:
        counts = [
            count for count in counts if not
            contains_any_substring(
                text=count[0], substrings=illegal_substrings)
        ]

    if obligatory_substrings is not None:
        counts = [
            count for count in counts if
            contains_all_substrings(
                text=count[0], substrings=obligatory_substrings)
        ]

    return counts[:n_words] if n_words is not None else counts


def read_text_file(fdir: str) -> str:
    with open(fdir, encoding='utf8') as f:
        lines = f.readlines()
    return ''.join(lines)


def show_histogram(
        counts: list[tuple[str, int]],
        cmap_name: str,
        fdir: str,
) -> None:

    # A workaround to make ascii_graph working with python 3.10+
    import collections.abc
    collections.Iterable = collections.abc.Iterable

    # prepare 'colored' data for histogram
    data = colordata.hcolor(
        data=counts,
        thresholds={
            count[1]: value_to_ansi_color(
                value=count[1],
                vmin=min(count[1] for count in counts),
                vmax=max(count[1] for count in counts),
                cmap_name=cmap_name,
            )
            for count in counts
        },
    )
    graph = ascii_graph.Pyasciigraph(
        multivalue=False,
        titlebar='=',
    )
    fname = rgb_to_ansi(0, 255, 0) + os.path.split(fdir)[1] + "\033[0m"
    title = f'\nHistogram liczby słów w pliku {fname}'
    for line in graph.graph(label=title, data=data):
        print(line)


def fdirs_from_folder(folder_path: str) -> list[str]:
    return glob.glob(f'{folder_path}/*.*')

