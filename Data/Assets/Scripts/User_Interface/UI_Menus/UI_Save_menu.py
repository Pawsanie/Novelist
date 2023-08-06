from ..UI_Base_menu import BaseMenu
from ...Universal_computing.Pattern_Singleton import SingletonPattern
from ...Application_layer.Save_Keeper import SaveKeeper
"""
Contains Save menu code.
"""


class SaveMenu(BaseMenu, SingletonPattern):
    """
    Controls reactions to user input commands from mouse or key bord in Save Menu.
    """
    def __init__(self):
        super(SaveMenu, self).__init__()
        self.save_keeper: SaveKeeper = SaveKeeper()
        self.selected_save_cell: int | None = None
        self.selected_scene_name: None = None
        self.menu_page: int = 1
        self.last_menu_page: int = 1
        self.empty_save_slot: tuple[str] = tuple('empty_save_slot')
        self.selected_save_file_name: str | None = None

    def vanish_menu_data(self):
        """
        Back menu to base state.
        """
        self.selected_save_cell: None = None
        self.selected_scene_name: None = None
        self.menu_page: int = 1
        self.last_menu_page: int = self.save_keeper.last_menu_page
        self.save_keeper.reread = True
        self.selected_save_file_name: None = None

    def save_slots_ui_reread(self):
        """
        Return ui to reread state.
        """
        self.selected_save_cell: None = None
        self.save_keeper.reread = True
        self.save_keeper.generate_save_slots_buttons()

    def save_game(self):
        """
        Save game and continue the game.
        """
        self.save_keeper.save(
            auto_save=False
        )
        self.status: bool = False
        self.interface_controller.gameplay_interface_status = True
        self.save_slots_ui_reread()

    def input_mouse(self, event):
        """
        Interface interaction in in-game save menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command: str = gameplay_ui_buttons[0]

            if command == 'save_menu_save':
                if self.selected_save_cell is not None:
                    if self.selected_scene_name is not None:
                        self.save_game()
                        if self.selected_scene_name != self.empty_save_slot:
                            self.save_keeper.delete_save(
                                self.selected_save_file_name
                            )

            elif command == 'save_menu_back':
                self.status: bool = False
                from .UI_Game_menu import GameMenu
                GameMenu().status = True

            elif command == 'save_menu_previous_page':
                if self.menu_page != 1:
                    self.menu_page -= 1
                    self.save_slots_ui_reread()

            elif command == 'save_menu_next_page':
                if self.menu_page != self.last_menu_page:
                    self.menu_page += 1
                    self.save_slots_ui_reread()

            else:
                get_save_slot_data: dict = self.save_keeper.get_save_slot_data(command)
                try:
                    self.selected_scene_name: str = get_save_slot_data['scene']
                except KeyError:
                    self.selected_scene_name: tuple[str] = self.empty_save_slot
                try:
                    self.selected_save_file_name: str = get_save_slot_data['save_name']
                except KeyError:
                    self.selected_save_file_name: None = None
                self.selected_save_cell: list[int] = get_save_slot_data['save_cell']
