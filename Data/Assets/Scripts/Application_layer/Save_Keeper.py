from os import path, walk, makedirs
import json
from time import strftime, localtime, strptime
import logging

from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..User_Interface.Interface_Controller import InterfaceController
from .Settings_Keeper import SettingsKeeper
from .Scene_Validator import SceneValidator
from ..Logging_Config import text_for_logging
from ..User_Interface.UI_Button import Button
"""
Contend code for save/load system.
"""


class SaveKeeper(SingletonPattern):
    """
    Responsible for saving and loading game progress.
    Stores all saves and their data.
    """
    def __init__(self):
        # Program layers settings:
        self.settings_keeper: SettingsKeeper = SettingsKeeper()
        self.scene_validator: SceneValidator = SceneValidator()
        self.interface_controller: InterfaceController = InterfaceController()

        # Path settings:
        script_root_path: str = path.abspath(__file__) \
            .replace(path.join(
                *['Assets', 'Scripts', 'Save_Keeper.py']
            ), '')
        self.save_folder_path: str = path.join(*[script_root_path, 'Saves'])

        # Saves collection:
        self.saves_dict: dict | None = {}
        self.save_buttons_collection: dict | None = None

        # Save/Load buttons reference:
        self.save_buttons_reference: dict = self.interface_controller.buttons_dict['ui_save_menu_buttons']
        self.load_buttons_reference: dict = self.interface_controller.buttons_dict['ui_load_menu_buttons']

        self.reread: bool = True

    def update_ui_buttons(self, menu_data: dict):
        """
        Update menu`s buttons dict in 'InterfaceController.buttons_dict'.
        """
        if menu_data["menu_object"].status is True:
            menu_data["menu_buttons"] = menu_data["menu`s_buttons_reference"]

            save_cell_buttons: dict = self.get_cell_buttons()
            for key, value in save_cell_buttons.items():
                menu_data["menu_buttons"].setdefault(key, value)

    def get_cell_buttons(self) -> dict[Button]:
        """
        Generate cell buttons for Save/Load UI.
        :return: dict[Button]
        """
        # Button(
        #     button_name=...,
        #     button_text=...,
        #     button_image_data=...,
        #     button_text_localization_dict=...
        # )

        if self.reread is True:
            self.saves_read()

        if self.saves_dict is None:
            return {}
        else:
            ...
            return {}

    def generate_save_slots_buttons(self):
        """
        Add save cell buttons for Save/Load UI.
        """
        from ..User_Interface.UI_Menus.UI_Save_menu import SaveMenu
        from ..User_Interface.UI_Menus.UI_Load_menu import LoadMenu

        # UI collection:
        ui_collection: dict = {
            "save": {
                "menu_object": SaveMenu(),
                "menu_buttons": self.interface_controller.buttons_dict['ui_save_menu_buttons'],
                "menu`s_buttons_reference": self.save_buttons_reference
            },
            "load": {
                "menu_object": LoadMenu(),
                "menu_buttons": self.interface_controller.buttons_dict['ui_load_menu_buttons'],
                "menu`s_buttons_reference": self.load_buttons_reference
            }
        }

        for menu_data in ui_collection:
            self.update_ui_buttons(ui_collection[menu_data])

    def get_save_buttons_collection(self) -> dict | None:
        """
        Get saves collection.
        """
        return self.save_buttons_collection

    def save(self, *, auto_save: bool = True, save_cell: int = 1):
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
               self.get_game_progress_data_for_save(save_cell)
            )

    def get_game_progress_data_for_save(self, save_cell: int) -> str:
        """
        Get progress data for save it like json in file.
        """
        data_to_save: dict[str] = {
            "scene": self.scene_validator.scene,
            "date": strftime("%Y:%m:%d:%H:%M:%S", localtime()),
            "save_cell": save_cell
        }
        return json.dumps(data_to_save, indent=4)

    def continue_game(self) -> str or bool:
        """
        Get scene name for game continue.
        Used in StartMenu class from "UI_Start_menu.py".

        :return: String with scene name from last save.
                 Or False if save file was corrupted.
        """
        self.saves_read()
        if self.saves_dict is None or len(self.saves_dict) == 0:
            return 'scene_01'
        else:
            last_save: list[str] = sorted(self.saves_dict.keys(), reverse=True)

            try:
                return self.saves_dict[last_save[0]]["save_data"]["scene"]

            # Logging errors:
            except Exception as error:
                try:
                    corrupted_data = self.saves_dict[last_save[0]]
                except Exception as corrupted_data_error:
                    corrupted_data = corrupted_data_error
                logging.error(
                    text_for_logging(
                        log_text=
                        f"SaveKeeper Exception in 'continue_game' method:"
                        f"\n{'-' * 30}"
                        f"\nSaves list: \n{corrupted_data}",
                        log_error=error
                    ))
                return False

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
                try:
                    with open(
                            path.join(
                                *[self.save_folder_path, file]
                            ), 'r') as save_file:
                        # Generate save frame for save collection:
                        file_data: str = save_file.read()
                        save_data: dict = json.loads(file_data)
                        self.saves_dict.update({
                            strptime(save_data['date'], "%Y:%m:%d:%H:%M:%S"): {
                                "file_name": file,
                                "save_data": save_data
                            }
                        })

                # Logging Errors:
                except Exception as error:
                    try:
                        save_data: str = json.loads(file_data)
                    except Exception as save_data_error:
                        save_data: Exception = save_data_error
                    logging.error(text_for_logging(
                        log_text=
                        f"SaveKeeper Exception in 'saves_read' method:"
                        f"\nIssue with: {repr(error)}"
                        f"\n{'-'*30}"
                        f"\nFile name: {file}"
                        f"\n{'-'*30}"
                        f"\nFile data:"
                        f"\n{save_data}",
                        log_error=error
                    ))

        self.reread: bool = False
