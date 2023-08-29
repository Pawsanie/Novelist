from ..Application_layer.Stage_Director import StageDirector
from ..User_Interface.UI_Base_menu import BaseMenu
from ..User_Interface.UI_Buttons.UI_GamePlay_Choice_Button import GamePlayChoiceButton
from ..Application_layer.Assets_load import json_load
"""
Contains gameplay of choice code.
"""


class GamePlayDialoguesChoice(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in choice gameplay.
    Generated in GamePlayAdministrator from 'Game_Play_Administrator.py' file.
    """
    def __init__(self):
        # Arguments processing:
        super(GamePlayDialoguesChoice, self).__init__()
        self.stage_director: StageDirector = StageDirector()
        # Gameplay choice buttons generate:
        self.dialogues_buttons: dict = {}
        self.dialogues_choice_buttons_generations()

    def dialogues_choice_buttons_generations(self):
        """
        Generate dict with buttons for dialogues choice gameplay.
        This is a nested dictionary of button`s group and an instance of the Button class.
        """
        # localizations instructions from 'dialogues_localizations_data.json':
        localizations_data: dict[str] = json_load(
            ['Scripts', 'Json_data', 'Dialogues', 'dialogues_localizations_data']
        )
        # localizations data:
        localizations: tuple[str] = (
            localizations_data['language_flags']
        )
        # All buttons text localizations:
        all_buttons_text_localizations_dict: dict = {}
        for language in localizations:
            all_buttons_text_localizations_dict.update(
                {language: json_load(['Scripts', 'Json_data', 'Dialogues', 'Choice', language])}
            )
        choice_buttons_text: dict[str] = all_buttons_text_localizations_dict[self.stage_director.language_flag]
        # Generate dialogues choice buttons:
        dialogues_buttons: dict = {}
        for scene in choice_buttons_text:
            if choice_buttons_text[scene] is not False:
                for index, choice in enumerate(choice_buttons_text[scene]):
                    # Generate text localizations for button:
                    buttons_text_localization: dict = {}
                    for language in all_buttons_text_localizations_dict:
                        buttons_text_localization.update(
                            {language: all_buttons_text_localizations_dict[language][scene][choice]}
                        )
                    # Generate sprite data for button:
                    image_data_dict: dict = json_load(
                        ['Scripts', 'Json_data', 'Dialogues', 'dialogues_choice_buttons']
                    )
                    image_data_dict.update({"index_number": index})
                    # Generate button:
                    dialogues_buttons.update(
                        {choice: GamePlayChoiceButton(
                            button_name=choice,
                            button_text=choice_buttons_text[scene][choice],
                            button_image_data=image_data_dict,
                            button_text_localization_dict=buttons_text_localization
                        )})
                    self.dialogues_buttons.setdefault(scene, dialogues_buttons)

    def button_gameplay_ui_status(self, event):
        """
        Processing the gameplay choice.
        :param event: pygame.event from main_loop.
        """
        # Rules of choice for scene:
        choice_data: dict[str, dict[str]] = self.scene_validator.choices_data[self.scene_validator.scene]

        # If user interface is not hidden:
        if self.interface_controller.gameplay_interface_hidden_status is False:
            gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
            # Clicking a virtual button with a mouse:
            if gameplay_ui_buttons[1] is True:
                command = gameplay_ui_buttons[0]
                for choice in choice_data:
                    if command == choice:
                        if choice_data[choice]['branching'] is not False:
                            self.scene_validator.scene_flag = choice_data[choice]['branching']
                        if choice_data[choice]['counter_change'] is not False:
                            ...  # TODO: Add reputation system?

    def key_bord_gameplay_key_down(self, event):
        ...

    def gameplay_input(self, event):
        """
        Gameplay input conveyor:
        :param event: 'pygame.event' from main_loop.
        """
        # Button gameplay ui status:
        # self.interface_controller.gameplay_choice_buttons = self.dialogues_buttons[self.scene_validator.scene]
        self.button_gameplay_ui_status(event)
        # Button gameplay key bord status:
        self.key_bord_gameplay_key_down(event)
        self.input_wait_ready()
