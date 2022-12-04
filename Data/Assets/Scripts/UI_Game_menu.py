from pygame import KEYDOWN, K_ESCAPE

from .UI_Base_menu import BaseMenu
"""
Contains game menu code.
"""


class GameMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Game Menu.

    :param interface_controller: InterfaceController exemplar.
                                 Responsible for user interface status and buttons.
    :type interface_controller: InterfaceController
    :param scene_validator: SceneValidator exemplar.
                        Responsible for scene order and scene construction.
    :type scene_validator: SceneValidator
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
        super(GameMenu, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)

    def game_menu_ui_status(self):
        """
        Interface interaction in in-game menu.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status()
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'game_menu_continue':
                self.interface_controller.game_menu_status = False
                self.interface_controller.gameplay_interface_status = True
            if command == 'game_menu_save':
                self.interface_controller.game_menu_status = False
                self.interface_controller.save_menu_status = True
            if command == 'game_menu_load':
                self.interface_controller.game_menu_status = False
                self.interface_controller.load_menu_status = True
            if command == 'game_menu_settings':
                self.interface_controller.game_menu_status = False
                self.interface_controller.settings_menu_status = True
            if command == 'game_menu_exit':
                self.interface_controller.game_menu_status = False
                self.interface_controller.exit_menu_status = True

    def key_bord_game_menu_key_down(self, event):
        """
        Interface interaction in in-game menu.
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.interface_controller.game_menu_status = False
                self.interface_controller.gameplay_interface_status = True

    def game_menu_input(self, event):
        """
        Game menu input conveyor:
        :param event: pygame.event from main_loop.
        """
        # Exit menu "from called" status flag:
        self.interface_controller.exit_from_start_menu_flag = False
        self.interface_controller.exit_from_game_menu_flag = True
        # Button game menu ui status:
        self.game_menu_ui_status()
        # Button game menu key bord status:
        self.key_bord_game_menu_key_down(event)
        self.input_wait_ready()
