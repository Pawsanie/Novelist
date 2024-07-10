from ..UI_Base_menu import BaseMenu
from ...Universal_computing.Pattern_Singleton import SingletonPattern
from ...Application_layer.Save_Keeper import SaveKeeper
from ..UI_Menu_Text import MenuText
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
        self.selected_save_cell: str | None = None
        self.selected_scene_name: None = None
        self.menu_page: int = 1
        self.last_menu_page: int = 1
        self.empty_save_slot: tuple[str] = tuple('empty_save_slot')
        self.selected_save_file_name: str | None = None

        self.page_select_text: str = f"{self.menu_page} / {self.last_menu_page}"
        self.menu_name: str = 'save_menu'
        self.text_file_flag: str = 'text_file'
        self.page_text_coordinates: dict = {'x': 1, 'y': 1}
        self.page_text_font: None = None
        self.page_text_color: str = '#FFFFFF'
        self.page_flag: str = 'current_page_text'

    def vanish_menu_data(self):
        """
        Back menu to base state.
        """
        self.selected_save_cell: None = None
        self.selected_scene_name: None = None
        self.menu_page: int = 1
        self.last_menu_page: int = self.save_keeper.last_menu_page
        self.save_keeper.reread()
        self.selected_save_file_name: None = None
        self.unselect_cell()
        self.set_menu_pages_text()

    def set_menu_pages_text(self):
        """
        Set new page data to menu text.
        """
        self.page_select_text: str = f"{self.menu_page} / {self.last_menu_page}"

        self._interface_controller.menus_text_dict.update(
            {
                self.page_flag: {
                    self.menu_name: MenuText(
                        menu_name=self.menu_name,
                        menu_text=self.page_select_text,
                        menu_text_localization_dict=None,
                        menu_text_font=self.page_text_font,
                        menu_text_color=self.page_text_color,
                        menu_text_coordinates=self.page_text_coordinates,
                        menu_text_substrate=None,
                        menu_text_factor=2.5
                    )
                }
            }
        )

        menu_data: dict = self._interface_controller.menus_collection[self.menu_name]
        menu_data[self.text_file_flag]: str = self.page_flag

    def save_slots_ui_reread(self):
        """
        Return ui to reread state.
        """
        self.selected_save_cell: None = None
        self.save_keeper.reread()
        self.save_keeper.generate_save_slots_buttons()

    def unselect_cell(self):
        """
        Try to unselect last select save slot.
        """
        try:
            self._interface_controller.buttons_dict['ui_save_menu_buttons'][self.selected_save_cell].select = False
        except KeyError:
            pass

    def save_game(self):
        """
        Save game and continue the game.
        """
        self.save_keeper.save(
            auto_save=False
        )
        self.status: bool = False
        self._interface_controller.gameplay_interface_status = True
        self.save_slots_ui_reread()

        self._state_machine.next_state()

    def _input_mouse(self, event):
        """
        Interface interaction in in-game save menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self._interface_controller.button_clicked_status(event)
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
                        self.vanish_menu_data()

            elif command == 'save_menu_back':
                self.status: bool = False
                from .UI_Game_menu import GameMenu
                GameMenu().status = True
                self.vanish_menu_data()

            elif command == 'save_menu_previous_page':
                if self.menu_page != 1:
                    self.menu_page -= 1
                    self.save_slots_ui_reread()
                    self.set_menu_pages_text()

            elif command == 'save_menu_next_page':
                if self.menu_page != self.last_menu_page:
                    self.menu_page += 1
                    self.save_slots_ui_reread()
                    self.set_menu_pages_text()

            else:
                self.unselect_cell()
                get_save_slot_data: dict = self.save_keeper.get_save_slot_data(command)
                try:
                    self.selected_scene_name: str = get_save_slot_data['scene']
                except KeyError:
                    self.selected_scene_name: tuple[str] = self.empty_save_slot
                try:
                    self.selected_save_file_name: str = get_save_slot_data['save_name']
                except KeyError:
                    self.selected_save_file_name: None = None
                self.selected_save_cell: str = get_save_slot_data['select_name']
                self._interface_controller.buttons_dict['ui_save_menu_buttons'][self.selected_save_cell].select = True
