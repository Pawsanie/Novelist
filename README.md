# Visual Novel app code:
This repository contains the source code to create a Visual Novel game based on minimal edits using Python if it needed.<br/>
And just setting up a few jason files.

I was inspired to develop this code by the inability to use [RenPy](https://www.renpy.org/) to create a game in the form in which I want.<br>
As well as not wanting to learn RenPy scripting language.

In addition, writing your own game, almost from scratch, is quite interesting.

## Disclaimer:
**Using** some or all of the elements of this code, **You** assume **responsibility for any consequences!**<br>

The **licenses** for the technologies on which the code **depends** are subject to **change by their authors**.<br><br>

___
<br>

## Required:
The application code is written in python and obviously depends on it.<br>
**Python** version 3.6 [Python Software Foundation License / (with) Zero-Clause BSD license (after 3.8.6 version Python)]:
* [Python GitHub](https://github.com/python)
* [Python internet page](https://www.python.org/)

## Required Packages:
**PyGame** [GNU LGPL version 2.1]:
* [PyGame GitHub](https://github.com/pygame/pygame)
* [Pygame internet page](https://www.pygame.org/news)

Used to create windows, surfaces and draw them on top of each other.<br>
Also for flipping the screen and drawing the window icon.

**OpenCV** [3-clause BSD / Apache 2 (after 4.5 version OpenCV)]:
* [OpenCV GitHub](https://github.com/opencv/opencv)
* [OpenCV internet page](https://opencv.org/)

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
And 'past_scene' key of 'scene_01' **must** be **'START'**.<br>
In last scene next_scene key **must** be **'FINISH'**.

**File location:**<br>
./:open_file_folder:Data<br>
   ├── :file_folder:Assets<br>
            ├── :file_folder:Scripts<br>
                     ├── :file_folder:Json_data<br>
                              ├── :page_facing_up:screenplay.json<br>

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
      "past_scene": "START",
      "next_scene": "scene_02"
   }
}
```
In this case, the keys indicate which scene was before 'scene_01' and which should be after (scene_02).<br>
Scenes 'START' or 'FINISH' do not exist.<br>
But the game focuses on its flags.

### Dialogues:
Game dialogues have to be writen in **lang_tag.json** file... **eng.json** as example...<br>
And this tag must be writen in **dialogues_localizations_data.json** file.<br>
You need to name localization language tags for translation in the game settings.

**Files location:**<br>
**./**:open_file_folder:Data<br>
   ├── :file_folder:Assets<br>
            ├── :file_folder:Scripts<br>
                     ├── :file_folder:Json_data<br>
                              ├── :file_folder:Dialogues<br>
                                       ├── :page_facing_up:eng.json **(Can be your localization)**<br>
                                       ├── :page_facing_up:dialogues_localizations_data.json<br>

**Example of one scene in 'eng.json' file:**
```json
{
   "scene_01": {
      "who": [
         "Test Character",
         "#00ffff"
      ],
      "what": [
         "Hello World!",
         "#ffffff"
      ]
   }
}
```
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
   ├── :file_folder:Assets<br>
            ├── :file_folder:Scripts<br>
                     ├── :file_folder:Json_data<br>
                              ├── :page_facing_up:characters_sprites.json<br>
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
   ├── :file_folder:Assets<br>
            ├── :file_folder:Images<br>
            ├── :file_folder:Characters<br>

## Backgrounds ands its sprites:
Information about the backgrounds and its sprites must be entered into the 'backgrounds_sprites.json' file.<br>
The names that will be given here are used to create scenes in 'screenplay.json' fie.

**File location:**<br>
**./**:open_file_folder:Data<br>
   ├── :file_folder:Assets<br>
            ├── :file_folder:Scripts<br>
                     ├── :file_folder:Json_data<br>
                              ├── :page_facing_up:backgrounds_sprites.json<br>
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
   ├── :file_folder:Assets<br>
            ├── :file_folder:Images<br>
            ├── :file_folder:Backgrounds<br>

However, you can change the sprite's format requirement by modifying it in the code.

## Default game settings:
The default settings are stored in a file **'user_settings'**.<br>
The game reads them at startup and saves them there, with the consent to change by the user, after setting.

**File location:**<br>
./:open_file_folder:Data<br>
   ├── :file_folder:Assets<br>
            ├── :page_facing_up:user_settings<br>

***

**Thank you** for your interest in my work.<br><br>