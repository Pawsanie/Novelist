from csv import reader
"""
Contains code responsible for csv assets load.
"""


def csv_load_internal(path: str) -> tuple[
    list[str],
    list[list[str]]
]:
    """
    Load csv table for FileLoader.
    :param path: Absolute path to file as string.
    """
    with open(
            file=path,
            mode='r',
            newline='',
            encoding="utf-8"
    ) as file:
        header, *rows = reader(
            file,
            delimiter="\t"
        )
        return header, rows
