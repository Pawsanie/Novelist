from pygame.event import Event

from ..User_Interface.UI_Button_Factory import button_generator
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..User_Interface.UI_Menu_Text import menus_text_generator, MenuText
from ..User_Interface.UI_Buttons.UI_Base_Button import BaseButton
# Lazy import:
# from ..Render.Batch import Batch
"""
Contents code for user interface controller.
"""


class InterfaceController(SingletonPattern):
    """
    Generate user interface: buttons, menu and control it.
    InterfaceController used in "GamePlay_Administrator.py" for gameplay programming.
    Created in GameMaster class in Game_Master.py.
    """
    def __init__(self):
        # Generate buttons:
        self.buttons_dict: dict = button_generator()
        self.gameplay_choice_buttons: dict = {}
        # Generate menus text:
        self.menus_text_dict: dict = menus_text_generator()

        # In game user interface:
        self.gameplay_interface_hidden_status: bool = False
        self.gameplay_interface_status: bool = False
        # GamePlay type:
        self.gameplay_type_reading: bool = False
        self.gameplay_type_choice: bool = False

        # Tag for menu background render:
        self.menu_name: str | None = 'start_menu'
        # Menu interface:
        self.menus_collection: dict | None = None
        self.game_menu_status: bool = False
        # In game or start menu flag:
        self.start_menu_flag: bool = True

    def get_ui_buttons_dict(self) -> dict[str, BaseButton]:
        """
        Generate user interface buttons.
        :return: Dict with buttons names strings as values.
        """
        # In game user interface:
        if self.gameplay_interface_status is True:
            self.menu_name: None = None
            if self.gameplay_type_reading is True:
                return self.buttons_dict['ui_gameplay_buttons']
            if self.gameplay_type_choice is True:
                return self.gameplay_choice_buttons
            
        # Menu interface:
        for menu_key in self.menus_collection:
            menu: dict = self.menus_collection[menu_key]
            if menu['object'].status is True:
                self.menu_name: str | None = menu_key
                return self.buttons_dict[
                    menu['menu_file']
                ]

    def get_menus_text_dict(self) -> dict[str, MenuText]:
        """
        Generate text for same menu.
        """
        for menu_key in self.menus_collection:
            menu: dict = self.menus_collection[menu_key]
            if menu['object'].status is True:
                if menu['text_file'] is not None:
                    return self.menus_text_dict[
                        menu['text_file']
                    ]

    def scale(self):
        """
        Scale interface buttons.
        """
        # UI Buttons scale:
        ui_buttons_dict: dict[str, BaseButton] = self.get_ui_buttons_dict()
        if ui_buttons_dict is not None:
            for key in ui_buttons_dict:
                button: BaseButton = ui_buttons_dict[key]
                button.scale()

        # UI Text scale:
        text_dict: dict[str, MenuText] = self.get_menus_text_dict()
        if text_dict is not None:
            for key in text_dict:
                text: MenuText = text_dict[key]
                text.scale()

    def button_clicked_status(self, event: Event) -> tuple[str | None, bool]:
        """
        Check left click of mouse to button status.
        :param event: pygame.event from main_loop.
        """
        if self.gameplay_interface_hidden_status is False:
            gameplay_ui_dict: dict = self.get_ui_buttons_dict()
            for button in gameplay_ui_dict:
                click_status: bool = gameplay_ui_dict[button].button_clicked_status(event)
                if click_status is True:
                    return button, True
        return None, False

    def button_push_status(self) -> tuple[str | None, bool]:
        """
        Check left click of mouse to button status.
        """
        if self.gameplay_interface_hidden_status is False:
            gameplay_ui_dict: dict[str, BaseButton] = self.get_ui_buttons_dict()
            for button in gameplay_ui_dict:
                click_status: bool = gameplay_ui_dict[button].button_click_hold()
                if click_status is True:
                    return button, True
        return None, False

    def button_cursor_position_status(self) -> bool:
        """
        Checking the cursor position above the button.
        """
        gameplay_ui_dict: dict = self.get_ui_buttons_dict()
        for button in gameplay_ui_dict:
            cursor_position_status: bool = gameplay_ui_dict[button].button_cursor_position_status()
            if cursor_position_status is True:
                return True
            else:
                return False

    def generate_menus_batch(self):
        """
        Generate UI_batch for display image render.
        :return: Batch
        """
        from ..Render.Batch import Batch
        result: Batch = Batch()

        # Generate buttons:
        menus_dict: dict[str, BaseButton] = self.get_ui_buttons_dict()
        if menus_dict is not None:
            for button_name in menus_dict:
                button: BaseButton = menus_dict[button_name]
                result.append(
                    button.get_sprite()
                )

        # Generate text:
        text_dict: dict[str, MenuText] = self.get_menus_text_dict()
        if text_dict is not None:
            for text_name in text_dict:
                result.append(
                    text_dict[text_name].get_sprite()
                )

        return result
