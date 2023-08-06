from pygame import display, Surface, SRCALPHA

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
        # Arguments processing:
        self.settings_keeper: SettingsKeeper = SettingsKeeper()
        self.stage_director: StageDirector = StageDirector()
        self.interface_controller: InterfaceController = InterfaceController()

        # Render settings:
        self.screen: Surface = self.settings_keeper.get_windows_settings()
        self.layers_collection: dict = {}
        self.batch_collection: list = []
        self.sprite_collection: list = []

        self.reset: bool = True
        self.save_screen: Surface = self.settings_keeper.screen

    def screen_clear(self):
        """
        Clear scene before scene render.
        """
        self.screen.fill((0, 0, 0))

    def render_devnull(self):
        """
        Devnull sprite, batch and layers collections.
        """
        self.layers_collection.clear()
        self.batch_collection.clear()
        self.sprite_collection.clear()

    def initialization(self):
        """
        Prepare the scene for frame rendering.
        """
        if self.reset is True:
            self.render_devnull()

        # Generate background:
            self.batch_collection.append(
                self.stage_director.generate_background_batch()
            )

        # Generate characters:
            if self.interface_controller.start_menu_flag is False:
                self.batch_collection.append(
                    self.stage_director.generate_characters_batch()
                )
        # Generate speech:
                if self.interface_controller.gameplay_interface_hidden_status is False \
                        and self.interface_controller.gameplay_interface_status is True:
                    self.batch_collection.append(
                        self.stage_director.generate_speech()
                    )

        # Generate gameplay screen mask in game menu:
            self.menu_screen_mask()

        # Generate UI:
            if self.interface_controller.gameplay_interface_hidden_status is False:
                self.batch_collection.append(
                    self.interface_controller.generate_menus_batch()
                )

    def save_screen_prepare(self):
        """
        Collect screen for game save.
        """
        from ..User_Interface.UI_Menus.UI_Game_menu import GameMenu

        if self.interface_controller.gameplay_type_reading is True \
                and self.interface_controller.menu_name is None\
                and GameMenu().status is False:
            self.save_screen: Surface = self.settings_keeper.screen.convert()

    def menu_screen_mask(self):
        """
        Make filter for gameplay part of game menu image.
        """
        from ..User_Interface.UI_Menus.UI_Game_menu import GameMenu

        if self.interface_controller.gameplay_type_reading is True \
                and self.interface_controller.menu_name is None\
                and GameMenu().status is True:
            screen_mask: Surface = Surface(
                [self.screen.get_width(), self.screen.get_height()],
                SRCALPHA
            )
            screen_mask.fill((0, 0, 0))
            screen_mask.set_alpha(210)

            self.sprite_collection.append(
                Sprite(
                    image=screen_mask,
                    layer=3
                )
            )

    def layers_initialization(self):
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

    def single_sprites_initialization(self):
        """
        Add single sprites to layers.
        """
        for sprite in self.sprite_collection:
            sprite_layer: int = sprite.layer

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
        self.screen_clear()

        # Render initialization:
        self.initialization()

        # Batch render initialization:
        if len(self.batch_collection) > 0:
            for batch in self.batch_collection:
                if batch.active is True:
                    batch.initialization()

        # Single sprites render initialization:
        if len(self.sprite_collection) > 0:
            self.single_sprites_initialization()

        # Display image render:
        self.layers_initialization()
        for layer in self.layers_collection.values():
            layer.draw()

        # Flip all surfaces:
        display.update()
        self.save_screen_prepare()
