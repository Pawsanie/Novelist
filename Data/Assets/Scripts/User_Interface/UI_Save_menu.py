from .UI_Base_menu import BaseMenu
"""
Contains Save menu code.
"""


class SaveMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Save Menu.
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
        super(SaveMenu, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)

    def save_menu_input_mouse(self):
        """
        Interface interaction in in-game save menu.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status()
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'save_menu_save':
                ...
            if command == 'save_menu_back':
                self.interface_controller.save_menu_status = False
                self.interface_controller.game_menu_status = True

    def save_menu_input(self, event):
        """
        Save menu conveyor:
        :param event: pygame.event from main_loop.
        """
        self.save_menu_input_mouse()
        self.input_wait_ready()
