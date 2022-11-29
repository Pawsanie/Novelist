from pygame import time, QUIT, quit, VIDEORESIZE, KEYDOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, mouse, KEYUP
from pygame import event as pygame_events

from .Stage_Director import StageDirector
from .Scene_Validator import SceneValidator
from .Interface_Controller import InterfaceController
"""
Contains gameplay code.
"""


def main_loop(func):
    """
    MAIN Coroutine!:
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
                self.gameplay.input_devices(event)
            main_cycle_fps_clock.tick(main_cycle_fps)

    return coroutine


class GamePlay:
    def __init__(self, *, stage_director: StageDirector, interface_controller: InterfaceController,
                 scene_validator: SceneValidator):
        # Stage Director settings:
        self.director: StageDirector = stage_director
        self.scene_validator: SceneValidator = scene_validator
        # User Interface controller settings:
        self.interface_controller: InterfaceController = interface_controller

    def __call__(self):
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
                if command == 'settings_menu':
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

        # Cursor position above the button:
        # if self.interface_controller.button_cursor_position_status() is True:
        #     self.scene_validator.scene = 'redraw'
        # else:
        #     self.scene_validator.scene = 'redraw'

    def key_bord_gameplay_key_down(self, event):
        """
        Checking pressed keys.
        Runs the functions associated with the desired keys.
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
                self.interface_controller.settings_status_menu_status = True
            if command == 'game_menu_exit':
                self.interface_controller.game_menu_status = False
                self.interface_controller.exit_menu_status = True

    def key_bord_game_menu_key_down(self, event):
        """
        Interface interaction in in-game menu.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.interface_controller.game_menu_status = False
                self.interface_controller.gameplay_interface_status = True

    def game_exit_ui_from_game_menu_status(self):
        """
        Interface interaction in in-game exit menu.
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
                self.interface_controller.gameplay_interface_status = True

    def key_bord_exit_menu_from_game_menu_key_down(self, event):
        """
        Interface interaction in in-game exit menu.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.interface_controller.exit_menu_status = False
                self.interface_controller.gameplay_interface_status = True

    def input_devices(self, event):
        """
        User commands:
        """
        if self.interface_controller.gameplay_interface_status is True:
            # Button gameplay ui status:
            self.button_gameplay_ui_status()
            # Button gameplay key bord status:
            self.key_bord_gameplay_key_down(event)
            self.scene_validator.scene = 'redraw'
            return
        if self.interface_controller.game_menu_status is True:
            # Button game menu ui status:
            self.game_menu_ui_status()
            # Button game menu key bord status:
            self.key_bord_game_menu_key_down(event)
            self.scene_validator.scene = 'redraw'
            return
        if self.interface_controller.exit_menu_status is True:
            if self.interface_controller is True:
                # Button game menu ui status:
                self.game_exit_ui_from_game_menu_status()
                # Button game menu key bord status:
                self.key_bord_exit_menu_from_game_menu_key_down(event)
            self.scene_validator.scene = 'redraw'
            return
