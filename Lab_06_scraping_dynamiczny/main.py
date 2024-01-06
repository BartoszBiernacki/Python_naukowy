import argparse
from zadanie6 import scrape, save_json

# python main.py koncerty.json
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('fdir')
    args = parser.parse_args()

    save_json(data=scrape(), fdir=args.fdir)
