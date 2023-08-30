# Pygame Visual Novel:

This repository contains the source code to create a Visual Novel game based on minimal edits using Python if it needed.<br/>
And just setting up a few json files.

I was inspired to develop this code by the inability to use [RenPy](https://www.renpy.org/) to create a game in the form in which I want.<br>
As well as not wanting to learn RenPy scripting language.

In addition, writing your own game, almost from scratch, is quite interesting.

:warning:The code probably needs some light refactoring.:warning: <br>
:warning:Please note that some non-game features are not fully implemented.:warning:

## Disclaimer:
:warning:**Using** some or all of the elements of this code, **You** assume **responsibility for any consequences!**<br>

:warning:The **licenses** for the technologies on which the code **depends** are subject to **change by their authors**.<br><br>

___
<br>

## Required:
The application code is written in python and obviously depends on it.<br>
**Python** version 3.6 [Python Software Foundation License / (with) Zero-Clause BSD license (after 3.8.6 version Python)]:
* :octocat:[Python GitHub](https://github.com/python)
* :bookmark_tabs:[Python internet page](https://www.python.org/)

## Required Packages:
**PyGame** [GNU LGPL version 2.1]:
* :octocat:[PyGame GitHub](https://github.com/pygame/pygame)
* :bookmark_tabs:[Pygame internet page](https://www.pygame.org/news)

Used to create windows, surfaces and draw them on top of each other.<br>
Also for flipping the screen and drawing the window icon.


## Installing the Required Packages:
```bash
pip install pygame
```

## How to run the application:
To run the application, you need to run the 'Visual_novel_game.py' script with your shell.<br>
**Example of shell command:**<br>
```shell
python -B Visual_novel_game.py
```
**File location:**<br>
**./**:open_file_folder:Data<br>
   └── :page_facing_up:Visual_novel_game.py


## Settings of scenes:

### Scene order:
To adjust the scene order, you need to change the json file **'screenplay.json'**.<br>
At the same time, the first scene **must** be named **scene_01**!<br>
And the 'past_scene' key of 'scene_01' **must** be **'START'**.<br>
In the last scene next_scene key **must** be **'FINISH'**.<br>

**File location:**<br>
./:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Scripts<br>
                     └── :file_folder:Json_data<br>
                              └── :page_facing_up:screenplay.json<br>

**Example of one scene in screenplay.json file:**
```json
{
   "scene_01": {
      "background": "back_ground_01",
      "actors": {
         "Character_1": {
            "character_start_position": "right",
            "character_pose": "3",
            "character_plan": "background_plan"
         },
         "Character_2": {
            "character_start_position": "middle",
            "character_pose": "2",
            "character_plan": "first_plan"
         }
      },
      "special_effects": false,
      "gameplay_type": "reading",
      "past_scene": "START",
      "next_scene": "scene_02"
   }
}
```
In this case, the keys indicate which scene was before 'scene_01' and which should be after (scene_02).<br>
Scenes 'START' or 'FINISH' do not exist.<br>
But the game focuses on its flags.<br>
Please note that a '**gameplay_type**' key value must be **reading/choice/false** where the first two options are strings.<br>
Please note that an **actors** characters keys must match certain values:<br>
**character_start_position** - may have values **right/middle/left**.<br>
**character_pose** - can be any key from the dictionary 'characters_sprites.json'. <br>
More about this further in **"Characters and their sprites"** paragraph.<br>
**character_plan** - may have values **background_plan/first_plan**.

### Dialogues:
Game dialogues have to be writen in **lang_tag.json** file... **eng.json** as example...<br>
And this tag must be writen in **dialogues_localizations_data.json** file.<br>
You need to name localization language tags for translation in the game settings.

**Files location:**<br>
**./**:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Scripts<br>
                     └── :file_folder:Json_data<br>
                              └── :file_folder:Dialogues<br>
                                       ├── :file_folder:Choice<br>
                                       │       └── :page_facing_up:eng.json **(Can be your localization)**<br>
                                       ├── :file_folder:Reading<br>
                                       │       └── :page_facing_up:eng.json **(Can be your localization)**<br>
                                       └── :page_facing_up:dialogues_localizations_data.json<br>

**Example of one scene in 'eng.json' file in 'Reading' folder':**
```json
{
   "scene_01": {
    "who": {
      "text": "Test Chan",
      "color": "#00ffff"
    },
    "what": {
      "text": "Hello World!",
      "color": "#ffffff"
    }
  }
}
```
**Example of 'eng.json' file in 'Choice' folder':**
```json
{
  "scene_01": false,

  "test_scene_02": {
    "choice_01": "Got to Scene 01",
    "choice_02": "ERROR!",
    "choice_03": "Go to Scene 03"
  },

  "test_scene_03": false

}
```
Scenes with '**false**' keys can be omitted.

**Example of 'dialogues_localizations_data.json' file:**
```json
{
  "language_flags": [
    "eng",
    "ru"
  ]
}
```

## Characters and their sprites:
Information about the characters is stored in a 'characters_sprites.json 'file.<br>
It needs to list the names by which the game will look for characters. <br>
Sprite file name. And the x|y coordinates for sprite animations.<br>
**File location:**<br>
**./**:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Scripts<br>
                     └── :file_folder:Json_data<br>
                              └── :page_facing_up:characters_sprites.json<br>
**Example of 'characters_sprites.json' file:**
```json
{
  "Character_1": {
    "sprite": "blank",
    "poses": {
      "1": {
        "x": [25, 280],
        "y": [49, 618]
      },
      "2": {
        "x": [330, 594],
        "y": [49, 618]
}}}}
```
Please note that the name of the sprite is indicated without the file extension.<br>
The coordinates are in pixels.<br>
**Please note** that the name specified here is how the key is used in the **'screenplay.json'** file!<br>
And this name is in no way related to the one you can set in the dialogs!<br>
As example 'eng.json' file from 'Dialogues' folder.

Sprites must be in **png** format and stored in a 'Characters' folder.<br>
**Folder location:**<br>
./:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Images<br>
                    └── :file_folder:Characters<br>
                           └── :framed_picture:*.png **(Can be your image file)**<br>

## Backgrounds and its sprites:
Information about the backgrounds and its sprites must be entered into the 'backgrounds_sprites.json' file.<br>
The names that will be given here are used to create scenes in 'screenplay.json' fie.

**File location:**<br>
**./**:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Scripts<br>
                     └── :file_folder:Json_data<br>
                              └── :page_facing_up:backgrounds_sprites.json<br>
**Example of 'backgrounds_sprites.json' file:**
```json
{
  "back_ground_01": "blank",

  "exit_menu": "blank",
  "settings_menu": "blank",
  "load_menu": "blank",
  "save_menu": "blank",
  "settings_status_menu": "blank",
  "start_menu": "blank"
}
```
As you can see from the example, names are also used for static menus.

Sprites must be in **jpg** format and stored in a 'Backgrounds' folder.<br>
**Folder location:**<br>
./:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            ├── :file_folder:Images<br>
            └── :file_folder:Backgrounds<br>

However, you can change the sprite's format requirement by modifying it in the code.

## User Interface:
Information about the standard user interface is contained in 'ui_menu-name_buttons.json' files and 'ui_localizations_data.json'.<br>
Localization of the standard interface is stored in the appropriate files: 'eng.json' as example.

**Below** examples with **json`s** describes the code that needs to be changed if you want to supplement the standard menus with your own.

**Files locations:**<br>
**./**:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Scripts<br>
                     └── :file_folder:Json_data<br>
                              └── :file_folder:User_Interface<br>
                                       ├── :file_folder:UI_Buttons<br>
                                       │        ├── :page_facing_up:ui_\*_buttons.json **(Can be your button file)**<br>
                                       │        └── :file_folder:Localization<br>
                                       │                 ├── :page_facing_up:eng.json **(Can be your localization)**<br>
                                       │                 └── :page_facing_up:ui_buttons_localizations_data.json<br>
                                       └── :file_folder:UI_Menu_texts<br>
                                                ├── :page_facing_up:ui_\*_menu_text.json **(Can be your menu text file)**<br>
                                                └── :file_folder:Localization<br>
                                                         ├── :page_facing_up:eng.json **(Can be your localization)**<br>
                                                         └── :page_facing_up:ui_menu_texts_localizations_data.json<br>

**Json interface settings files:**<br>

**Example of 'ui_localizations_data.json' file:**
```json
{
  "ui_buttons_files": [
    "ui_exit_menu_buttons",
    "ui_game_menu_buttons",
    "ui_gameplay_buttons"
  ],
  "localizations": [
    "eng",
    "ru"
  ]
}
```
'ui_buttons_files' key is used in the 'Interface_Controller.py' file code.<br>
In 'get_ui_buttons_dict' method of 'InterfaceController' class.<br>

Please note that you need to write file names in ui_buttons_files key values.<br>
Note that localization tags work similarly to scene text localization.

**Example of start menu in './UI_Buttons/\*/eng.json' file:**
```json
{
  "start_menu_new_game": "New game",
  "start_menu_continue": "Continue",
  "start_menu_load": "Load",
  "start_menu_settings": "Settings",
  "start_menu_creators": "Creators",
  "start_menu_exit": "Exit"
}
```
The values of these keys are written as text, on buttons that have text in them.

**Example of buttons in ui\_\*\_buttons.json file:**
```json
{
  "start_menu_new_game": {
    "type": "start_menu",
    "index_number": 0,
    "sprite_name": "game_menu_buttons",
    "font": null,
    "color": "#000000"
  },
  "start_menu_continue": {
    "type": "start_menu",
    "index_number": 1,
    "sprite_name": "game_menu_buttons",
    "font": null,
    "color": "#000000"
  }
}
```
'**index_number**' key contains the horizontal or vertical menu order of button as value.<br>
Numbers can be negative.<br>
Finding the order of the buttons and how it will be described in the 'UI_Button.py' file 'Button' class.<br>
In 'coordinates' method of 'Button' class also uses the '**type**' key value.<br>
If you want to add your own menus, please note that the key values are **hardcoded**.<br>

Please note that the '**sprite_name**' key contains the name of the sprite, as the value.<br>
Sprites must be in **png** format and stored in a 'Buttons' folder.<br>
**Folder location:**<br>
./:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Images<br>
                    └── :file_folder:User_Interface<br>
                            └── :file_folder:Buttons<br>

**Example of 'ui_menu_text_localizations_data.json' file:**
```json
{
  "ui_menus_text_files": [
    "ui_back_to_start_menu_status_menu_text",
    "ui_exit_menu_text",
    "ui_settings_status_text"
  ],
  "localizations": [
    "eng",
    "ru"
  ]
}
```
Arranged by **analogy** with the 'ui_localizations_data.json'.<br>
Only instead of the 'ui_buttons_files' key the 'ui_menus_text_files'.

**Example of text in './UI_Menu_texts/\*/eng.json' file:**
```json
{
  "back_to_start_menu_status_menu_text": "Would you like to return to the main menu?\nAll unsaved progress will be lost!",

  "exit_menu_text": "Would you like to exit the game?\nAll unsaved progress will be lost!",

  "settings_status_menu_text": "Would you like to change the game settings?"
}
```
Note that you can use the line break '\n' character for text.

**Example of 'ui_exit_menu_text.json' file:**
```json
{
  "type": "exit_menu",
  "text": "exit_menu_text",
  "coordinates": {
    "x": 1,
    "y": 1
  },
  "font": null,
  "color": "#FFFFFF",
  "substrate": "blank_big"
}
```
**text** key contains as value link to text in localisation.

**coordinates** key contains as value dictionary with multipliers for the coordinates on which the text will be positioned, from the center.

**color** key contains as value color like string.

Please note that the '**substrate**' key contains the name of the sprite, as the value.<br>
Sprites must be in **png** format and stored in a 'Menu_Substrate' folder.<br>
**Folder location:**<br>
./:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Images<br>
                    └── :file_folder:User_Interface<br>
                            └── :file_folder:Menu_Substrate<br>

**Learn more about coding your own interface:**<br>

**Files locations:**<br>
**./**:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Scripts<br>
                     └── :file_folder:User_Interface<br>
                              ├── :page_facing_up:Interface_Controller.py<br>
                              ├── :page_facing_up:UI_Menu_Text.py<br>
                              ├── :page_facing_up:UI_Button_Factory.py<br>
                              ├── :file_folder:UI_Buttons<br>
                               |       └── :page_facing_up:UI_Base_Button.py<br>
                               |       └── :page_facing_up:UI_*_Button.py **(Can be your button file)**<br>
                              └── :file_folder:UI_Menus<br>
                                       └── :page_facing_up:UI_*_menu.py **(Can be your menu file)**<br>

**Buttons for new menu:**<br>
To create new buttons, in any case, you need to update the collections of the **ButtonFactory** class from 'UI_Button_Factory.py' file.<br>
If you want to use **standard button coordinates**.<br>
Simply update the lists under the **"Interface collections"** comment.<br>
**Example:**
```python
# Interface collections:
yes_no_menus: tuple = (
    'exit_menu',
    'settings_status_menu',
    'back_to_start_menu_status_menu'
)
long_buttons_menus: tuple = (
    'game_menu',
    'settings_menu',
    'start_menu',
    'creators_menu'
)
```
In **this case**, all settings will be applied **automatically**.

If your menu will hase a different way of calculating button positions, then
you need to create a **new button class** and make it inherit from the **BaseButton** abstract class.<br>
You will also need to update the **"button_collections"** dictionary.<br>
**Example:**
```python
# Buttons collection:
button_collections: dict = {
    'yes_no_menus': {
        'button_object': YesNoButton,
        'allowable_menus': yes_no_menus
    },
    'long_buttons_menus': {
        'button_object': LongButton,
        'allowable_menus': long_buttons_menus
    }
}
```
Where is your **"button_object"** key value is your new class.<br>
And **"allowable_menus"** key value is tuple from under **"Interface collections"** comment.

**New menu objects:**<br>
You will need to modify the menus_collection dictionary of '**InputCommandsReactions**' in 'Reactions_to_input_commands.py' file.<br>
Add a new item with menu settings to the dictionary.<br>
**Example:**
```python
menus_collection: dict = {
'exit_menu': {
    'object': ExitMenu(),
    'menu_file': 'ui_exit_menu_buttons',
    'text_file': 'ui_exit_menu_text'
},
'settings_menu': {
    'object': SettingsMenu(),
    'menu_file': 'ui_settings_menu_buttons',
    'text_file': None
}}
```
As a key for your menu collection element will act **"type"** key in your menus json file.<br>
Please note that **None** key is reserved for reading gameplay UI.<br>
In a nested dictionary, the **'object'** key value is your menu object.
If your menu does not have static text, set the value of the '**text_file**' key to 'None'.

You will also need to add your buttons to 'ui_localizations_data.json', and localization.json 'eng.json' as example.<br>
And create and fill a new 'ui_*_menu_buttons.json' file, for your menu.

Finally, you will need to program your menu to work in a new python file.<br>
The 'UI_Start_menu.py' as example.

**Informative text for new menu:**<br>
If you need to add static text, with or without a background, to your new menu then a new menu needs to be added to 'ui_menu_text_localizations_data.json'.<br>
In addition, you will need to create a new ui_*_menu_text.json for the new menu and fill it with correct data.

You will also need to add a new menu to 'UI_Menu_Text.py' **MenuText** class '**scale**' method`s list.<br>
Or you can use the standard coordinates by adding a list for such text at the beginning of the MenuText class.<br>
**Example:**
```python
# Set menu lists:
yes_no_menu_text_list: list[str] = [
    'back_to_start_menu_status_menu',
    'exit_menu',
    'settings_status_menu',
]
back_menu_text_list: list[str] = [
    'creators_menu'
]
```

## The name and icon of the game window:
In order to change the program name, you need to change the value of the variable '**app_name**' in 'Visual_novel_game.py'.<br>
**File location:**<br>
**./**:open_file_folder:Data<br>
   └── :page_facing_up:Visual_novel_game.py

**Example of app_name variable:**
```python
app_name: str = "Visual Novel"
```

In order to change the program window icons, please replace the icon files in the '**Icons**' folder.<br>
Icons images must be in **png** format and have the default size and titles.<br>
**Folder location:**<br>
./:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Images<br>
                    └── :file_folder:User_Interface<br>
                            └── :file_folder:Icons<br>

## GamePlay:
All gameplay code is stored in the folder 'GamePlay'.<br>
If you need to program your gameplay element, add it to the constructor of class '**GamePlayAdministrator**' from 'GamePlay_Administrator.py' file.<br>
'**gameplay_input**' method of this class control of gameplay.

**Files locations:**<br>
**./**:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Scripts<br>
                     └── :file_folder:GamePlay<br>
                              ├── :page_facing_up:GamePlay_Administrator.py<br>
                              └── :page_facing_up:GamePlay_*.py **(Can be your gameplay file)**<br>

## Default game settings:
The default settings are stored in a file **'user_settings'**.<br>
The game reads them at startup and saves them there, with the consent to change by the user, after setting.

**File location:**<br>
./:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :page_facing_up:user_settings<br>

## How the program works:

'Visual_novel_game.py' initializes game and call 'GameMaster' class.<br>
During the initiation process, the script creates the '**SettingsKeeper**' object that is responsible for the game settings.<br>
The **GameMaster** class control game loop and generates lower-level entities that control the gameplay.<br>
* **StageDirector** - Controls the actions on the stage.<br>
Controls who and what will say as well as the appearance of the characters.<br>
Manages the scene background.<br>
Generates a '**Character**', '**Background**' and '**DialoguesWords**' objects used to control staging.
* **SceneValidator** - controls the order of the scenes.<br>
Stores inside itself information about the type of scene with which the StageDirector.
* **InterfaceController** - controls all interface with which the player can interact.<br>
Generates '**Button**' instances with **'ButtonFactory'** and make menus from them.
* **InputCommandsReactions** - catches user commands inside the game and passes them inside the loop to other entities.<br>
Generates '**GamePlayAdministrator**' and all **menus** objects.
* **Render** - renders the image after the calculations.

Simplified: the **InputCommandsReactions** processes user commands.<br>
The **SceneValidator** checks for changes.<br>
The **StageDirector** builds a scene.<br>
**Or** the **InterfaceController** switches menu.

**Files locations:**<br>
**./**:open_file_folder:Data<br>
   ├── :page_facing_up:Visual_novel_game.py<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Scripts<br>
                     ├── :file_folder:Application_layer<br>
                     │        ├── :page_facing_up:Game_Master.py<br>
                     │        ├── :page_facing_up:Reactions_to_input_commands.py<br>
                     │        ├── :page_facing_up:Scene_Validator.py<br>
                     │        ├── :page_facing_up:Settings_Keeper.py<br>
                     │        └── :page_facing_up:Stage_Director.py<br>
                     ├── :file_folder:Game_objects<br>
                     │        ├── :page_facing_up:Background.py<br>
                     │        ├── :page_facing_up:Character.py<br>
                     │        └── :page_facing_up:Dialogues.py<br>
                     ├── :file_folder:GamePlay<br>
                     │        └── :page_facing_up:GamePlay_Administrator.py<br>
                     ├── :file_folder:Render<br>
                     │        └── :page_facing_up:Render.py<br>
                     └── :file_folder:User_Interface<br>
                              ├── :page_facing_up:Interface_Controller.py<br>
                              └── :page_facing_up:UI_Button_Factory.py<br>

Please note that the name of some classes does not correspond to the files where they are contained.<br>
But according to the meaning of the names of the given files, it is still clear where they are.

## Logging:
The program creates a log file and writes messages about critical problems to it.<br>
**File location:**<br>
**./**:open_file_folder:Data<br>
   └── :page_facing_up:logg_file.txt

## Save and Load system:
Game saves are located in the 'Saves' folder.<br>
The game save is a subfolder with a simple json file marked as 'save' format and a png image.<br>
Please note that the subfolder and the save file **must have the same name**.<br>
**Files locations:**<br>
**./**:open_file_folder:Data<br>
   └── :file_folder:Saves<br>
            └── :file_folder:AutoSave<br>
                     ├── :page_facing_up:AutoSave.save<br>
                     └── :framed_picture:screen_preview.png<br>
**Example of 'AutoSave.save' file:**
```json
{
    "scene": "test_scene_03",
    "date": "2023-08-01_19:05:15"
}
```
The **SaveKeeper** class from '**Save_Keeper.py**' file is responsible for working with saves.<br>
**File location:**<br>
**./**:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Scripts<br>
                     └── :file_folder:Application_layer<br>
                              └─── :page_facing_up:Save_Keeper.py<br>

# What needs to be completed:
### Settings Menu:
The **'SettingsKeeper'** class already exists.<br>
It must be used for business logic that will work in the menu.<br>
The **'SettingsMenu'** class and its menu can be used as an external wrapper, or modified.<br>
I planned to use it as a wrapper and make a separate menu for each type of setting.

### Sound system:
At the moment, working with sound in the application is not implemented.

# Known Bugs:

* **Incorrect sRGB profile:**
```text
libpng warning: iCCP: known incorrect sRGB profile
```
Appears due to extra information in the sRGB profile when converting to PNG.<br>
Because of this, after the program ends, a warning message appears in the terminal.<br>
Actually this warning is not an error. I'm just too lazy to re-save the sprite blanks correctly...<br>
Don't be like me and save your sprites correctly!

***

**Thank you** for your interest in my work.<br><br>
