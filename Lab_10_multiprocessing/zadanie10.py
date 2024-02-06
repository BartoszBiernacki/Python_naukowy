import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
from PIL import Image
from scipy.ndimage import gaussian_filter
import numpy as np
from io import BytesIO


def scrape_png_urls(
        url: str = 'https://www.if.pw.edu.pl/~mrow/dyd/wdprir/'
) -> list[str]:

    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all(
        'a',
        href=lambda href: href and href.endswith('.png'),
    )

    return [url + link['href'] for link in links]


def fdirs_for_png_urls(urls: list[str]) -> list[str]:
    folder = 'Downloaded'
    Path(folder).mkdir(parents=True, exist_ok=True)

    fdirs = []
    for url in urls:
        filename = os.path.basename(url)
        fdir = os.path.join(folder, filename)
        fdirs.append(fdir)
    return fdirs


def download_file(url: str) -> Image:
    img_response = requests.get(url)
    img = Image.open(BytesIO(img_response.content))
    return img


def rgba_to_gray(img: Image) -> Image:
    return img.convert('LA')


def apply_gaussian_blur_to_image(img: Image) -> Image:
    img = gaussian_filter(img, sigma=10)
    img = (img-np.min(img))/(np.max(img)-np.min(img))  # rescale to [0, 1]
    img = (img*255).astype(np.uint8)  # rescale to [0, 255]
    img = Image.fromarray(img)
    return img


def save_image(img: Image, fdir: str) -> None:
    img.save(fdir)

