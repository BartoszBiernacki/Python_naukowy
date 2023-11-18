import numpy as np
from time import sleep


class Timer:
    def __init__(self, func=None, useless_arg=None):
        self._times = []

        def decorator(function):
            def wrapper(*args, **kwargs):

                from time import perf_counter
                start_time = perf_counter()

                result = function(*args, **kwargs)

                end_time = perf_counter()
                self._times.append(end_time - start_time)

                return result

            wrapper.exec_times = self.exec_times
            wrapper.mean_exec_time = self.mean_exec_time
            wrapper.min_exec_time = self.min_exec_time
            wrapper.max_exec_time = self.max_exec_time
            wrapper.std_exec_time = self.std_exec_time

            return wrapper

        if func is None:
            self.func = decorator
        else:
            self.func = decorator(function=func)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def exec_times(self) -> list[float]:
        return self._times

    def mean_exec_time(self) -> float:
        return np.array(self.exec_times()).mean()

    def min_exec_time(self) -> float:
        return np.array(self.exec_times()).min()

    def max_exec_time(self) -> float:
        return np.array(self.exec_times()).max()

    def std_exec_time(self) -> float:
        return np.array(self.exec_times()).std()


if __name__ == '__main__':
    # Dekorator bez podania argumentów
    @Timer
    def my_function0(name='World'):
        print('Starting calculations ...')
        sleep(np.random.uniform(0, 2))
        print(f"Hello {name}!", '\n')

    my_function0(name='Arnold')
    my_function0(name='Bartek')
    my_function0(name='Celina')
    my_function0(name='Dodger')

    print(f'execution times: {my_function0.exec_times()}')
    print(f'mean execution time: {my_function0.mean_exec_time()}')
    print(f'min execution time: {my_function0.min_exec_time()}')
    print(f'max execution time: {my_function0.max_exec_time()}')
    print(f'std execution time: {my_function0.std_exec_time()}', '\n')

    # Dekorator z argumentem
    @Timer(useless_arg=0)
    def my_function1(name='World'):
        print('Starting calculations ...')
        sleep(np.random.uniform(0, 2))
        print(f"Hello {name}!", '\n')

    my_function1(name='Ela')
    my_function1(name='Flip')
    my_function1(name='Grażka')

    print(f'execution times: {my_function1.exec_times()}')
    print(f'mean execution time: {my_function1.mean_exec_time()}')
    print(f'min execution time: {my_function1.min_exec_time()}')
    print(f'max execution time: {my_function1.max_exec_time()}')
    print(f'std execution time: {my_function1.std_exec_time()}')


