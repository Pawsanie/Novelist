from abc import ABC, abstractmethod

from ..UI_Buttons.UI_Base_Button import BaseButton
from ..UI_Base_menu import BaseMenu
from ...User_Interface.Interface_Controller import InterfaceController
from ...Universal_computing.Alternative_deep_copy import deep_copy_alternative
from ...Universal_computing.Surface_size import surface_size


class BaseDropdown(ABC):

    def __init__(self, buttons_collection: dict, menu_destination: str):
        """
        :param buttons_collection:
        :type buttons_collection: dict
        """
        self.interface_controller: InterfaceController = InterfaceController()

        self.menu_destination: str = menu_destination

        self.menu_buttons_reference: dict = deep_copy_alternative(
            self.interface_controller.buttons_dict[self.menu_destination]
        )

        # Dropdown button generate:
        self.buttons_collection: dict[str, BaseButton] = buttons_collection
        self.anchor_button: dict[str, BaseButton] = self.buttons_collection.items()[0]
        self.status: bool = False

        # Point for open buttons list:
        # Can be: down|left|right|up string.
        # "down" as default value.
        self.anchor_point: str = "down"

    def open_dropdown(self):
        self.menu_import()
        ...

    def close_dropdown(self):
        self.menu_import()
        ...

    def update_dropdown_ui_buttons(self):
        menu_object: BaseMenu = self.menu_import()
        menu_buttons: dict = self.interface_controller.buttons_dict[self.menu_destination]

        if menu_object.status is True:
            menu_buttons.clear()
            menu_buttons.update({
                **self.menu_buttons_reference,
                **self.anchor_button
            })

            if self.status is True:
                menu_buttons.update(
                    self.menu_buttons_reference
                )

    @abstractmethod
    def menu_import(self) -> BaseMenu:
        """
        from ..User_Interface.UI_Menus.UI_Abstract_Menu import AbstractMenu
        return AbstractMenu
        """
        pass
