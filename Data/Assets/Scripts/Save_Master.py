from os import path, walk, makedirs
import json
from time import strftime, localtime

from .Universal_computing import SingletonPattern
from .User_Interface.Interface_Controller import InterfaceController
"""
Contend code for save/load system.
"""


class SaveMaster(SingletonPattern):
    """
    Responsible for saving and loading game progress.
    """
    def __init__(self):
        # Program layers settings:

        # Path settings:
        script_root_path: str = path.abspath(__file__) \
            .replace(path.join(*['Assets', 'Scripts', 'Save_Master.py']), '')
        self.save_folder_path: str = f"{script_root_path}{path.join(*['Saves'])}"
        # Saves collection:
        self.saves_dict: dict | None = {}

        self.save()

    def save(self):
        """
        Save game progress.
        """
        # Path settings:
        save_type: str = "_save"
        time_path_part: str = strftime("%Y-%m-%d_%H-%M-%S", localtime())
        save_name: str = f"{time_path_part}{save_type}"
        save_path: str = path.join(*[self.save_folder_path, save_name])
        # Saving game progress:
        if path.exists(self.save_folder_path) is False:
            makedirs(self.save_folder_path)
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(
               self.get_game_progress_data_for_save()
            )

    def get_game_progress_data_for_save(self) -> str:
        data_to_save: dict[str] = {
            "scene": "test",
            "date": strftime("%Y:%m:%d:%H:%M:%S", localtime())
        }
        return str(data_to_save)

    def load(self):
        ...

    def continue_game(self):
        self.saves_read()

    def saves_read(self):
        """
        Read save directory.
        """
        if path.exists(self.save_folder_path) is False:
            self.saves_dict: None = None
            return
        save_files: list[str] = walk(self.save_folder_path).__next__()[-1]
        if len(save_files) == 0:
            self.saves_dict: None = None
