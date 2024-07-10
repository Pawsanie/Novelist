from asyncio import sleep

from pygame import KEYDOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, mouse, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame import event as pygame_events
from pygame.event import Event

from ..Application_layer.Stage_Director import StageDirector
from ..User_Interface.UI_Base_menu import BaseMenu
from ..Universal_computing.Pattern_Singleton import SingletonPattern
"""
Contains gameplay reading code.
"""


class GamePlayReading(BaseMenu, SingletonPattern):
    """
    Controls reactions to user input commands from mouse or key bord in reading gameplay.
    Generated in GamePlayAdministrator from 'Game_Play_Administrator.py' file.
    """
    def __init__(self):
        super().__init__()
        # Program layers settings:
        self.stage_director: StageDirector = StageDirector()

    def _go_to_game_menu(self):
        """
        Switch to game menu.
        """
        self._interface_controller.gameplay_interface_status = False
        from ..User_Interface.UI_Menus.UI_Game_menu import GameMenu
        GameMenu().status = True
        self._state_machine.next_state()

        from .Scene_Validator import SceneValidator
        SceneValidator().set_scene_update_status(True)

    async def _button_gameplay_ui_status(self, event: Event):
        """
        Processing the gameplay interface interaction.
        :param event: pygame.event.Event from main_loop.
        """
        button_clicked: tuple[bool, bool, bool] = mouse.get_pressed()

        # If user interface is not hidden:
        if self._interface_controller.gameplay_interface_hidden_status is False:
            if event.type != MOUSEBUTTONDOWN:
                if event.type == MOUSEBUTTONUP:
                    gameplay_ui_buttons: tuple[str, bool] = self._interface_controller.button_clicked_status(event)
                    command: str = gameplay_ui_buttons[0]

                    # Clicking a virtual button with a mouse:
                    if gameplay_ui_buttons[1] is True:
                        if command == 'past_scene':
                            if self._scene_validator.get_current_scene_data()["past_scene"] != 'START':
                                self._scene_validator.switch_scene(
                                    self._scene_validator.get_current_scene_data()["past_scene"]
                                )
                            else:
                                ...

                        elif command == 'hide_interface':
                            self._interface_controller.gameplay_interface_hidden_status = True

                        elif command == 'game_menu':
                            self._go_to_game_menu()

                        elif command == 'next_scene':
                            if self._scene_validator.get_current_scene_data()["next_scene"] != 'FINISH':
                                self._scene_validator.switch_scene(
                                    self._scene_validator.get_current_scene_data()["next_scene"]
                                )
                            else:
                                ...  # TODO: Make FINISH credits path.

                        elif command == 'fast_forward':
                            if button_clicked[0] is not False:
                                if self._scene_validator.get_current_scene_data()["next_scene"] != 'FINISH':
                                    self._scene_validator.switch_scene(
                                        self._scene_validator.get_current_scene_data()["next_scene"]
                                    )

            # Next scene without virtual buttons:
            else:
                if button_clicked[0] is True:
                    gameplay_ui_buttons: tuple[str, bool] = self._interface_controller.button_push_status()
                    if gameplay_ui_buttons[1] is False:
                        new_event: Event = pygame_events.poll()
                        while new_event.type != MOUSEBUTTONUP:
                            new_event: Event = pygame_events.poll()
                            await sleep(0)
                        if self._scene_validator.get_current_scene_data()["next_scene"] != 'FINISH':
                            self._scene_validator.switch_scene(
                                self._scene_validator.get_current_scene_data()["next_scene"]
                            )

        # If user interface is hidden:
        else:
            if button_clicked[0] is True:
                self._interface_controller.gameplay_interface_hidden_status = False

    def _key_bord_gameplay_key_down(self, event):
        """
        Checking pressed keys.
        Runs the functions associated with the desired keys.
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if self._interface_controller.gameplay_interface_hidden_status is False:

                if event.key == K_LEFT:
                    if self._scene_validator.get_current_scene_data()["past_scene"] != 'START':
                        self._scene_validator.switch_scene(
                            self._scene_validator.get_current_scene_data()["past_scene"]
                        )

                elif event.key == K_RIGHT:
                    if self._scene_validator.get_current_scene_data()["next_scene"] != 'FINISH':
                        self._scene_validator.switch_scene(
                            self._scene_validator.get_current_scene_data()["next_scene"]
                        )

                elif event.key == K_SPACE:
                    if self._scene_validator.get_current_scene_data()["next_scene"] != 'FINISH':
                        self._scene_validator.switch_scene(
                            self._scene_validator.get_current_scene_data()["next_scene"]
                        )

            if self._interface_controller.game_menu_status is False:
                if event.key == K_ESCAPE:
                    self._go_to_game_menu()

    async def gameplay_input(self, event: Event):
        """
        Gameplay input conveyor:
        Call from GameplayAdministrator.
        :param event: pygame.event.Event from main_loop.
        """
        # Button gameplay ui status:
        await self._button_gameplay_ui_status(event)
        # Button gameplay key bord status:
        self._key_bord_gameplay_key_down(event)
        self._input_wait_ready()
