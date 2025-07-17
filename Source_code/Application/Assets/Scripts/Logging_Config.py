from logging import basicConfig, error
from traceback import format_exc
from typing import Callable
"""
Logging configuration.
"""


def logging_config(
        *,
        log_path: str,
        log_level: int
):
    """
    Get logging configuration.
    As result set logging rules.
    --------------
    log_path - path to logging file.
    log_level:
    CRITICAL - 50
    ERROR - 40
    WARNING - 30
    INFO - 20
    DEBUG - 10
    NOTSET - 0
    """
    basicConfig(
        filename=log_path,
        encoding='utf-8',
        level=log_level,
        format='%(asctime)s - %(levelname)s:\n%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %p'
    )


def text_for_logging(
        *,
        log_text: str,
        log_error: Exception = None
) -> str:
    """
    Wrapper for log text.
    :param log_text: Arbitrary text for logging.
    :param log_error: Custom or standard Exception object.
    """
    if log_error is not None:
        log_error: str = f"\nRaise: {repr(log_error)}"
    else:
        log_error: str = ""
    return \
        f"{'=' * 52}"\
        f"{log_error}"\
        f"\n{log_text}"\
        f"\n{'-' * 52}"\
        f"\n{format_exc()}"\
        f"\n{'=' * 52}\n\n"


def error_logger(function: Callable):
    """
    Error logger.
    """
    def wrapper_function(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except Exception as exception:
            error(
                text_for_logging(
                    log_text="Raise Exception:",
                    log_error=exception
                )
            )
        return wrapper_function
    return function
