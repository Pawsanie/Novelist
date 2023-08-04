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
        self.selected_scene_name: str = ''
        self.menu_page: int = 1

    def vanish_menu_data(self):
        """
        Back menu to base state.
        """
        self.selected_save_cell: None = None
        self.selected_scene_name: str = ''
        self.menu_page: int = 1

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
                    self.save_keeper.save(
                        auto_save=False
                    )
                    self.selected_save_cell: None = None
                self.save_keeper.reread = True

            elif command == 'save_menu_back':
                self.status: bool = False
                from .UI_Game_menu import GameMenu
                GameMenu().status = True

            else:
                get_save_slot_data: dict = self.save_keeper.get_save_slot_data(command)
                self.selected_scene_name: str = get_save_slot_data['scene']
                self.selected_save_cell: list[int] = get_save_slot_data['save_cell']
