from os import path, walk, makedirs
import json
from time import strftime, localtime, strptime

from .Universal_computing import SingletonPattern
from .Settings_Keeper import SettingsKeeper
from .Scene_Validator import SceneValidator
"""
Contend code for save/load system.
"""


class SaveKeeper(SingletonPattern):
    """
    Responsible for saving and loading game progress.
    Stores all saves and their data.
    """
    def __init__(self, *, scene_validator):
        """
        :param scene_validator: SceneValidator exemplar.
                            Responsible for scene order and scene construction.
        :type scene_validator: SceneValidator
        """
        # Program layers settings:
        self.settings_keeper: SettingsKeeper = SettingsKeeper()
        self.scene_validator: SceneValidator = scene_validator

        # Path settings:
        script_root_path: str = path.abspath(__file__) \
            .replace(path.join(
                *['Assets', 'Scripts', 'Save_Master.py']
            ), '')
        self.save_folder_path: str = path.join(*[script_root_path, 'Saves'])

        # Saves collection:
        self.saves_dict: dict | None = {}
        self.saves_read()

    def save(self, *, auto_save: bool):
        """
        Save game progress.
        """
        # Path settings:
        if auto_save is True:
            save_name: str = "AutoSave"
        else:
            time_path_part: str = strftime("%Y-%m-%d_%H-%M-%S", localtime())
            save_name: str = f"save__{time_path_part}"
        save_path: str = path.join(*[self.save_folder_path, save_name])

        # Saving game progress:
        if path.exists(self.save_folder_path) is False:
            makedirs(self.save_folder_path)
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(
               self.get_game_progress_data_for_save()
            )

    def get_game_progress_data_for_save(self) -> str:
        """
        Get progress data for save it like json in file.
        """
        data_to_save: dict[str] = {
            "scene": self.scene_validator.scene,
            "date": strftime("%Y:%m:%d:%H:%M:%S", localtime())
        }
        return json.dumps(data_to_save, indent=4)

    def continue_game(self) -> str:
        """
        Get scene name for game continue.
        Used in StartMenu class from "UI_Start_menu.py".

        :return: String with scene name from last save.
        """
        self.saves_read()
        if self.saves_dict is None:
            return 'scene_01'
        else:
            last_save: list[str] = sorted(self.saves_dict.keys(), reverse=True)
            return self.saves_dict[last_save[0]]["save_data"]["scene"]

    def saves_read(self):
        """
        Read save directory.
        """
        # Save path dos not exist:
        if path.exists(self.save_folder_path) is False:
            self.saves_dict: None = None
            return
        # Check save path:
        save_files: list[str] = walk(self.save_folder_path).__next__()[-1]
        if len(save_files) == 0:
            self.saves_dict: None = None
            return
        else:
            self.saves_dict: dict = {}
            for file in save_files:
                with open(
                        path.join(
                            *[self.save_folder_path, file]
                        ), 'r') as save_file:
                    # Generate save frame for save collection:
                    save_data: dict = json.load(save_file)
                    self.saves_dict.update({
                        strptime(save_data['date'], "%Y:%m:%d:%H:%M:%S"): {
                            "file_name": file,
                            "save_data": save_data
                        }
                    })
