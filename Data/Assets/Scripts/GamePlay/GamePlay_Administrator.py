from ..Application_layer.Stage_Director import StageDirector
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
    gameplay_collections: dict = {
        'reading': GamePlayReading(),
        'choice': GamePlayDialoguesChoice()
    }

    def __init__(self):
        # Arguments processing:
        super(GamePlayAdministrator, self).__init__()
        self.stage_director: StageDirector = StageDirector()

    def gameplay_input(self, event):
        """
        Gameplay interaction.
        :param event: pygame.event from main_loop.
        """
        for gameplay_type, gameplay_class in self.gameplay_collections.items():
            if self.scene_validator.scene_gameplay_type == gameplay_type:
                gameplay_class.gameplay_input(event)
                return
