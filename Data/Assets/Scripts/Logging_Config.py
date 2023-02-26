import logging
from traceback import format_exc
"""
Logging configuration.
"""


def logging_config(*, log_path: str, log_level: int):
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
    logging.basicConfig(
        filename=log_path,
        encoding='utf-8',  # Not mistake: parameter added in python 3.9...
        level=log_level,
        format='%(asctime)s - %(levelname)s:\n%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %p'
    )


def text_for_logging(*, log_text: str, log_error: Exception = None) -> str:
    """
    Wrapper for log text.
    :param log_text: Arbitrary text for logging.
    :type log_text: str
    :param log_error: Custom or standard Exception object..
    :type log_error: Exception
    """
    if log_error is not None:
        log_error: str = f"\nRaise: {repr(log_error)}"
    else:
        log_error: str = ""
    result_text: str = \
        f"{'=' * 30}"\
        f"{log_error}"\
        f"\n{log_text}"\
        f"\n{'-' * 30}"\
        f"\n{format_exc()}"\
        f"\n{'=' * 30}\n\n"
    return result_text


def logger(function):
    """
    Error logger.
    """
    try:
        function()
    except Exception as error:
        logging.error(text_for_logging(
            log_text="Raise Exception:",
            log_error=error
        ))

    return function
