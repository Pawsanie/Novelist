import time
from os import path, walk, makedirs, sep, remove, rmdir
import json
from time import strftime, localtime, strptime, struct_time
from datetime import datetime, timedelta
import logging
from math import ceil

from pygame import image, transform, Surface

from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..User_Interface.Interface_Controller import InterfaceController
from .Settings_Keeper import SettingsKeeper
from .Scene_Validator import SceneValidator
from ..Logging_Config import text_for_logging
from ..User_Interface.UI_Buttons.UI_Save_Load_Cell_Button import SaveLoadCellButton
from ..Render.Render import Render
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
        self.render: Render = Render()

        # Path settings:
        script_root_path: str = path.abspath(__file__) \
            .replace(path.join(
                *['Assets', 'Scripts', 'Application_layer', 'Save_Keeper.py']
            ), '')
        self.save_folder_path: str = path.join(
            *[script_root_path, 'Saves']
        )
        self.save_and_load_ui_path: str = path.join(
            *[script_root_path, "Assets", "Images", "User_Interface", "Save_System"]
        )

        # Saves collection:
        self.saves_dict: dict = {}
        self.save_buttons_collection: dict = {}
        self.load_buttons_collection: dict = {}
        self.save_load_collections: dict[str, dict[str | SaveLoadCellButton | None]] = {
            "save": self.save_buttons_collection,
            "load": self.load_buttons_collection
        }

        # Save/Load buttons reference:
        self.save_buttons_reference: dict = self.deep_copy_alternative(
            self.interface_controller.buttons_dict['ui_save_menu_buttons']
        )
        self.load_buttons_reference: dict = self.deep_copy_alternative(
            self.interface_controller.buttons_dict['ui_load_menu_buttons']
        )

        # SaveKeeper settings:
        self.reread: bool = True
        self.button_image: str = "screen_preview"
        self.screen_preview_empty_image: str = "screen_preview_empty"
        self.autosave_name: str = "AutoSave"
        self.button_type: str = "save_and_load_cell"
        self.button_text_color: str = "#FFFFFF"
        self.button_text_font: str | None = None
        self.save_cells_count: int = 12
        self.empty_cell: str = "Empty Slot"
        self.empty_time: str = "0001-01-01_00:00:00"
        self.last_menu_page: int = 1
        self.save_file_format: str = 'save'
        self.preview_file_format: str = 'png'
        self.new_save_button_name: str = "New Save"

    @staticmethod
    def deep_copy_alternative(interesting_data: dict) -> dict:
        """
        Alternative for dict deepcopy, because it cant works with pygame.
        :param interesting_data: Dict with menus data.
        :type interesting_data: dict
        """
        result: dict = {}
        for key, value in interesting_data.items():
            result.update(
                {key: value}
            )
        return result

    def update_ui_buttons(self, *, menu_data: dict, save_type: str):
        """
        Update menu`s buttons dict in 'InterfaceController.buttons_dict'.
        :param menu_data: InterfaceController menu`s data.
        :type menu_data: dict
        :param save_type: Save | Load
        :type save_type: str
        """
        if menu_data["menu_object"].status is True:
            menu_data["menu_buttons"].clear()
            menu_data["menu_buttons"].update(
                menu_data["menu`s_buttons_reference"]
            )

            save_cell_buttons: dict = self.save_load_collections[save_type]
            for key, value in save_cell_buttons.items():
                if value['save_page'] == menu_data["menu_object"].menu_page:
                    menu_data["menu_buttons"].setdefault(key, value['button'])

    def save_cells_sort(self):
        """
        Sorted game saves for get them screen position.
        """
        if len(self.saves_dict) != 0:
            self.saves_dict = dict(
                sorted(
                    self.saves_dict.items(),
                    key=lambda key_name: key_name[0],
                    reverse=True
                )
            )

            # Base variables:
            row_number: int = 1
            column_number: int = 1
            row_counter: int = 1
            save_cell_page: int = 1

            for key, value in self.saves_dict.items():
                # Autosave position:
                if value['save_data']['save_name'] in (self.autosave_name, self.new_save_button_name):
                    value['save_data']['save_cell']: list[int, int] = [1, 1]

                else:  # Another save position:
                    # Counters:
                    column_number += 1
                    if column_number == 5:
                        column_number: int = 1
                        row_counter += 1
                        row_number += 1
                    if row_number == 4:
                        row_number: int = 1
                    if row_counter == 4:
                        row_counter: int = 1
                        save_cell_page += 1

                    # Add save position data:
                    value['save_data']['save_cell']: list[int, int] = [
                        row_number,
                        column_number
                    ]
                value['save_data']['save_page']: int = save_cell_page

    def enrichment_of_game_saves(self):
        """
        Enrichment game save`s collection with empty cells.
        """
        if len(self.saves_dict) != 0:
            divider: int = len(self.saves_dict)
            if len(self.saves_dict) % self.save_cells_count == 0:
                return
        else:
            divider: int = 12

        close_value: int = (
                ceil(divider / self.save_cells_count)
                * self.save_cells_count
        )
        enrichment_count: int = close_value - len(self.saves_dict)

        time_stamp: datetime = datetime.strptime(self.empty_time, "%Y-%m-%d_%H:%M:%S")
        for number in range(enrichment_count):
            time_stamp: datetime = time_stamp + timedelta(seconds=1)
            key_name: struct_time = datetime.timetuple(time_stamp)
            time_mark_str: str = strftime("%Y-%m-%d_%H:%M:%S", key_name)

            self.saves_dict.update(
                {
                    key_name: {
                        "file_name": time_mark_str,
                        "save_data": {
                            'date': time_mark_str,
                            "save_name": self.empty_cell,
                            'select_name': time_mark_str
                        }
                    }
                }
            )

    def generate_cell_buttons(self):
        """
        Generate cell buttons for Save/Load UI.
        """
        if self.reread is True:
            self.saves_read()
        else:
            if len(self.saves_dict) != 0:
                return

        # Save slots initialization:
        self.enrichment_of_game_saves()
        self.generate_new_save_slot()
        self.save_cells_sort()

        # Generate menu`s buttons:
        for save in self.saves_dict:
            save_data: dict = self.saves_dict[save]
            text_offset_y: float = 3.2

            # Cells with save data:
            button_image_path: str = path.join(
                *[self.save_folder_path, save_data['file_name'], self.button_image]
            )
            save_name: str = save_data["save_data"]['save_name']

            if save_name == self.autosave_name:
                save_text = self.autosave_name
            elif save_name in (self.empty_cell, self.new_save_button_name):
                save_text: str = save_name
                button_image_path: str = f"{self.save_and_load_ui_path}{sep}{self.screen_preview_empty_image}"
                text_offset_y: None = None
                if save_name == self.empty_cell:
                    save_name: str = save_data['save_data']['date']
            else:
                save_text: str = save_data['save_data']['date']

            save_cell_button: SaveLoadCellButton = SaveLoadCellButton(
                        button_name=save_data['save_data']['date'],
                        button_text=save_text,
                        button_image_data={
                            'sprite_name': button_image_path,
                            'index_number': save_data['save_data']['save_cell'],
                            'type': self.button_type,
                            'color': self.button_text_color,
                            'font': self.button_text_font
                        },
                        have_real_path=True,
                        text_offset_y=text_offset_y
                    )

            for key, collection in self.save_load_collections.items():
                collection.setdefault(
                    save_name,
                    {
                        'button': save_cell_button,
                        'save_page': save_data['save_data']['save_page']
                    }
                )

        self.get_last_save_load_menus_page()

        # Specific menus preprocessing:
        # Drop AutoSave from Save Menu buttons:
        try:
            self.save_buttons_collection.pop(self.autosave_name)
        except KeyError:
            pass

        # Drop NewSave from Load Menu buttons:
        try:
            self.load_buttons_collection.pop(self.new_save_button_name)
        except KeyError:
            pass

        # Full empty load meny:
        # TODO: crutch?
        no_autosave_status: bool = True
        for name in self.saves_dict.values():
            if self.autosave_name in name['save_data']['save_name']:
                no_autosave_status: bool = False
                break
        if no_autosave_status is True:
            self.no_autosave_load_menu()

    def no_autosave_load_menu(self):  # TODO: crutch?
        """
        Add additional empty save cell to load meny if AutoSave do not exist.
        """
        save_cell_button: SaveLoadCellButton = SaveLoadCellButton(
            button_name=self.empty_time,
            button_text=self.empty_cell,
            button_image_data={
                'sprite_name': f"{self.save_and_load_ui_path}{sep}{self.screen_preview_empty_image}",
                'index_number': [1, 1],
                'type': self.button_type,
                'color': self.button_text_color,
                'font': self.button_text_font
            },
            have_real_path=True,
            text_offset_y=3.2
        )

        self.load_buttons_collection.setdefault(
            self.empty_time,
            {
                'button': save_cell_button,
                'save_page': 1
            }
        )

    def generate_new_save_slot(self):
        """
        Generate first button for Save menu.
        """
        key_name: struct_time = time.localtime()
        time_mark_str: str = strftime("%Y-%m-%d_%H:%M:%S", key_name)
        self.saves_dict.update(
            {
                key_name: {
                    "file_name": self.new_save_button_name,
                    "save_data": {
                        'date': time_mark_str,
                        "save_name": self.new_save_button_name,
                        'select_name': self.new_save_button_name
                    }
                }
            }
        )

    def get_last_save_load_menus_page(self):
        """
        Generate max save menu pages.
        """
        saves_count: int = len(self.save_buttons_collection) - 1

        close_value: int = (
                ceil(saves_count / self.save_cells_count)
                * self.save_cells_count
        )

        self.last_menu_page: int = close_value // self.save_cells_count

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

    def save(self, *, auto_save: bool = True):
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
            *[save_path, f"{save_name}.{self.save_file_format}"]
        )

        # Saving game progress:
        if path.exists(save_path) is False:
            makedirs(save_path)
        with open(save_file, 'w', encoding='utf-8') as file:
            file.write(
               self.get_game_progress_data_for_save()
            )

        # Saving game scene image preview:
        x_screen_size: int = 720
        y_screen_size: int = int(
            self.settings_keeper.screen.get_height()
            * (x_screen_size / self.settings_keeper.screen.get_width())
        )
        screen_preview: Surface = transform.scale(
            surface=self.render.save_screen,
            size=(x_screen_size, y_screen_size)
        )
        image.save(
            screen_preview,
            path.join(
                *[save_path, f"{self.button_image}.{self.preview_file_format}"]
            )
        )

    def get_game_progress_data_for_save(self) -> str:
        """
        Get progress data for save it like json in file.
        """
        data_to_save: dict[str] = {
            "scene": self.scene_validator.scene_flag,
            "date": strftime("%Y-%m-%d_%H:%M:%S", localtime())
        }
        return json.dumps(data_to_save, indent=4)

    def continue_game(self) -> str or False:
        """
        Get scene name for game continue.
        Used in StartMenu class from "UI_Start_menu.py".

        :return: String with scene name from last save.
                 Or False if save file was corrupted.
        """
        self.saves_read()
        if len(self.saves_dict) == 0:
            return self.scene_validator.default_scene_name
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

    def vanish_game_collections(self):
        """
        Vanish save collections for save reading.
        """
        self.saves_dict.clear()
        self.save_buttons_collection.clear()
        self.load_buttons_collection.clear()

    def saves_read(self):
        """
        Read save directory.
        """
        # Save path dos not exist:
        if path.exists(self.save_folder_path) is False:
            return
        # Check save path:
        # Path`s names is parts of file names.
        save_files: list[str] = walk(self.save_folder_path).__next__()[1]
        if len(save_files) == 0:
            return
        else:
            self.vanish_game_collections()
            for file in save_files:
                try:
                    with open(
                            path.join(
                                *[self.save_folder_path, file, f"{file}.{self.save_file_format}"]
                            ), 'r') as save_file:
                        # Generate save frame for save collection:
                        file_data: str = save_file.read()
                        save_data: dict = json.loads(file_data)
                        save_data.update(
                            {
                                'save_name': file,
                                'select_name': file
                            }
                        )
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

    def get_save_slot_data(self, slot_name: str):
        """
        Get save slot data.
        :param slot_name: Save Slot` button name. (save name)
        :type slot_name: str
        """
        for save in self.saves_dict.values():
            if save['file_name'] == slot_name:
                return save['save_data']

    def delete_save(self, file_name: str | None):
        """
        Delete save files and save cell folder.
        """
        if file_name is not None:
            save_path: str = path.join(
                *[self.save_folder_path, file_name]
            )

            for file in [
                f"{file_name}.{self.save_file_format}",
                f"{self.button_image}.{self.preview_file_format}"
            ]:
                try:
                    remove(
                        path.join(
                            *[save_path, file]
                        )
                    )
                except OSError:
                    pass

            try:
                rmdir(save_path)
            except OSError:
                raise OSError(
                    f"Not only game save data are inside folder:\nDelete root path: {save_path}"
                )
