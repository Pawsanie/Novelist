from ..Application_layer.Stage_Director import StageDirector
from ..Universal_computing.Assets_load import AssetLoader
from ..Universal_computing.Pattern_Singleton import SingletonPattern
"""
Contains SceneValidator code.
"""


class SceneValidator(SingletonPattern):
    """
    Controls in what order the scenes go and their settings.
    """
    def __init__(self):
        # Program layers settings:
        self._asset_loader: AssetLoader = AssetLoader()
        self._stage_director: StageDirector = StageDirector()

        # Screenplay loading:
        self._screenplay: dict = self._asset_loader.json_load(
            path_list=[
                'Scripts', 'Json_data', 'screenplay'
            ]
        )

        # Scene FLAGS:
        self._default_start_scene: str = 'START'
        self._current_scene_name: str | None = None
        self._possible_next_scene_checker_flag: str | None = None
        self._scene_update_status: bool = True

        # Over settings:
        self._scene_data: dict | None = None

    def get_screenplay_data(self) -> dict:
        """
        Used in StageDirector (generate_dialogues).
        """
        return self._screenplay

    def get_default_scene_name(self):
        """
        Get default scene for New Game.
        Use in SaveKeeper or StartMenu.
        """
        for scene_name, scene_data in self._screenplay.items():
            if scene_data["past_scene"] == self._default_start_scene:
                return scene_name

    def devnull(self):
        """
        Return to base settings.
        """
        self._current_scene_name: str = self.get_default_scene_name()
        self._possible_next_scene_checker_flag: str | None = None
        self._scene_update_status: bool = True

    def get_gameplay_type(self) -> str | None:
        """
        Used in GamePlayAdministrator.
        """
        try:
            return self._scene_data['gameplay_type']
        except TypeError:
            return None

    def switch_scene(self, new_scene_name: str):
        """
        Used in GamePlayDialoguesChoice, GamePlayReading, LoadMenu, StartMenu.
        """
        self._possible_next_scene_checker_flag: str = new_scene_name

    def get_current_scene_data(self) -> dict:
        """
        Used in GamePlayDialoguesChoice, GamePlayReading, StageDirector.
        """
        return self._screenplay[self._current_scene_name]

    def get_current_scene_name(self) -> str:
        """
        Used in SaveKeeper, GamePlayDialoguesChoice, SpriteAnimationPause, StageDirector.
        """
        return self._current_scene_name

    def set_scene_update_status(self, status: bool):
        """
        Used in GamePlayReading.
        """
        self._scene_update_status: bool = status

    def __call__(self):
        """
        Manages game scene selection and rendering.
        """
        # Keep current scene:
        if all(
                (
                        self._possible_next_scene_checker_flag == self._current_scene_name,
                        self._scene_update_status is False
                )
        ):
            return

        # Set new scene settings:
        self._current_scene_name: str = self._possible_next_scene_checker_flag
        self._scene_data: dict = self._screenplay[self._current_scene_name]
        self._scene_update_status: bool = False

        # Build a scene:
        self._stage_director.build_a_scene()

        # Autosave:
        if self._scene_data['gameplay_type'] == 'reading':
            self._autosave()

    @staticmethod
    def _autosave():
        """
        If current scene type is reading autosave it.
        """
        from ..Application_layer.Save_Keeper import SaveKeeper
        SaveKeeper().save(auto_save=True)
