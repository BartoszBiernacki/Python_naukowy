import argparse
from zadanie5 import scrape, save_json

# python main.py bomba.json
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Static scraper')
    parser.add_argument('fdir')
    args = parser.parse_args()

    save_json(data=scrape(), fdir=args.fdir)
