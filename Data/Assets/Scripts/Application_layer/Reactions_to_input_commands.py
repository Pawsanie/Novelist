from asyncio import sleep

from pygame import QUIT, quit
from pygame import event as pygame_events
from pygame.event import Event

from ..User_Interface.Interface_Controller import InterfaceController
from ..User_Interface.UI_Menus.UI_Exit_menu import ExitMenu
from ..User_Interface.UI_Menus.UI_Game_menu import GameMenu
from ..User_Interface.UI_Menus.UI_Load_menu import LoadMenu
from ..User_Interface.UI_Menus.UI_Save_menu import SaveMenu
from ..User_Interface.UI_Menus.UI_Settings_menu import SettingsMenu
from ..User_Interface.UI_Menus.UI_Settings_Status_menu import SettingsStatusMenu
from ..User_Interface.UI_Menus.UI_Start_menu import StartMenu
from ..User_Interface.UI_Menus.UI_Back_to_Start_menu_Status_menu import BackToStartMenuStatusMenu
from ..User_Interface.UI_Menus.UI_Creators_menu import CreatorsMenu
from ..GamePlay.GamePlay_Administrator import GamePlayAdministrator
from ..Universal_computing.Pattern_Singleton import SingletonPattern
"""
Contains code for reactions to input commands.
"""


class InputCommandsReactions(SingletonPattern):
    """
    Controls reactions to user input commands from mouse or key bord by conveyor
    in '_reactions_to_input_commands' method from 'input_commands_loop'.
    """
    _menus_collection: dict = {
        'exit_menu': {
            'object': ExitMenu(),
            'menu_file': 'ui_exit_menu_buttons',
            'text_file': 'ui_exit_menu_text'
        },
        'settings_menu': {
            'object': SettingsMenu(),
            'menu_file': 'ui_settings_menu_buttons',
            'text_file': None
        },
        'load_menu': {
            'object': LoadMenu(),
            'menu_file': 'ui_load_menu_buttons',
            'text_file': None
        },
        None: {
            'object': GameMenu(),
            'menu_file': 'ui_game_menu_buttons',
            'text_file': None
        },
        'save_menu': {
            'object': SaveMenu(),
            'menu_file': 'ui_save_menu_buttons',
            'text_file': None
        },
        'settings_status_menu': {
            'object': SettingsStatusMenu(),
            'menu_file': 'ui_settings_status_buttons',
            'text_file': 'ui_settings_status_text'
        },
        'start_menu': {
            'object': StartMenu(),
            'menu_file': 'ui_start_menu_buttons',
            'text_file': None
        },
        'back_to_start_menu_status_menu': {
            'object': BackToStartMenuStatusMenu(),
            'menu_file': 'ui_back_to_start_menu_status_menu_buttons',
            'text_file': 'ui_back_to_start_menu_status_menu_text'
        },
        'creators_menu': {
            'object': CreatorsMenu(),
            'menu_file': 'ui_creators_menu_buttons',
            'text_file': 'ui_creators_menu_text'
        }
    }

    def __init__(self):
        # Program layers:
        self._interface_controller: InterfaceController = InterfaceController()
        self._gameplay_administrator: GamePlayAdministrator = GamePlayAdministrator()

        # Itself data proxy:
        self._interface_controller.menus_collection = self._menus_collection

    async def _reactions_to_input_commands(self, event: Event):
        """
        User commands conveyor.
        Uses in input_command_oop.
        :param event: 'pygame.event' from input_commands_loop.
        """
        # Gameplay:
        if self._interface_controller.gameplay_interface_status is True:
            await self._gameplay_administrator.gameplay_input(event)
            return
        # Game menus:
        for key in self._menus_collection:
            menu = self._menus_collection[key]['object']
            if menu.status is True:
                menu.menu_input(event)
                return

    async def input_commands_loop(self):
        """
        Controller MVC pattern part: coll from GameMaster.
        """
        while True:
            for event in pygame_events.get():

                # Quit by exit_icon:
                if event.type == QUIT:
                    quit()
                    exit(0)

                # User commands:
                await self._reactions_to_input_commands(event)

            pygame_events.clear()
            await sleep(0)
