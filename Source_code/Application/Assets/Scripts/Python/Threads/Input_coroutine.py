from ..Fundamentals.Patterns import SingletonPattern
from ..Input.Reactions_to_input_commands import InputCommandsReactions
"""
Contains code for reactions to input commands.
"""


class InputThread(SingletonPattern):
    """
    Interpret user commands into program reactions.
    """
    def __init__(self):
        self._reactions_to_input_commands: InputCommandsReactions = InputCommandsReactions()

    async def coroutine(self):
        """
        MVC pattern Control part.
        """
