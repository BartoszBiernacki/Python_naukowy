import argparse
from zadanie1 import process_file, process_folder, fake_progressbar


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Word frequency histogram')
    parser.add_argument('fdir')
    parser.add_argument('-nw', '--n_words', default=10, type=int)
    parser.add_argument('-mwl', '--min_word_length', default=0, type=int)
    parser.add_argument('-iw', '--ignored_words', nargs='+')
    parser.add_argument('-is', '--illegal_substrings', nargs='+')
    parser.add_argument('-os', '--obligatory_substrings', nargs='+')
    parser.add_argument('-cn', '--cmap_name', default='cool')
    parser.add_argument('-f', '--folder', default='')

    args = parser.parse_args()

    fake_progressbar()

    process_file(**args.__dict__)

    if args.folder:
        process_folder(**args.__dict__)
