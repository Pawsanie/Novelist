from os import path, walk, makedirs
import json
from time import strftime, localtime, strptime
import logging

from pygame import image, transform, Surface

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
                *['Assets', 'Scripts', 'Application_layer', 'Save_Keeper.py']
            ), '')
        self.save_folder_path: str = path.join(
            *[script_root_path, 'Saves']
        )

        # Saves collection:
        self.saves_dict: dict = {}
        self.save_buttons_collection: dict = {}
        self.load_buttons_collection: dict = {}
        self.save_load_collections: dict[str, dict[Button | None]] = {
            "save": self.save_buttons_collection,
            "load": self.load_buttons_collection
        }

        # Save/Load buttons reference:
        self.save_buttons_reference: dict = self.interface_controller.buttons_dict['ui_save_menu_buttons']
        self.load_buttons_reference: dict = self.interface_controller.buttons_dict['ui_load_menu_buttons']

        self.reread: bool = True
        self.button_image: str = "screen_preview"
        self.autosave_name: str = "AutoSave"

    def update_ui_buttons(self, *, menu_data: dict, save_type: str):
        """
        Update menu`s buttons dict in 'InterfaceController.buttons_dict'.
        """
        if menu_data["menu_object"].status is True:
            menu_data["menu_buttons"] = menu_data["menu`s_buttons_reference"]

            save_cell_buttons: dict = self.save_load_collections[save_type]
            for key, value in save_cell_buttons.items():
                menu_data["menu_buttons"].setdefault(key, value)

    def generate_cell_buttons(self):
        """
        Generate cell buttons for Save/Load UI.
        :return: dict[Button]
        """
        if self.reread is True:
            self.saves_read()

        if self.saves_dict is None:
            ...
        else:
            # If game was saved:
            if len(self.saves_dict) > 0:
                for save in self.saves_dict:
                    save_data: dict = self.saves_dict[save]
                    # Cells with save data:
                    button_image_path: str = path.join(
                        *[self.save_folder_path, save_data['file_name'], self.button_image]
                    )
                    for key, collection in self.save_load_collections.items():
                        collection.setdefault(
                            save_data['file_name'],
                            Button(
                                button_name=save_data['save_data']['date'],
                                button_text=None,
                                button_image_data={
                                    'sprite_name': button_image_path,
                                    'index_number': save_data['save_data']['save_cell'],
                                    'type': key
                                },
                                button_text_localization_dict={},
                                have_real_path=True
                            )
                        )
                self.save_buttons_collection.pop(self.autosave_name)

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

        self.generate_cell_buttons()

        for save_type in ui_collection:
            self.update_ui_buttons(
                menu_data=ui_collection[save_type],
                save_type=save_type
            )

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
            save_name: str = self.autosave_name
        else:
            time_path_part: str = strftime("%Y-%m-%d_%H-%M-%S", localtime())
            save_name: str = f"save__{time_path_part}"

        save_path: str = path.join(
            *[self.save_folder_path, save_name]
        )
        save_file: str = path.join(
            *[save_path, f"{save_name}.save"]
        )

        # Saving game progress:
        if path.exists(save_path) is False:
            makedirs(save_path)
        with open(save_file, 'w', encoding='utf-8') as file:
            file.write(
               self.get_game_progress_data_for_save(save_cell)
            )

        # Saving game scene image preview:
        x_screen_size: int = 720
        y_screen_size: int = int(
            self.settings_keeper.screen.get_height()
            * (x_screen_size / self.settings_keeper.screen.get_width())
        )
        screen_preview: Surface = transform.scale(
            surface=self.settings_keeper.screen,
            size=(x_screen_size, y_screen_size)
        )
        image.save(
            screen_preview,
            path.join(
                *[save_path, f"{self.button_image}.png"]
            )
        )

    def get_game_progress_data_for_save(self, save_cell: int) -> str:
        """
        Get progress data for save it like json in file.
        """
        data_to_save: dict[str] = {
            "scene": self.scene_validator.scene,
            "date": strftime("%Y-%m-%d_%H:%M:%S", localtime()),
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
        # Path`s names is parts of file names.
        save_files: list[str] = walk(self.save_folder_path).__next__()[1]
        if len(save_files) == 0:
            self.saves_dict: None = None
            return
        else:
            self.saves_dict: dict = {}
            for file in save_files:
                try:
                    with open(
                            path.join(
                                *[self.save_folder_path, file, f"{file}.save"]
                            ), 'r') as save_file:
                        # Generate save frame for save collection:
                        file_data: str = save_file.read()
                        save_data: dict = json.loads(file_data)
                        self.saves_dict.update({
                            strptime(save_data['date'], "%Y-%m-%d_%H:%M:%S"): {
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
