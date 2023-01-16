from ..Settings_Keeper import SettingsKeeper
from .UI_Base_menu import BaseMenu
"""
Contains settings menu code.
"""


class SettingsMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Settings Menu.
    """
    def __init__(self, *, interface_controller, settings_keeper, scene_validator):
        """
        :param interface_controller: InterfaceController exemplar.
                                     Responsible for user interface status and buttons.
        :type interface_controller: InterfaceController
        :param scene_validator: SceneValidator exemplar.
                            Responsible for scene order and scene construction.
        :type scene_validator: SceneValidator
        :param settings_keeper: Settings controller class.
        :type settings_keeper: SettingsKeeper
        """
        super(SettingsMenu, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)
        self.settings_keeper: SettingsKeeper = settings_keeper

    def settings_menu_ui_mouse(self, event):
        """
        Interface interaction in in-game setting menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'settings_menu_video':
                ...
            if command == 'settings_menu_audio':
                ...
            if command == 'settings_menu_localization':
                ...
            if command == 'settings_menu_back':
                self.interface_controller.settings_menu_status = False
                if self.interface_controller.settings_from_start_menu_flag is True:
                    self.interface_controller.start_menu_status = True
                if self.interface_controller.settings_from_game_menu_flag is True:
                    self.interface_controller.game_menu_status = True

    def setting_menu_input(self, event):
        """
        Setting menu conveyor:
        :param event: pygame.event from main_loop.
        """
        self.settings_menu_ui_mouse(event)
        self.input_wait_ready()