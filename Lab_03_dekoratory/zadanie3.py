from functools import wraps


def my_decorator(func=None, x=6, y=8):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            print("Before function call", x, y)
            function(*args, **kwargs)
            print("After function call", x, y)
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(function=func)


@my_decorator(x=1, y=2)
def my_function1(x, y, z):
    print("Hello World!", x + y + z)


class ObjectDecorator:
    def __init__(self, func=None, k=0):
        print('calling __init__')

        def decorator(function):
            print('calling decorator')

            def wrapper(*args, **kwargs):
                print('calling wrapper')
                function(*args, **kwargs)

            return wrapper

        if func is None:
            print('self.func = decorator')
            self.func = decorator
        else:
            self.func = decorator(function=func)

    def __call__(self, *args, **kwargs):
        print('Calling __call__')
        self.func(*args, **kwargs)


# @ObjectDecorator(k=3)
def my_function2(a=4):
    print(f"Calling my_function2")


if __name__ == '__main__':
    # my_function = my_decorator(x, y, z, e)(my_function)
    my_function2 = ObjectDecorator(k=5)(my_function2)

    my_function2(a=4)

    print()

    # my_function2()

    print()

    # my_function2()



