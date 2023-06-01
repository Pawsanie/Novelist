from ..Stage_Director import StageDirector
from .GamePlay_Reading import GamePlayReading
from ..User_Interface.UI_Base_menu import BaseMenu
from .GamePlay_dialogues_choice import GamePlayDialoguesChoice
"""
Contains gameplay code.
"""


class GamePlayAdministrator(BaseMenu):
    """
    Responsible for gameplay type at the moment.
    """
    def __init__(self):
        # Arguments processing:
        super(GamePlayAdministrator, self).__init__()
        self.stage_director: StageDirector = StageDirector()

        # Settings for gameplay:
        self.gameplay_reading: GamePlayReading = GamePlayReading()
        self.gameplay_dialogues_choice: GamePlayDialoguesChoice = GamePlayDialoguesChoice()

    def gameplay_input(self, event):
        """
        Gameplay interaction.
        :param event: pygame.event from main_loop.
        """
        # Gameplay reading:
        if self.scene_validator.scene_gameplay_type == 'reading':
            self.gameplay_reading.gameplay_input(event)
            return
        # Gameplay choice:
        if self.scene_validator.scene_gameplay_type == 'choice':
            self.gameplay_dialogues_choice.gameplay_input(event)
            return
        # Have no gameplay:
        if self.scene_validator.scene_gameplay_type is False:
            pass
