from .Settings_Keeper import SettingsKeeper
from .Save_Keeper import SaveKeeper
from ..GamePlay.Scene_Validator import SceneValidator
from ..Render.Texture_Master import TexturesMaster
"""
Initialization part of main application layer objects.
"""


def initialization():
    """
    Prepare application to work.
    Call from GameMaster.
    """
    # Collect base game settings:
    SettingsKeeper()
    # Save and load system:
    SaveKeeper()
    # Scene Validator settings:
    SceneValidator()
    # Texture processing system:
    TexturesMaster()
