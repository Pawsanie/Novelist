from ..Wrapper import screen_flip
from ....Fundamentals.Patterns import SingletonPattern
"""
Contains code responsible for Render backend API bridge.
"""


class GraphicsEngineBridge(SingletonPattern):
    """
    Render backend API bridge.
    """
    @staticmethod
    def flip():
        """
        Render new image on window screen.
        """
        screen_flip()
