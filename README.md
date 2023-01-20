# Visual Novel app code:
This repository contains the source code to create a Visual Novel game based on minimal edits using Python if it needed.<br/>
And just setting up a few jason files.

I was inspired to develop this code by the inability to use [RenPy](https://www.renpy.org/) to create a game in the form in which I want.<br>
As well as not wanting to learn RenPy scripting language.

In addition, writing your own game, almost from scratch, is quite interesting.

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

**OpenCV** [3-clause BSD / Apache 2 (after 4.5 version OpenCV)]:
* :octocat:[OpenCV GitHub](https://github.com/opencv/opencv)
* :bookmark_tabs:[OpenCV internet page](https://opencv.org/)

Used to cut video into frames and determine the number of frames in the video.

## Installing the Required Packages:
```bash
pip install pygame
pip install opencv-python
```

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
Please note that a **actors** characters keys must match certain values:<br>
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
Scenes with '**false**' keys can be omitted.<br>
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
And this name is in no way related to the one you can set in the dialogs!
As example 'eng.json' file from 'Dialogues' folder.

Sprites must be in **png** format and stored in a 'Characters' folder.<br>
**Folder location:**<br>
./:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Images<br>
                    └── :file_folder:Characters<br>

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
                              ├── :file_folder:UI<br>
                              ├── :page_facing_up:ui_\*_buttons.json **(Can be your button file)**<br>
                              └── :file_folder:Localization<br>
                                       └── :file_folder:Localization<br>
                                                ├── :page_facing_up:eng.json **(Can be your localization)**<br>
                                                └── :page_facing_up:ui_localizations_data.json<br>

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

**Example of start menu in 'eng.json' file:**
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
                    └── :file_folder:UI<br>
                            └── :file_folder:Buttons<br>

**Learn more about coding your own interface:**<br>

**Files locations:**<br>
**./**:open_file_folder:Data<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Scripts<br>
                     └── :file_folder:User_Interface<br>
                              ├── :page_facing_up:Interface_Controller.py<br>
                              ├── :page_facing_up:UI_Button.py<br>
                              ├── :page_facing_up:UI_buttons_calculations.py<br>
                              └── :page_facing_up:UI_*_menu.py **(Can be your menu file)**<br>

New menu need to be added in '**coordinates**' method of '**Button**' class in 'UI_Button.py' file.<br>
Also you need to **write a new method** finding button coordinates.<br>
'menu_yes_no_coordinates' method as example of **horizontal** menu.<br>
And 'menu_start_and_settings_coordinates' as example of **vertical** menu.

New menu buttons need to be added in 'UI_buttons_calculations.py **button_size** function.'

You will need to modify the class constructor of '**InterfaceController**' in 'Interface_Controller.py' file.<br>
Add new menu class like variable to it.
And add new 'return' to '**get_ui_buttons_dict**' in method of 'InterfaceController' class.

You will also need to add your buttons to 'ui_localizations_data.json', and localization.json 'eng.json' as example.<br>
And create and fill a new 'ui_*_menu_buttons.json' file, for your menu.

Finally, you will need to program your menu to work in a new python file.<br>
The 'UI_Start_menu.py' as example.

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
                    └── :file_folder:UI<br>
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
Generates '**Button**' instances and make menus from them.
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
                     ├── :file_folder:GamePlay<br>
                     │        └── :page_facing_up:GamePlay_Administrator.py<br>
                     ├── :file_folder:User_Interface<br>
                     │        ├── :page_facing_up:Interface_Controller.py<br>
                     │        └── :page_facing_up:UI_Button.py<br>
                     ├── :page_facing_up:Background.py<br>
                     ├── :page_facing_up:Character.py<br>
                     ├── :page_facing_up:Dialogues.py<br>
                     ├── :page_facing_up:Game_Master.py<br>
                     ├── :page_facing_up:Reactions_to_input_commands.py<br>
                     ├── :page_facing_up:Render.py<br>
                     ├── :page_facing_up:Scene_Validator.py<br>
                     ├── :page_facing_up:Settings_Keeper.py<br>
                     └── :page_facing_up:Stage_Director.py

Please note that the name of some classes does not correspond to the files where they are contained.<br>
But according to the meaning of the names of the given files, it is still clear where they are.

***

**Thank you** for your interest in my work.<br><br>