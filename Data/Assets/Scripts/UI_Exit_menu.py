from pygame import quit, KEYDOWN, K_ESCAPE, K_TAB, K_e

from .UI_Base_menu import BaseMenu
"""
Contains exit menu code.
"""


class ExitMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Exit Menu.

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
        super(ExitMenu, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)

    def exit_menu_back(self):
        """
        Back from exit menu.
        """
        self.interface_controller.exit_menu_status = False
        if self.interface_controller.exit_from_start_menu_flag is True:
            self.interface_controller.start_menu_status = True
        if self.interface_controller.exit_from_game_menu_flag is True:
            self.interface_controller.game_menu_status = True

    def exit_menu_input_mouse(self):
        """
        Interface interaction in in-game exit menu.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status()
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'exit_menu_yes':
                quit()
                exit(0)
            if command == 'exit_menu_no':
                self.exit_menu_back()

    def key_bord_exit_menu_key_down(self, event):
        """
        Interface interaction in in-game exit menu.
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_TAB:
                self.exit_menu_back()
            if event.key == K_e:
                quit()
                exit(0)

    def exit_menu_input(self, event):
        """
        Exit menu input conveyor:
        :param event: pygame.event from main_loop.
        """
        # Button game menu ui status:
        self.exit_menu_input_mouse()
        # Button game menu key bord status:
        self.key_bord_exit_menu_key_down(event)
        self.input_wait_ready()
