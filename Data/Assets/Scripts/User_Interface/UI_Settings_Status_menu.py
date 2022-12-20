from .UI_Base_menu import BaseMenu
"""
Contains Settings Status menu code.
"""


class SettingsStatusMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Settings Status Menu.

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
        super(SettingsStatusMenu, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)

    def setting_menu_input_mouse(self):
        """
        Interface interaction in in-game settings menu.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status()
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'save_menu_save':
                ...

    def settings_status_menu_input(self, event):
        """
        Settings status menu conveyor:
        :param event: pygame.event from main_loop.
        """
        self.setting_menu_input_mouse()
        self.input_wait_ready()
