from os import path
import json

from pygame import image, font, mixer
"""
Contains code responsible for assets load.
"""


def asset_root_path() -> str:
    """
    Generate root path for assets loading.
    """
    # ./Assets/. root path:
    replace_path_list: list[str] = ['Scripts', 'Application_layer', 'Assets_load.py']
    root_path: str = f"{path.abspath(__file__).replace(path.join(*replace_path_list), '')}"
    return root_path


def image_load(*, art_name: str, file_format: str, asset_type: str) -> image.load:
    """
    Load image by name.
    :param asset_type: String: 'Characters', 'Scenes' or 'UI'.
    :param art_name: must be string with file name in '*/Images/*' folder.
    :param file_format: Image file format: 'png' or 'jpg'.
    :return: Loaded image.
    """
    art_path: str = f"{asset_root_path()}{path.join(*['Images', asset_type, art_name])}"
    scene_image_path: str = f"{art_path}.{file_format}"

    if file_format == 'png':
        return image.load(scene_image_path).convert_alpha()
    if file_format == 'jpg':
        return image.load(scene_image_path).convert()


def sound_load(*, asset_type: str, file_name: str) -> mixer.music.load:
    """
    Load sound by name.
    :param asset_type: String: 'Effects' or 'Music'.
    :param file_name: must be string with file name in '*/Sounds/*' folder.
    :return: Loaded sound.
    """
    sound_path: str = f"{asset_root_path()}{path.join(*['Sounds', asset_type, file_name])}"
    return mixer.music.load(sound_path)


def font_load(*, font_name: str, font_size: int) -> font.Font:
    """
    Load font by name.
    :param font_name: Must be string with file name in '*/Fonts/*' folder.
    :param font_size: Must be int type.
    :return: Loaded font.
    """
    font_path: str = f"{asset_root_path()}{path.join(*['Fonts', font_name])}"
    font_to_load: font.Font = font.Font(font_path, font_size)
    return font_to_load


def json_load(path_list: list[str]) -> json.loads:
    """
    :param path_list: list with strings of folders names and file name.
    :return: Json dict.
    """
    scene_options_path: str = f"{asset_root_path()}{path.join(*path_list)}.{'json'}"
    with open(scene_options_path, 'r', encoding='utf-8') as json_file:
        json_data: str = json_file.read()
        return json.loads(json_data)


def video_load(*, video_name: str, video_format) -> str:
    """
    :param video_name: String name of video file.
    :type video_name: str
    :param video_format: String with the video format of file.
    :type video_format: str
    """
    return f"{asset_root_path()}{path.join(*['Video', video_name])}.{video_format}"
