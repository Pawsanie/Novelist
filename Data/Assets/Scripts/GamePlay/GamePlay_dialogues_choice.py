from pygame import KEYDOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, mouse

from ..Stage_Director import StageDirector
from ..Scene_Validator import SceneValidator
from ..User_Interface.Interface_Controller import InterfaceController
from ..User_Interface.UI_Base_menu import BaseMenu
"""
Contains gameplay reading code.
"""


class GamePlayDialoguesChoice(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in reading gameplay.
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
        # Arguments processing:
        super(GamePlayDialoguesChoice, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)
        # Stage Director settings:
        self.stage_director = stage_director

    def button_gameplay_ui_status(self):
        """
        Processing the gameplay interface.
        """
        button_clicked: tuple[bool, bool, bool] = mouse.get_pressed()
        choice_data: dict[str, dict[str]] = self.scene_validator.choices_data[self.scene_validator.scene]

        # If user interface is not hidden:
        if self.interface_controller.gameplay_interface_hidden_status is False:
            gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status()
            # Clicking a virtual button with a mouse:
            if gameplay_ui_buttons[1] is True:
                command = gameplay_ui_buttons[0]
                if command == '  ':
                    ...

    def key_bord_gameplay_key_down(self, event):
        ...

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
