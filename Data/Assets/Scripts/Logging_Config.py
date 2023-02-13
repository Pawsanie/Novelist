import logging
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
        datefmt='%Y-%m-%d %H:%M:%S %p')
