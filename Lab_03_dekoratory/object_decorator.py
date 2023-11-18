from time import sleep


class Timer:
    def __init__(self, func=None, x=None, y=None):
        def decorator(function):

            def wrapper(*args, **kwargs):
                function(*args, **kwargs)

            return wrapper

        if func is None:
            self.func = decorator
        else:
            self.func = decorator(function=func)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


if __name__ == '__main__':
    @Timer
    def my_function0(name):
        print(f"Hello func0 {name}!")
    print(f'{my_function0 = }')
    my_function0(name='Bartek')
    print()
    sleep(1)

    @Timer(x=10)
    def my_function1(name):
        print(f"Hello func1 {name}!")
    print(f'{my_function1 = }')
    my_function1(name='Bartek')
    print()
    sleep(1)

    @Timer(x=1, y=2)
    def my_function2(name):
        print(f"Hello func2 {name}!")
    my_function2(name='Bartek')
    print()


