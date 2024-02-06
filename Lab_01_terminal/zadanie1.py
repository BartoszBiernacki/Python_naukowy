import time

import utils


def process_file(
    fdir: str,
    n_words: int = 10,
    min_word_length: int = 0,
    ignored_words: list[str] = None,
    illegal_substrings: list[str] = None,
    obligatory_substrings: list[str] = None,
    cmap_name: str = 'cool',
    **kwargs,
) -> None:

    counts = utils.count_words(
        text=utils.read_text_file(fdir),
        n_words=n_words,
        min_word_length=min_word_length,
        ignored_words=ignored_words,
        illegal_substrings=illegal_substrings,
        obligatory_substrings=obligatory_substrings,
    )

    utils.show_histogram(counts=counts, cmap_name=cmap_name, fdir=fdir)


def process_folder(folder: str, **kwargs) -> None:
    for fdir in utils.fdirs_from_folder(folder_path=folder):
        kwargs['fdir'] = fdir
        process_file(**kwargs)


def fake_progressbar() -> None:
    from tqdm import tqdm
    from time import sleep

    settings = {
        'desc': (
            utils.rgb_to_ansi(255, 128, 0)
            + 'Przemiatanie plików'
            + "\033[0m"
        ),
        'colour': 'green',
        'mininterval': 1/60,
        'maxinterval': 1/60 * 5,
        'ascii': " 123456789▒",
    }
    for _ in tqdm(range(400), **settings):
        sleep(0.01)





