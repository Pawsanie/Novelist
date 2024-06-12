from inspect import iscoroutinefunction

from pygame.event import Event

from .GamePlay_Reading import GamePlayReading
from ..User_Interface.UI_Base_menu import BaseMenu
from .GamePlay_dialogues_choice import GamePlayDialoguesChoice
from ..Universal_computing.Pattern_Singleton import SingletonPattern
"""
Contains gameplay code.
"""


class GamePlayAdministrator(BaseMenu, SingletonPattern):
    """
    Responsible for gameplay type at the moment.
    """
    def __init__(self):
        super(GamePlayAdministrator, self).__init__()
        self._gameplay_collections: dict = {
            'reading': {
                "gameplay": GamePlayReading(),
                "interface": "gameplay_type_reading"
            },
            'choice': {
                "gameplay": GamePlayDialoguesChoice(),
                "interface": "gameplay_type_choice"
            }
        }

    def _devnull(self):
        """
        Return interface to base state.
        """
        for gameplay_type, gameplay_class in self._gameplay_collections.items():
            setattr(
                self.interface_controller,
                gameplay_class["interface"],
                False
            )

    def set_gameplay_type(self):
        """
        Set GamePlay type.
        Call from GameMaster _render_loop method.
        """
        self._devnull()
        for gameplay_type, gameplay_class in self._gameplay_collections.items():
            if self.scene_validator.scene_gameplay_type == gameplay_type:
                setattr(
                    self.interface_controller,
                    gameplay_class["interface"],
                    True
                )
                try:
                    gameplay_class["gameplay"].set_choice()
                except AttributeError:
                    pass

    async def gameplay_input(self, event: Event):
        """
        Gameplay interaction.
        Call from InputCommandsReactions.
        :param event: pygame.event from InputCommandsReactions input_commands_loop method.
        """
        for gameplay_type, gameplay_class in self._gameplay_collections.items():
            if self.scene_validator.scene_gameplay_type == gameplay_type:
                gameplay_method = gameplay_class["gameplay"].gameplay_input
                if iscoroutinefunction(gameplay_method):
                    await gameplay_method(event)
                else:
                    gameplay_method(event)
                return
