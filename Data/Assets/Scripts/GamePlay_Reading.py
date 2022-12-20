from pygame import KEYDOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, mouse

from .Stage_Director import StageDirector
from .Scene_Validator import SceneValidator
from .Interface_Controller import InterfaceController
from .User_Interface.UI_Base_menu import BaseMenu
"""
Contains gameplay code.
"""


class GamePlayReading(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in reading gameplay.

    :param stage_director: Stage Director class exemplar.
                           Responsible for stage production.
    :type stage_director: StageDirector
    :param interface_controller: InterfaceController exemplar.
                                 Responsible for user interface status and buttons.
    :type interface_controller: InterfaceController
    :param scene_validator: SceneValidator exemplar.
                            Responsible for scene order and scene construction.
    :type scene_validator: SceneValidator
    """
    def __init__(self, *, stage_director: StageDirector, interface_controller: InterfaceController,
                 scene_validator: SceneValidator):
        """
        :param stage_director: Stage Director class exemplar.
                               Responsible for stage production.
        :type stage_director: StageDirector
        :param interface_controller: InterfaceController exemplar.
                                     Responsible for user interface status and buttons.
        :type interface_controller: InterfaceController
        :param scene_validator: SceneValidator exemplar.
                                Responsible for scene order and scene construction.
        :type scene_validator: SceneValidator
        """
        super(GamePlayReading, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)
        # Stage Director settings:
        self.director: StageDirector = stage_director

    def button_gameplay_ui_status(self):
        """
        Processing the gameplay interface.
        """
        button_clicked: tuple[bool, bool, bool] = mouse.get_pressed()

        # If user interface is not hidden:
        if self.interface_controller.gameplay_interface_hidden_status is False:
            gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status()
            # Clicking a virtual button with a mouse:
            if gameplay_ui_buttons[1] is True:
                command = gameplay_ui_buttons[0]
                if command == 'past_scene':
                    if self.scene_validator.past_scene != 'START':
                        self.scene_validator.scene_flag = self.scene_validator.past_scene
                    else:
                        ...
                if command == 'hide_interface':
                    self.interface_controller.gameplay_interface_hidden_status = True
                if command == 'game_menu':
                    self.interface_controller.game_menu_status = True
                    self.interface_controller.gameplay_interface_status = False
                if command == 'next_scene':
                    if self.scene_validator.next_scene != 'FINISH':
                        self.scene_validator.scene_flag = self.scene_validator.next_scene
                    else:
                        ...
                if command == 'fast_forward':
                    if button_clicked[0] is not False:
                        if self.scene_validator.next_scene != 'FINISH':
                            self.scene_validator.scene_flag = self.scene_validator.next_scene
            # Next scene without virtual buttons:
            else:
                if button_clicked[0] is True:
                    if self.scene_validator.next_scene != 'FINISH':
                        self.scene_validator.scene_flag = self.scene_validator.next_scene

        # If user interface is hidden:
        else:
            if button_clicked[0] is True:
                self.interface_controller.gameplay_interface_hidden_status = False

    def key_bord_gameplay_key_down(self, event):
        """
        Checking pressed keys.
        Runs the functions associated with the desired keys.
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if self.interface_controller.gameplay_interface_hidden_status is False:
                if event.key == K_LEFT:
                    if self.scene_validator.past_scene != 'START':
                        self.scene_validator.scene_flag = self.scene_validator.past_scene
                if event.key == K_RIGHT:
                    if self.scene_validator.next_scene != 'FINISH':
                        self.scene_validator.scene_flag = self.scene_validator.next_scene
                if event.key == K_SPACE:
                    if self.scene_validator.next_scene != 'FINISH':
                        self.scene_validator.scene_flag = self.scene_validator.next_scene
            if self.interface_controller.game_menu_status is False:
                if event.key == K_ESCAPE:
                    self.interface_controller.game_menu_status = True
                    self.interface_controller.gameplay_interface_status = False

    def gameplay_input(self, event):
        """
        Gameplay input conveyor:
        :param event: pygame.event from main_loop.
        """
        # Button gameplay ui status:
        self.button_gameplay_ui_status()
        # Button gameplay key bord status:
        self.key_bord_gameplay_key_down(event)
        self.input_wait_ready()
