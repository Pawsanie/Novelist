from pygame import KEYDOWN, K_ESCAPE, K_TAB, K_e

from .UI_Base_menu import BaseMenu
"""
Back to start menu status menu code.
"""


class BackToStartMenuStatusMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in "Back to 'Start menu' status menu".
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
        super(BackToStartMenuStatusMenu, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)

    def back_to_start_menu_status_menu_yes(self):
        """
        Switch to start menu.
        """
        self.interface_controller.back_to_start_menu_status = False
        self.interface_controller.start_menu_status = True

    def back_to_start_menu_status_menu_no(self):
        """
        Back from back to start menu status menu.
        """
        self.interface_controller.back_to_start_menu_status = False
        self.interface_controller.game_menu_status = True

    def back_to_start_menu_status_menu_input_mouse(self):
        """
        Interface interaction in in-game back to start menu status menu.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status()
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'back_to_start_menu_yes':
                self.back_to_start_menu_status_menu_yes()
            if command == 'back_to_start_menu_no':
                self.back_to_start_menu_status_menu_no()

    def key_bord_back_to_start_menu_status_menu_key_down(self, event):
        """
        Interface interaction in in-game back to start menu status menu.
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_TAB:
                self.back_to_start_menu_status_menu_no()
            if event.key == K_e:
                self.back_to_start_menu_status_menu_yes()

    def back_to_start_menu_status_menu_input(self, event):
        """
        Back to start menu status menu input conveyor:
        :param event: pygame.event from main_loop.
        """
        # Button game menu ui status:
        self.back_to_start_menu_status_menu_input_mouse()
        # Button game menu key bord status:
        self.key_bord_back_to_start_menu_status_menu_key_down(event)
        self.input_wait_ready()
