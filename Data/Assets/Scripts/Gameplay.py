from pygame import time, QUIT, quit, VIDEORESIZE, KEYDOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, mouse, KEYUP, Surface, \
    display
from pygame import event as pygame_events

from .Stage_Director import StageDirector
from .Assets_load import json_load
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
                if self.scene_flag != self.scene:
                    func(*args, **kwargs)
                # Window resize:
                if event.type == VIDEORESIZE:
                    self.scene = 'redraw'
                # Button gameplay ui status:
                self.key_bord_gameplay_key_down(event)
                # Button gameplay key bord status:
                self.button_gameplay_ui_status()
            main_cycle_fps_clock.tick(main_cycle_fps)

    return coroutine


def gameplay_stage_director_initialization(*, display_screen):
    """
    Set all settings for Stage Director and game.
    Entry point for gameplay.

    :param display_screen: pygame.display.Surface
    """
    # Stage Director settings:
    director = StageDirector(display_screen=display_screen)
    gameplay = SceneValidator(director=director)
    gameplay()


class SceneValidator:
    """
    Controls in what order the scenes go and their settings.

    :param director: Import StageDirector.
    :type director: StageDirector.
    """
    def __init__(self, *, director: StageDirector):
        """
        :param director: Import StageDirector.
        :type director: StageDirector.
        """
        # Screenplay loading:
        self.screenplay: dict = json_load(path_list=['Scripts', 'Json_data', 'screenplay'])
        # Stage Director settings:
        self.director: StageDirector = director
        # Scene FLAG:
        self.scene: str = 'START'  # START as default!
        self.scene_flag: str = 'test'  # <------- TEST SCENE!
        self.next_scene: str = ''
        self.past_scene: str = ''

    # @main_loop
    # def __call__(self):
    #     if self.settings_menu_status == 'off':
    #         self.gameplay()
    #     else:
    #         self.settings_menu()

    @main_loop
    def __call__(self):
        """
        Manages game scene selection and rendering.
        """
        # Set new scene!:
        if self.scene_flag != self.scene:
            self.director.vanishing_scene()
            scene: dict = self.screenplay[self.scene_flag]
            self.director.set_scene(location=scene['background'])
            for name in scene['actors']:
                character = scene['actors'][name]
                self.director.set_actor(character=name).set_pose(pose_number=character['character_pose'])
                self.director.set_actor(character=name).set_plan(plan=character['character_plan'])
                if character['character_start_position'] == 'middle':
                    self.director.set_actor(character=name).move_to_middle()
                if character['character_start_position'] == 'right':
                    self.director.set_actor(character=name).move_to_right()
                if character['character_start_position'] == 'left':
                    self.director.set_actor(character=name).move_to_left()
            # Scene FLAG settings!:
            self.scene: str = self.scene_flag
            self.next_scene: str = scene['next_scene']
            self.past_scene: str = scene['past_scene']
            # Scene text settings!:
            self.director.set_words(script=self.director.text_dict.get(self.director.language_flag)[self.scene])
            # Special effects!:
            if scene['special_effects'] is not False:
                ...
        # Keep current scene!:
        else:
            pass
        self.director.action()

    def button_gameplay_ui_status(self):
        """
        Processing the gameplay interface.
        """
        button_clicked: tuple[bool, bool, bool] = mouse.get_pressed()

        # If user interface is not hidden:
        if self.director.interface_controller.gameplay_interface_status is True:
            gameplay_ui_buttons: tuple[str, bool] = self.director.interface_controller.button_clicked_status()
            # Clicking a button with a mouse:
            if gameplay_ui_buttons[1] is True:
                command = gameplay_ui_buttons[0]
                if command == 'past_scene':
                    if self.past_scene != 'START':
                        self.scene_flag: str = self.past_scene
                    else:
                        ...
                if command == 'hide_interface':
                    self.director.interface_controller.gameplay_interface_status = False
                if command == 'settings_menu':
                    self.settings_menu()
                if command == 'next_scene':
                    if self.next_scene != 'FINISH':
                        self.scene_flag: str = self.next_scene
                    else:
                        ...
                if command == 'fast_forward':
                    if button_clicked[0] is not False:
                        if self.next_scene != 'FINISH':
                            self.scene_flag: str = self.next_scene

        # If user interface is hidden:
        else:
            if button_clicked[0] is True:
                self.director.interface_controller.gameplay_interface_status = True

        # Cursor position above the button:
        if self.director.interface_controller.button_cursor_position_status() is True:
            self.scene: str = 'redraw'
        else:
            self.scene: str = 'redraw'

    def key_bord_gameplay_key_down(self, event):
        """
        Checking pressed keys.
        Runs the functions associated with the desired keys.
        """
        if event.type == KEYDOWN:
            if self.director.interface_controller.gameplay_interface_status is True:
                if event.key == K_LEFT:
                    if self.past_scene != 'START':
                        self.scene_flag: str = self.past_scene
                if event.key == K_RIGHT:
                    if self.next_scene != 'FINISH':
                        self.scene_flag: str = self.next_scene
                if event.key == K_SPACE:
                    if self.next_scene != 'FINISH':
                        self.scene_flag: str = self.next_scene
            if self.director.interface_controller.game_menu_status is False:
                if event.key == K_ESCAPE:
                    self.director.interface_controller.game_menu_status = True
                    self.settings_menu()
            else:
                if event.key == K_ESCAPE:
                    self.director.interface_controller.game_menu_status = False

    def settings_menu(self):
        """
        Launches the in-game menu.
        """
        self.director.interface_controller.gameplay_interface_status = False
        self.director.interface_controller.game_menu_status = True
        screen: Surface = self.director.display_screen

        screen_mask = Surface([screen.get_width(), screen.get_height()])
        screen_mask.fill((0, 0, 0))
        screen_mask.set_alpha(128)

        screen.blit(screen_mask, (0, 0))
        display.update()
