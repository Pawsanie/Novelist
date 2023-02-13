from .UI_Base_menu import BaseMenu

from ..Save_Keeper import SaveKeeper
"""
Contains Start menu code.
"""


class StartMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Start Menu.
    """
    def __init__(self, *, interface_controller, scene_validator):
        """
        :param interface_controller: InterfaceController exemplar.
                                     Responsible for user interface status and buttons.
        :type interface_controller: InterfaceController
        :param scene_validator: SceneValidator exemplar.
                            Responsible for scene order and scene construction.
        :type scene_validator: SceneValidator
        """
        super(StartMenu, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)
        self.save_keeper: SaveKeeper = SaveKeeper(
            scene_validator=scene_validator
        )

    def start_game(self, scene_name: str):
        self.scene_validator.scene = scene_name
        self.scene_validator.scene_flag = scene_name
        self.interface_controller.start_menu_status = False
        self.interface_controller.gameplay_interface_hidden_status = False
        self.interface_controller.gameplay_interface_status = True

    def start_menu_input_mouse(self, event):
        """
        Interface interaction in in-game start menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'start_menu_new_game':
                self.start_game('scene_01')  # 'scene_01' as default!
            if command == 'start_menu_continue':
                self.start_game(
                    self.save_keeper.continue_game()
                )
            if command == 'start_menu_load':
                self.interface_controller.start_menu_status = False
                self.interface_controller.load_menu_status = True
            if command == 'start_menu_settings':
                self.interface_controller.start_menu_status = False
                self.interface_controller.settings_menu_status = True
            if command == 'start_menu_creators':
                ...
            if command == 'start_menu_exit':
                self.interface_controller.start_menu_status = False
                self.interface_controller.exit_menu_status = True

    def start_menu_input(self, event):
        """
        Start menu conveyor:
        :param event: pygame.event from main_loop.
        """
        # Exit menu "from called" status flag:
        self.interface_controller.exit_from_start_menu_flag = True
        self.interface_controller.exit_from_game_menu_flag = False
        # Load menu "from called" status flag:
        self.interface_controller.load_from_start_menu_flag = True
        self.interface_controller.load_from_game_menu_flag = False
        # Setting menu "from called" status flag:
        self.interface_controller.settings_from_start_menu_flag = True
        self.interface_controller.settings_from_game_menu_flag = False
        # Input:
        self.start_menu_input_mouse(event)
        self.input_wait_ready()
