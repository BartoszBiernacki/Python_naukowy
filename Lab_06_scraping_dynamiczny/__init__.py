import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
import multiprocessing
import functools

import sys


def fibon(n):
    if n < 2:
        return n

    return fibon(n - 2) + fibon(n - 1)


if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as ex:
        futures = [ex.submit(fibon, n) for n in range(33)]
        results = [future.result() for future in futures]

