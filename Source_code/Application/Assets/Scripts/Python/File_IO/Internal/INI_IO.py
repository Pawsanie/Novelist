from configparser import ConfigParser
"""
Contains code responsible for INI assets I/O.
"""


def ini_load_internal(path: str) -> dict | None:
    """
    Load INI for FileLoader.
    :param path: Absolute path to file as string.
    :return: As exemple: {
                "section_name": {
                    "field_name": value,
                    ...
                },
                ...
            } | None # If file is empty.
    """
    with open(
            file=path,
            mode='r',
            encoding='utf-8'
    ) as ini_file:

        config_data: ConfigParser = ConfigParser(
            inline_comment_prefixes=(
                "#",
            )
        )

        config_data.read_file(
            ini_file
        )

        if not config_data.sections():
            return None

        return {
            section: dict(
                config_data[section]
            )
            for section in config_data.sections()
        }


def ini_output_internal(
    *,
    path: str,
    data: dict
):
    """
    Save INI file for FileOutput.
    :param path: Absolute path to file as string.
    :param data: New INI config for writing.
                 As exemple: {
                    "section_name": {
                        "comment": str,
                        "fields": {
                            "field_name": {
                                    "comment": str,
                                    "value": value_data
                                },
                            ...
                        }
                    },
                    ...
                }
    """
    comment_flag: str = "comment"

    with open(
            file=path,
            mode='w',
            encoding='utf-8'
    ) as file:
        for section_name, section_data in data.items():
            if comment_flag in section_data:
                file.write(
                    f"# {section_data[comment_flag]}\n"
                )

            file.write(
                f"[{section_name}]\n"
            )

            for field_key, field_data in section_data["fields"].items():
                comment_data: str = f"{
                    str("") if comment_flag not in field_data 
                    else str(
                        f"  # {field_data[comment_flag]}"
                    ) 
                }"

                file.write(
                    f"{field_key} = {field_data["value"]}{comment_data}\n"
                )

            file.write("\n")
