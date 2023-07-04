from concurrent.futures import ThreadPoolExecutor
"""
Contains a universal coroutine decorator.
"""


def coroutine_decorator(func):
    """
    Decorator with asynchronous results.
    """
    def coroutine(*args, **kwargs):
        with ThreadPoolExecutor(max_workers=1) as executor:
            task = func(*args, **kwargs)
            try:
                callback = executor.submit(task)
                try:
                    return callback.result()
                except Exception as error:
                    ...
            except Exception as error:
                ...
    return coroutine
