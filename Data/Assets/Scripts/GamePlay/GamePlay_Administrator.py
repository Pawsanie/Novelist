from ..Stage_Director import StageDirector
from ..Scene_Validator import SceneValidator
from ..User_Interface.Interface_Controller import InterfaceController
from .GamePlay_Reading import GamePlayReading
from ..User_Interface.UI_Base_menu import BaseMenu
"""
Contains gameplay code.
"""


class GamePlayAdministrator(BaseMenu):
    """
    Responsible for gameplay type at the moment.
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
        super(GamePlayAdministrator, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)
        # Stage Director settings:
        self.stage_director: StageDirector = stage_director

        # Settings for gameplay:
        self.gameplay_reading: GamePlayReading = GamePlayReading(
            stage_director=self.stage_director,
            interface_controller=self.interface_controller,
            scene_validator=self.scene_validator
        )

    def gameplay_input(self, event):
        if self.scene_validator.scene_gameplay_type == 'reading':
            self.gameplay_reading.gameplay_input(event)
        if self.scene_validator.scene_gameplay_type == 'choice':
            ...
        if self.scene_validator.scene_gameplay_type is False:
            ...
