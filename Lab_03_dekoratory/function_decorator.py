from functools import wraps


def my_decorator(func=None, x=None, y=None):
    print(f"Calling my_decorator with {func = }, {x = }, {y = }")

    def decorator(function):
        print(f"Calling decorator with {function =}")

        @wraps(function)
        def wrapper(*args, **kwargs):
            print(f"Calling wrapper with {args = }, {kwargs = }")
            function(*args, **kwargs)

        return wrapper

    if func is None:
        print('`func is None` --> return decorator')
        return decorator
    else:
        print('`func is not None` --> return decorator(func)')
        return decorator(function=func)


if __name__ == '__main__':
    @my_decorator
    def my_function0(name):
        print(f"Hello func0 {name}!")
    my_function0(name='Bartek')
    print()


    @my_decorator(x=10)
    def my_function1(name):
        print(f"Hello func1 {name}!")
    my_function1(name='Bartek')
    print()


    @my_decorator(x=1, y=2)
    def my_function2(name):
        print(f"Hello func2 {name}!")
    my_function2(name='Bartek')
    print()




