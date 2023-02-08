import functools


def with_arguments(*argument_names):
    """
    A decorator that we put on facets to let facets declare what arguments they actually use.
    The decorator fetches the required values from the dict and gives them to the function in order.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(obj):
            args = [obj[k] for k in argument_names]
            return func(*args)

        return wrapper

    return decorator
