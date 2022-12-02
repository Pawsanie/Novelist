from pygame import time, QUIT, quit, VIDEORESIZE, KEYDOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, mouse, KEYUP, K_TAB, K_e
from pygame import event as pygame_events

from .Stage_Director import StageDirector
from .Scene_Validator import SceneValidator
from .Interface_Controller import InterfaceController
"""
Contains gameplay code.
"""


def main_loop(func):
    """
    Decorator with the main loop of game.
    """
    def coroutine(*args, **kwargs):
        self = args[0]  # class method`s 'self.' for in class decorator.
        program_running = True
        main_cycle_fps_clock = time.Clock()
        main_cycle_fps = 30
        while program_running:
            for event in pygame_events.get():
                # Quit by exit_icon.
                if event.type == QUIT:
                    quit()
                    program_running = False
                    exit(0)
                # Set scene:
                if self.scene_validator.scene_flag != self.scene_validator.scene:
                    func(*args, **kwargs)
                # Window resize:
                if event.type == VIDEORESIZE:
                    self.scene = 'redraw'
                # User commands:
                self.gameplay.reactions_to_input_commands(event)
            main_cycle_fps_clock.tick(main_cycle_fps)

    return coroutine


class GamePlay:
    """
    Controls reactions to user input commands from mouse or key bord by conveyor
    in 'reactions_to_input_commands' method from 'main_loop'.

    :param stage_director: Stage Director class exemplar.
                           Responsible for stage production.
    :type stage_director: StageDirector
    :param interface_controller: InterfaceController exemplar.
                                 Responsible for user interface status and buttons.
    :type interface_controller: InterfaceController
    :param scene_validator: SceneValidator exemplar.
                            Responsible for scene order and scene construction.
    :type scene_validator: SceneValidator
    """
    def __init__(self, *, stage_director: StageDirector, interface_controller: InterfaceController,
                 scene_validator: SceneValidator):
        """
        :param stage_director: Stage Director class exemplar.
                               Responsible for stage production.
        :type stage_director: StageDirector
        :param interface_controller: InterfaceController exemplar.
                                     Responsible for user interface status and buttons.
        :type interface_controller: InterfaceController
        :param scene_validator: SceneValidator exemplar.
                                Responsible for scene order and scene construction.
        :type scene_validator: SceneValidator
        """
        # Stage Director settings:
        self.director: StageDirector = stage_director
        self.scene_validator: SceneValidator = scene_validator
        # User Interface controller settings:
        self.interface_controller: InterfaceController = interface_controller

    def __call__(self):
        """
        Need for calling by Game_Master class in main_loop.
        """
        pass

    def button_gameplay_ui_status(self):
        """
        Processing the gameplay interface.
        """
        button_clicked: tuple[bool, bool, bool] = mouse.get_pressed()

        # If user interface is not hidden:
        if self.interface_controller.gameplay_interface_hidden_status is False:
            gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status()
            # Clicking a button with a mouse:
            if gameplay_ui_buttons[1] is True:
                command = gameplay_ui_buttons[0]
                if command == 'past_scene':
                    if self.scene_validator.past_scene != 'START':
                        self.scene_validator.scene_flag = self.scene_validator.past_scene
                    else:
                        ...
                if command == 'hide_interface':
                    self.interface_controller.gameplay_interface_hidden_status = True
                if command == 'game_menu':
                    self.interface_controller.game_menu_status = True
                    self.interface_controller.gameplay_interface_status = False
                if command == 'next_scene':
                    if self.scene_validator.next_scene != 'FINISH':
                        self.scene_validator.scene_flag = self.scene_validator.next_scene
                    else:
                        ...
                if command == 'fast_forward':
                    if button_clicked[0] is not False:
                        if self.scene_validator.next_scene != 'FINISH':
                            self.scene_validator.scene_flag = self.scene_validator.next_scene

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
                if event.key == K_RIGHT:
                    if self.scene_validator.next_scene != 'FINISH':
                        self.scene_validator.scene_flag = self.scene_validator.next_scene
                if event.key == K_SPACE:
                    if self.scene_validator.next_scene != 'FINISH':
                        self.scene_validator.scene_flag = self.scene_validator.next_scene
            if self.interface_controller.game_menu_status is False:
                if event.key == K_ESCAPE:
                    self.interface_controller.game_menu_status = True
                    self.interface_controller.gameplay_interface_status = False

    def game_menu_ui_status(self):
        """
        Interface interaction in in-game menu.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status()
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'game_menu_continue':
                self.interface_controller.game_menu_status = False
                self.interface_controller.gameplay_interface_status = True
            if command == 'game_menu_save':
                self.interface_controller.game_menu_status = False
                self.interface_controller.save_menu_status = True
            if command == 'game_menu_load':
                self.interface_controller.game_menu_status = False
                self.interface_controller.load_menu_status = True
            if command == 'game_menu_settings':
                self.interface_controller.game_menu_status = False
                self.interface_controller.settings_menu_status = True
            if command == 'game_menu_exit':
                self.interface_controller.game_menu_status = False
                self.interface_controller.exit_menu_status = True

    def key_bord_game_menu_key_down(self, event):
        """
        Interface interaction in in-game menu.
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.interface_controller.game_menu_status = False
                self.interface_controller.gameplay_interface_status = True

    def game_exit_ui_from_game_menu_status(self):
        """
        Interface interaction in in-game exit menu.
        From GAME menu!
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status()
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'exit_menu_yes':
                quit()
                exit(0)
            if command == 'exit_menu_no':
                self.interface_controller.exit_menu_status = False
                self.interface_controller.game_menu_status = True

    def key_bord_exit_menu_from_game_menu_key_down(self, event):
        """
        Interface interaction in in-game exit menu.
        From GAME menu!
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_TAB:
                self.interface_controller.exit_menu_status = False
                self.interface_controller.game_menu_status = True
            if event.key == K_e:
                quit()
                exit(0)

    def game_exit_ui_from_start_menu_status(self):
        """
        Interface interaction in in-game exit menu.
        From START menu!
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status()
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'exit_menu_yes':
                quit()
                exit(0)
            if command == 'exit_menu_no':
                self.interface_controller.exit_menu_status = False
                self.interface_controller.start_menu_status = True

    def key_bord_exit_menu_from_start_menu_key_down(self, event):
        """
        Interface interaction in in-game exit menu.
        From START menu!
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_TAB:
                self.interface_controller.exit_menu_status = False
                self.interface_controller.start_menu_status = True
            if event.key == K_e:
                quit()
                exit(0)

    def input_wait_ready(self):
        """
        Stop loop after user command and redraw image.
        """
        self.scene_validator.scene = 'redraw'

    def gameplay_input(self, event):
        """
        Gameplay input conveyor:
        :param event: pygame.event from main_loop.
        """
        # Button gameplay ui status:
        self.button_gameplay_ui_status()
        # Button gameplay key bord status:
        self.key_bord_gameplay_key_down(event)
        self.input_wait_ready()

    def game_menu_input(self, event):
        """
        Game menu input conveyor:
        :param event: pygame.event from main_loop.
        """
        # Exit menu "from called" status flag:
        self.interface_controller.exit_from_start_menu_flag = False
        self.interface_controller.exit_from_game_menu_flag = True
        # Button game menu ui status:
        self.game_menu_ui_status()
        # Button game menu key bord status:
        self.key_bord_game_menu_key_down(event)
        self.input_wait_ready()

    def exit_menu_input(self, event):
        """
        Exit menu input conveyor:
        :param event: pygame.event from main_loop.
        """
        if self.interface_controller.exit_from_start_menu_flag is True:
            # Button game menu ui status:
            self.game_exit_ui_from_start_menu_status()
            # Button game menu key bord status:
            self.key_bord_exit_menu_from_start_menu_key_down(event)
        if self.interface_controller.exit_from_game_menu_flag is True:
            # Button game menu ui status:
            self.game_exit_ui_from_game_menu_status()
            # Button game menu key bord status:
            self.key_bord_exit_menu_from_game_menu_key_down(event)
        self.input_wait_ready()

    def setting_menu_input(self, event):
        """
        Setting menu conveyor:
        :param event: pygame.event from main_loop.
        """
        self.input_wait_ready()
        ...

    def load_menu_input(self, event):
        """
        Load menu conveyor:
        :param event: pygame.event from main_loop.
        """
        ...

    def save_menu_input(self, event):
        """
        Save menu conveyor:
        :param event: pygame.event from main_loop.
        """
        ...

    def start_menu_input(self, event):
        """
        Start menu conveyor:
        :param event: pygame.event from main_loop.
        """
        ...

    def settings_status_menu_input(self, event):
        """
        Settings status menu conveyor:
        :param event: pygame.event from main_loop.
        """
        ...

    def reactions_to_input_commands(self, event):
        """
        User commands conveyor:
        :param event: pygame.event from main_loop.
        """
        # Gameplay:
        if self.interface_controller.gameplay_interface_status is True:
            self.gameplay_input(event)
            return
        # Game menu:
        if self.interface_controller.game_menu_status is True:
            self.game_menu_input(event)
            return
        # Exit menu:
        if self.interface_controller.exit_menu_status is True:
            self.exit_menu_input(event)
            return
        # Setting menu:
        if self.interface_controller.settings_menu_status is True:
            self.setting_menu_input(event)
            return
        # Load menu:
        if self.interface_controller.load_menu_status is True:
            self.load_menu_input(event)
            return
        # Save menu:
        if self.interface_controller.save_menu_status is True:
            self.save_menu_input(event)
            return
        # Settings status menu:
        if self.interface_controller.settings_status_menu_status is True:
            self.settings_status_menu_input(event)
            return
        # Start menu:
        if self.interface_controller.start_menu_status is True:
            self.start_menu_input(event)
            return
