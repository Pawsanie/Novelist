from ..UI_Base_menu import BaseMenu
from ...Universal_computing.Pattern_Singleton import SingletonPattern
from ...Application_layer.Save_Keeper import SaveKeeper
"""
Contains Load menu code.
"""


class LoadMenu(BaseMenu, SingletonPattern):
    """
    Controls reactions to user input commands from mouse or key bord in Load Menu.
    """
    def __init__(self):
        super(LoadMenu, self).__init__()
        self.save_keeper: SaveKeeper = SaveKeeper()
        self.selected_save_cell: list[int] | None = None
        self.selected_scene_name: str = ''
        self.menu_page: int = 1

    def vanish_menu_data(self):
        """
        Back menu to base state.
        """
        self.selected_save_cell: None = None
        self.selected_scene_name: str = ''
        self.menu_page: int = 1

    def start_game(self, scene_name: str):
        """
        Switch flags for correct game start.
        Start game from correct scene.
        :param scene_name: The name of the scene to start the game from.
        """
        self.scene_validator.scene = 'redraw'
        self.scene_validator.scene_flag = scene_name
        self.status: bool = False

        self.interface_controller.gameplay_interface_hidden_status = False
        self.interface_controller.gameplay_interface_status = True
        self.interface_controller.start_menu_flag = False

    def input_mouse(self, event):
        """
        Interface interaction in in-game load menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command: str = gameplay_ui_buttons[0]

            if command == 'load_menu_load':
                if self.selected_save_cell is not None:
                    self.start_game(
                        self.selected_scene_name
                    )
                    self.selected_save_cell: None = None
                self.save_keeper.reread = True

            elif command == 'load_menu_back':
                self.status: bool = False
                if self.interface_controller.start_menu_flag is True:
                    from .UI_Start_menu import StartMenu
                    StartMenu().status = True
                if self.interface_controller.start_menu_flag is False:
                    from .UI_Game_menu import GameMenu
                    GameMenu().status = True

            else:
                get_save_slot_data: dict = self.save_keeper.get_save_slot_data(command)
                self.selected_scene_name: str = get_save_slot_data['scene']
                self.selected_save_cell: list[int] = get_save_slot_data['save_cell']
