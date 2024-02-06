import numpy as np
import cProfile
from pstats import SortKey, Stats
from PIL import Image
from tqdm import tqdm
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt

import compiled_fuctions
from fancy_colors import print_rainbow_string


class Ising:
    def __init__(
            self,
            side_length: int,
            spin_up_density: float,
            J: float,
            B: float,
            beta: float,
            n_makro_steps: int,
            image_prefix: str = None,
            animation_filename: str = None,
            magnetization_filename: str = None,
    ):
        self.J = J
        self.B = B
        self.beta = beta
        self.n_makro_steps = n_makro_steps

        self.grid = compiled_fuctions.make_grid(
            side_length=side_length,
            spin_up_density=spin_up_density,
        )

        self.grid_history = np.empty(
            shape=(n_makro_steps, *self.grid.shape),
            dtype=np.int8,
        )

        self.images = []
        self.image_prefix = image_prefix
        self.animation_filename = animation_filename
        self.magnetization_filename = magnetization_filename

        self.correct_animation_filename()
        self.correct_magnetization_filename()

    def correct_animation_filename(self):
        if self.animation_filename:
            if os.path.splitext(self.animation_filename)[1] == '':
                self.animation_filename += '.gif'

    def correct_magnetization_filename(self):
        if self.magnetization_filename:
            if os.path.splitext(self.magnetization_filename)[1] == '':
                self.magnetization_filename += '.png'

    def run_simulation(self):
        for step in tqdm(
                iterable=range(self.n_makro_steps),
                desc='Przeprowadzanie symulacji',
                ncols=100,
                mininterval=1./60,
                maxinterval=1./10,
        ):
            self.grid_history[step] = np.copy(self.grid)

            compiled_fuctions.makro_step_MC(
                grid=self.grid, J=self.J, B=self.B, beta=self.beta
            )

        self.grid_history[-1] = np.copy(self.grid)

    def make_images(self):
        for step in tqdm(
                iterable=range(self.n_makro_steps),
                desc='Tworzenie obrazków',
                ncols=100,
                mininterval=1. / 60,
                maxinterval=1. / 10,
        ):
            grid = (self.grid_history[step] * 255).astype(np.uint8)
            image = Image.fromarray(grid)

            self.images.append(image)

    def save_images(self):

        def save_image(img, img_prefix, n):
            img.save(f'{img_prefix}{n}.png')

        if folder := os.path.split(self.image_prefix)[0]:
            Path(folder).mkdir(parents=True, exist_ok=True)

        with tqdm(
                total=len(self.images),
                desc='Zapisywanie obrazków',
                ncols=100,
                mininterval=1. / 60,
                maxinterval=1. / 10,
        ) as pbar:
            with ThreadPoolExecutor(
                    max_workers=len(self.images)//5) as executor:
                futures = []

                for step, image in enumerate(self.images):
                    future = executor.submit(
                        save_image,
                        img=image,
                        img_prefix=self.image_prefix,
                        n=step,
                    )
                    futures.append(future)

                for _ in as_completed(futures):
                    pbar.update(1)

    def save_animation(self):
        if folder := os.path.split(self.animation_filename)[0]:
            Path(folder).mkdir(parents=True, exist_ok=True)

        print_rainbow_string(
            'Zapisywanie animacji:  ' +
            'Nie ma paska postępu ale powinno pójść szybko ' +
            '\U0001F44D' * 15,
        )

        self.images[0].save(
            f'{self.animation_filename}',
            save_all=True,
            append_images=self.images[1:],
            duration=100,
            loop=0,
        )

    def save_magnetization(self):
        print_rainbow_string(
            'Obliczenie i zapisanie magnetyzacji:  ' +
            'Też niestety bez paska postępu ' +
            '\U0001F525' * 15,
            cmap='rainbow_r',
        )

        magnetization = self.grid_history.mean(axis=(1, 2))

        plt.plot(magnetization)
        plt.xlabel('Makrokrok')
        plt.ylabel('Magnetyzacja')
        plt.savefig(f'{self.magnetization_filename}', dpi=300)

    def save_simulation(self):
        if self.image_prefix or self.animation_filename:
            self.make_images()

        if self.image_prefix:
            self.save_images()

        if self.animation_filename:
            self.save_animation()

        if self.magnetization_filename:
            self.save_magnetization()


if __name__ == '__main__':
    ising = Ising(
        side_length=100,
        spin_up_density=0.99,
        J=2, B=1, beta=0.0001,
        n_makro_steps=800,
        image_prefix='IMG/step',
        animation_filename='anim',
        magnetization_filename='magnetyzacja',
    )

    with cProfile.Profile() as pr:
        ising.run_simulation()
        ising.save_simulation()
        Stats(pr).strip_dirs().sort_stats(SortKey.TIME).print_stats(5)

    # *************************************************
    # With side_length=1000, n_makro_steps=3:
    #   pure python  = 122.70s; 1x
    #   safe numba   =   0.20s; 615x
    #   unsafe numba =   0.05s; 2450x
    # *************************************************

    # Unsafe numba means using `parallel = True` in `makro_step_MC`
    # it's unsafe, because in mikrostep1 thread1 can deside to flip spin,
    # so in mikrostep2 this spin should be flipped, but this process take
    # some time and if in the meantime thread2 will ask for value of this
    # spin it may not be updated yet. For grid size like 1000x1000 it's
    # very unlikely to happen, but still possible. Even if it occurs
    # simulation result almost will not be affected as it relies on
    # stohastic process.

