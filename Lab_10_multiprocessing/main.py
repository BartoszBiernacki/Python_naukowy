import multiprocessing
from zadanie10 import *
from dataclasses import dataclass
from time import perf_counter


@dataclass
class ImageDownloadInfo:
    url: str
    fdir: str


def process_image(img_info: ImageDownloadInfo):
    img = download_file(url=img_info.url)
    img = rgba_to_gray(img=img)
    img = apply_gaussian_blur_to_image(img=img)
    save_image(img=img, fdir=img_info.fdir)


def sequential(urls: list[str], fdirs: list[str]) -> None:
    for url, fdir in zip(urls, fdirs):
        img_info = ImageDownloadInfo(url=url, fdir=fdir)
        process_image(img_info=img_info)


def parallel(urls: list[str], fdirs: list[str]) -> None:
    images_info = [
        ImageDownloadInfo(url=url, fdir=fdir)
        for url, fdir in zip(urls, fdirs)
    ]
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(process_image, images_info)


if __name__ == "__main__":
    png_urls = scrape_png_urls()
    png_fdirs = fdirs_for_png_urls(urls=png_urls)

    t_start = perf_counter()
    sequential(urls=png_urls, fdirs=png_fdirs)
    print(f'Sequential: {perf_counter() - t_start}s')

    t_start = perf_counter()
    parallel(urls=png_urls, fdirs=png_fdirs)
    print(f'Parallel: {perf_counter() - t_start}s')



