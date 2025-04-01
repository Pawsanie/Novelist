from logging import basicConfig, error
from traceback import format_exc
from typing import Callable
"""
Logging configuration.
"""


def logging_config(
        *,
        logg_path: str,
        logg_level: int
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
        filename=logg_path,
        encoding='utf-8',
        level=logg_level,
        format='%(asctime)s - %(levelname)s:\n%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %p'
    )


def text_for_logging(
        *,
        logg_text: str,
        logg_error: Exception = None
) -> str:
    """
    Wrapper for log text.
    :param logg_text: Arbitrary text for logging.
    :param logg_error: Custom or standard Exception object.
    """
    if logg_error is not None:
        logg_error: str = f"\nRaise: {repr(logg_error)}"
    else:
        logg_error: str = ""
    return \
        f"{'=' * 52}"\
        f"{logg_error}"\
        f"\n{logg_text}"\
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
                    logg_text="Raise Exception:",
                    logg_error=exception
                )
            )
        return wrapper_function
    return function
