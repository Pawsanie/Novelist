from pygame import display, Surface

from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..Application_layer.Settings_Keeper import SettingsKeeper
from ..Application_layer.Stage_Director import StageDirector
from ..User_Interface.Interface_Controller import InterfaceController
from .Layer import Layer
from .Sprite import Sprite
"""
Contains code for display image render.
"""


class Render(SingletonPattern):
    """
    Render image on display.
    """
    def __init__(self):
        # Program layers settings:
        self._settings_keeper: SettingsKeeper = SettingsKeeper()
        self._stage_director: StageDirector = StageDirector()
        self._interface_controller: InterfaceController = InterfaceController()

        # Render settings:
        self._screen: Surface = self._settings_keeper.get_window()
        self.layers_collection: dict = {}
        self.batch_collection: list = []
        self.sprite_collection: list = []

        self.reset: bool = True
        self.save_screen: Surface = self._settings_keeper.get_window()

    def _screen_clear(self):
        """
        Clear scene before scene render.
        """
        self._screen.fill(
            (0, 0, 0)
        )

    def _render_devnull(self):
        """
        Devnull sprite, batch and layers collections.
        """
        self.layers_collection.clear()
        self.batch_collection.clear()
        self.sprite_collection.clear()

    def _initialization(self):
        """
        Prepare the scene for frame rendering.
        """
        if self.reset is True:
            self._render_devnull()

        # Generate background:
            self.batch_collection.append(
                self._stage_director.generate_background_batch()
            )

        # Generate characters:
            if self._interface_controller.start_menu_flag is False:
                self.batch_collection.append(
                    self._stage_director.generate_characters_batch()
                )
        # Generate speech:
                if self._interface_controller.gameplay_interface_hidden_status is False \
                        and self._interface_controller.gameplay_interface_status is True:
                    self.batch_collection.append(
                        self._stage_director.generate_speech()
                    )

        # Generate gameplay screen mask in game menu:
            self._menu_screen_mask()

        # Generate UI:
            if self._interface_controller.gameplay_interface_hidden_status is False:
                self.batch_collection.append(
                    self._interface_controller.generate_menus_batch()
                )

    def _save_screen_prepare(self):
        """
        Collect screen for game save.
        """
        from ..User_Interface.UI_Menus.UI_Game_menu import GameMenu

        if self._interface_controller.gameplay_type_reading is True \
                and self._interface_controller.menu_name is None\
                and GameMenu().status is False:
            self.save_screen: Surface = self._settings_keeper.get_window().convert()

    def _menu_screen_mask(self):
        """
        Make filter for gameplay part of game menu image.
        """
        from ..User_Interface.UI_Menus.UI_Game_menu import GameMenu

        if self._interface_controller.gameplay_type_reading is True \
                and self._interface_controller.menu_name is None\
                and GameMenu().status is True:
            self.sprite_collection.append(
                Sprite(
                    texture_mame="ui#screen_mask",
                    layer=3,
                    sprite_size=(self._screen.get_width(), self._screen.get_height()),
                    sprite_sheet_data={
                        "texture_type": "Backgrounds",
                        "sprite_sheet": False,
                        "statick_frames": {
                            "screen_mask": {}
                        }
                    }
                )
            )

    def _layers_initialization(self):
        """
        Sort layers.
        """
        if len(self.layers_collection) > 0:
            sorted_layers: list = sorted(
                self.layers_collection.items()
            )
            self.layers_collection: dict = {
                key: value for key, value in sorted_layers
            }

    def _single_sprites_initialization(self):
        """
        Add single sprites to layers.
        """
        for sprite in self.sprite_collection:
            sprite_layer: int = sprite.get_layer()

            if sprite_layer not in self.layers_collection:
                layer_object: Layer = Layer(sprite_layer)
                layer_object.append(sprite)
                self.layers_collection.update(
                    {sprite_layer: layer_object}
                )

            else:
                if sprite not in self.layers_collection[sprite_layer].sprite_collection:
                    self.layers_collection[sprite_layer].append(sprite)

    def image_render(self):
        """
        Render image on display screen.
        """
        # Clear old screen:
        self._screen_clear()

        # Render initialization:
        self._initialization()

        # Batch render initialization:
        if len(self.batch_collection) > 0:
            for batch in self.batch_collection:
                if batch.active is True:
                    batch.initialization()

        # Single sprites render initialization:
        if len(self.sprite_collection) > 0:
            self._single_sprites_initialization()

        # Display image render:
        self._layers_initialization()
        for layer in self.layers_collection.values():
            layer.draw()

        # Flip all surfaces:
        display.update()
        self._save_screen_prepare()
