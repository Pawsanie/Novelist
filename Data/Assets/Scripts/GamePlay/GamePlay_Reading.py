from pygame import KEYDOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, mouse, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame import event as pygame_events

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
        # Arguments processing:
        super(GamePlayReading, self).__init__()
        self.stage_director: StageDirector = StageDirector()

    def go_to_game_menu(self):
        """
        Switch to game menu.
        """
        self.interface_controller.gameplay_interface_status = False
        from ..User_Interface.UI_Menus.UI_Game_menu import GameMenu
        GameMenu().status = True
        self.state_machine.next_state()

    def button_gameplay_ui_status(self, event):
        """
        Processing the gameplay interface.
        :param event: pygame.event from main_loop.
        """
        button_clicked: tuple[bool, bool, bool] = mouse.get_pressed()

        # If user interface is not hidden:
        if self.interface_controller.gameplay_interface_hidden_status is False:
            if event.type != MOUSEBUTTONDOWN:
                if event.type == MOUSEBUTTONUP:
                    gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
                    command: str = gameplay_ui_buttons[0]

                    # Clicking a virtual button with a mouse:
                    if gameplay_ui_buttons[1] is True:
                        if command == 'past_scene':
                            if self.scene_validator.past_scene != 'START':
                                self.scene_validator.scene_flag = self.scene_validator.past_scene
                            else:
                                ...

                        elif command == 'hide_interface':
                            self.interface_controller.gameplay_interface_hidden_status = True

                        elif command == 'game_menu':
                            self.go_to_game_menu()

                        elif command == 'next_scene':
                            if self.scene_validator.next_scene != 'FINISH':
                                self.scene_validator.scene_flag = self.scene_validator.next_scene
                            else:
                                ...  # TODO: Make FINISH credits path.

                        elif command == 'fast_forward':
                            if button_clicked[0] is not False:
                                if self.scene_validator.next_scene != 'FINISH':
                                    self.scene_validator.scene_flag = self.scene_validator.next_scene

            # Next scene without virtual buttons:
            else:
                if button_clicked[0] is True:
                    gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_push_status()
                    if gameplay_ui_buttons[1] is False:
                        if self.scene_validator.next_scene != 'FINISH':
                            self.scene_validator.scene_flag = self.scene_validator.next_scene
                        new_event = pygame_events.wait()
                        while new_event.type != MOUSEBUTTONUP:
                            new_event = pygame_events.wait()

        # If user interface is hidden:
        else:
            if button_clicked[0] is True:
                self.interface_controller.gameplay_interface_hidden_status = False

    def key_bord_gameplay_key_down(self, event):
        """
        Checking pressed keys.
        Runs the functions associated with the desired keys.
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if self.interface_controller.gameplay_interface_hidden_status is False:

                if event.key == K_LEFT:
                    if self.scene_validator.past_scene != 'START':
                        self.scene_validator.scene_flag = self.scene_validator.past_scene

                elif event.key == K_RIGHT:
                    if self.scene_validator.next_scene != 'FINISH':
                        self.scene_validator.scene_flag = self.scene_validator.next_scene

                elif event.key == K_SPACE:
                    if self.scene_validator.next_scene != 'FINISH':
                        self.scene_validator.scene_flag = self.scene_validator.next_scene

            if self.interface_controller.game_menu_status is False:
                if event.key == K_ESCAPE:
                    self.go_to_game_menu()

    def gameplay_input(self, event):
        """
        Gameplay input conveyor:
        :param event: pygame.event from main_loop.
        """
        # Button gameplay ui status:
        self.button_gameplay_ui_status(event)
        # Button gameplay key bord status:
        self.key_bord_gameplay_key_down(event)
        self.input_wait_ready()
