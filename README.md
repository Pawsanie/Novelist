# Novelist Engine:

This repository contains the source code to create a Visual Novel game based on minimal edits using Python if it needed.<br/>
And just setting up a few json files.

And also elements of the basic Novelist game engine.

I was inspired to develop this code by the inability to use [RenPy](https://www.renpy.org/) to create a game in the form in which I want.<br>
As well as not wanting to learn RenPy scripting language.

In addition, writing your own game, almost from scratch, is quite interesting.

:warning:Please note that some non-game features are not fully implemented.:warning:

## Disclaimer:
:warning:**Using** some or all of the elements of this code, **You** assume **responsibility for any consequences!**<br>

:warning:The **licenses** for the technologies on which the code **depends** are subject to **change by their authors**.<br><br>

## Contents:
### Required:
Contains information about dependencies and how to install them.
* [Required](#Required)

### Novelist console utilities:
This section describes step by step how to create a game using the engine, at the level of console utilities.<br>
Just like scenes and texture data need to be described, without using any scripting languages, so that the game can be assembled.
* [Screenplay Parser](#Screenplay-Parser)

### Visual Novel game application source code:
The paragraphs in this section describe in sufficient detail how the game is structured and how to control it at the level of the contents of the configuration files.
* [How to run the application](#How-to-run-the-application)
* [Settings of scenes](#Settings-of-scenes)
* [Characters and their sprites](#Characters-and-their-sprites)
* [Backgrounds and its sprite](#Backgrounds-and-its-sprites)
* [User Interface](#User-Interface)
* [Text and Localization](#Text-and-Localization)
* [The name and icon of the game window](#The-name-and-icon-of-the-game-window)
* [GamePlay](#GamePlay)
* [Default game settings](#Default-game-settings)
* [Sound System](#Sound-System)
* [How the program works](#How-the-program-works)
* [Logging](#Logging)
* [Save and Load system](#Save-and-Load-system)

### Other paragraphs:
This section contains information on solving typical problems and plans for further development.
* [What needs to be completed](#What-needs-to-be-completed)
* [Known Problems](#Known-Problems)

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
If you want you can change this library by first downloading it from the repository and installing your version using the command.
```bash
pip install ./path/to/modified/lib
```

# Novelist console utilities:

## Screenplay Parser:

For convenience, this utility is equipped with shell scripts that simplify its call, and a file with an example scene.

**Files location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Utilities<br>
            └── :file_folder:Screenplay_parser<br>
                     ├── :file_folder:Screenplay_source<br>
                     |        └── :page_facing_up:example_scene_config.ini<br>
                     ├── :page_facing_up:Screenplay_Source_Parser.py<br>
                     ├── :page_facing_up:ScreenplaySourceParser_execute.ps1<br>
                     └── :page_facing_up:ScreenplaySourceParser_execute.sh

### How to create scene config:
Let's start with how to design the scene for this script.<br>
An example of the scene is in the 'example_scene_config.ini' file.<br>

In order to create your own scene, you need to create a file with any name and ini extension, and either add it to the '**Screenplay_source folder**'.<br>
Or to any directory in which you want to store your scenes.<br>
You can store several scenes in one file, or just one.

Let's take a closer look at the components of the scene settings:
* **Basic Scene Settings:**
    ```text
    [example_scene_name]
    
    scene_type = reading|choice
    past_scene = scene_name|START
    ```
  * **example_scene_name** - This scene name will be used inside the game.<br>
  It should be written in square brackets.<br>
  And all subsequent rows assigned to this scene must be under this title.
  * **scene_type** - keep gameplay type.<br>
  Can be **reading** or **choice**.
  * **past_scene** - keep name of previous scene.<br>
  This should be a name similar to what you write in square brackets at the beginning of the scene settings.<br>
  For another configured scene - respectively.<br>
  The first scene in your visual novel must have '**START**' written on it.

* **Background:**
    ```text
    background_sprite_sheet = background_01
    background_animation = animation_01
    ```
  * **background_sprite_sheet** - keep background sprite texture image and texture settings file.<br>
  To create a texture you can use "Texture_Source_Parser" utility.
  * **background_animation** - here you need to specify the name of the animation or static frame.

* **Reading scene settings:**
    ```text
    next_scene = scene_name|FINISH
    speaker_name_color = #ffffff
    speech_text_color = #ffffff
    ```
    * **next_scene** - keep name of next scene for reading gameplay.<br>
This should be a name similar to what you write in square brackets at the beginning of the scene settings.<br>
For another configured scene - respectively.<br>
The last scene in your visual novel must have '**FINISH**' written on it.
    * **speaker_name_color** and **speech_text_color** - keeps hex-code the color of the name of the character speaking in the scene and the color of the text that he speaks.<br>
    You don't have to specify colors.<br>
    They will be set to #ffffff by default.

* **Choice scene settings:**
    ```text
    scene_choice.choice_01 = scene_03
    scene_choice.choice_02 = scene_02
    choice_text_color.choice_02 = #ffffff
    ```
  * **scene_choice** - stores the name of the scene to be switched to as a value.<br>
  Please note that in this case the key consists of 2 parts '**scene_choice**' and choice name as example '**choice_01**' and '**choice_02**'.<br>
  This should be a name similar to what you write in square brackets at the beginning of the scene settings.<br>
  For another configured scene - respectively.<br>
  * **choice_text_color** - is designed on the same principle as '**scene_choice**'.<br>
  Keeps hex-code the color of choice text.<br>
  You don't have to specify colors. They will be set to #ffffff by default.

* **Characters settings:**
    ```text
    # Left Character:
    left_character_animation = animation_01
    left_character_sprite_sheet = left_character
    left_character_plan = background_plan|first_plan
    
    # Middle Character:
    middle_character_animation = animation_01
    middle_character_sprite_sheet = middle_character
    middle_character_plan = background_plan|first_plan
    
    # Right Character:
    right_character_animation = animation_01
    right_character_sprite_sheet = right_character
    right_character_plan = background_plan|first_plan
    ```
    You can leave the characters unspecified if you want the scene to remain empty.<br>
    Or you can use one, two or three character type actors on scene.<br>
    At the beginning of each key you need to indicate what type of character you want to describe:<br>
    **left\_**, **middle\_** or **right\_**. As example **right_character_animation**.<br>
    Next, the keys will be listed **without** this **prefix**:
    * **character_sprite_sheet** - keep character sprite texture image and texture settings file.<br>
To create a texture you can use "Texture_Source_Parser" utility.
    * **character_animation** - here you need to specify the name of the animation or static frame.
    * **character_plan** - can only have '**background_plan**' or '**first_plan**' as value.<br>
Obviously, the setting is responsible for how the character will be drawn.<br>
In the foreground or background.

* **Optional scene settings:**
    ```text
    # Special effects can be sent like list as example: "rain,noise_artifacts,snow"...
    scene_special_effects = rain|noise_artifacts|false
    music = music_file|false
    sound = sound_file|false
    voice = voice_file|false
    ```
  * **scene_special_effects** - the option is currently under development.
  * **music** - name of music file or **false**<br>
  This file will play in a loop during this scene
  * **sound** - name of sound file or **false**<br>
  This file plays once per scene, a moment after the switch is made.
  * **voice** - name of voice file or **false**<br>
  This file plays once per scene, a moment after the switch is made.

### How to assemble a game screenplay from scene configurations:
In order to use this utility, you need to call it directly, or through a shell **ScreenplaySourceParser_execute** script that simplifies working with it.<br>
As an argument, you can pass the absolute path to the folder with your scene settings, if it differs from the default one.<br>
As example:
```shell
./ScreenplaySourceParser_execute.sh /home/User/Example_Path
```
If the folder is standard you can simply call the script.
```shell
powershell -File ScreenplaySourceParser_execute.ps1
```
Below is a detailed description of how to run the utility on different operating systems:

* **Windows:**
  * Hold down '**Win**' and '**R**' keys on your keyboard.
  * Enter '**cmd**' in the window that opens and press '**Enter**'.
  * Enter the drive letter where the program was downloaded and '**:**'.<br>
  As example for 'D drive':
  ```shell
  D:
  ```
  * Enter '**cd**' and absolute path to the script through the folder where you downloaded the program.<br>
  As example for downloaded path 'D:\Git\Novelist':
  ```shell
  cd D:\Git\Novelist\Source_code\Utilities\Screenplay_parser
  ```
  * Run "**ScreenplaySourceParser_execute**" powershell script.
  ```shell
  powershell -File ScreenplaySourceParser_execute.ps1
  ```

* **MacOS:**
  * Hold down '**Command**' and '**Space**' keys on your keyboard.
  * Enter '**Terminal**' in the window that opens and press '**Enter**'.
  * Enter '**cd**' and absolute path to the script through the folder where you downloaded the program.<br>
  As example for downloaded path '/home/User/Git/Novelist':
  ```shell
  cd /home/User/Git/Novelist/Source_code/Utilities/Screenplay_parser
  ```
  * Please note that to run a script on Unix-like operating systems, you must first explicitly make it executable with the command:
  ```shell
  chmod +x ./ScreenplaySourceParser_execute.sh
  ```
  * Run "**ScreenplaySourceParser_execute**" Bash script.
  ```shell
  ./ScreenplaySourceParser_execute.sh
  ```

* **Other Unix type OS:** - Ubuntu, Fedora, etc.
  * Open the Terminal of your operating system.
  * Enter '**cd**' and absolute path to the script through the folder where you downloaded the program.<br>
  As example for downloaded path '/home/User/Git/Novelist':
  ```shell
  cd /home/User/Git/Novelist/Source_code/Utilities/Screenplay_parser
  ```
  * Please note that to run a script on Unix-like operating systems, you must first explicitly make it executable with the command:
  ```shell
  chmod +x ./ScreenplaySourceParser_execute.sh
  ```
  * Depending on your security settings, you may need to enter the sudo command.<br>
And enter the password when requested if necessary.
  ```shell
  sudo chmod +x ./ScreenplaySourceParser_execute.sh
  ```
  * Run "**ScreenplaySourceParser_execute**" Bash script.
  ```shell
  ./ScreenplaySourceParser_execute.sh
  ```

# Visual Novel game application source code:

## How to run the application:
To run the application, you need to run the 'Visual_novel_game.py' script with your shell.<br>
**Example of shell command:**<br>
```shell
python -B Visual_novel_game.py
```
**File location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :page_facing_up:Visual_novel_game.py


## Settings of scenes:

### Scene order:
To adjust the scene order, you need to change the json file **'screenplay.json'**.<br>
At the same time, the first scene **must** have the 'past_scene' key value as **'START'**.<br>
In the last scene 'next_scene' key **must** be **'FINISH'**.<br>

**File location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Scripts<br>
                              └── :file_folder:Json_data<br>
                                       └── :page_facing_up:screenplay.json<br>

**Example of screenplay.json file:**
```json
{
  "test_scene_01": {
    "gameplay_type": "reading",
    "background": {
      "background_sprite_sheet": "back_ground_01",
      "background_animation": "default"
    },
    "past_scene": "START",
    "actors": {
      "Character_02": {
        "character_animation": "1",
        "character_plan": "first_plan",
        "character_start_position": "middle"
      },
      "Character_01": {
        "character_animation": "3",
        "character_plan": "background_plan",
        "character_start_position": "right"
      }
    },
    "next_scene": "test_scene_02",
    "speaker_name_color": "#00ffff",
    "speech_text_color": "#ffffff",
    "special_effects": [
      "rain",
      "noise_artifacts"
    ],
    "sounds": {
      "music_channel": false,
      "sound_channel": "blank",
      "voice_channel": false
    }
  },
  "test_scene_02": {
    ...
    "choices": {
      "choice_01": {
        "branching": "test_scene_01",
        "text_color": "#ffffff"
      },
      "choice_02": {
        "branching": false,
        "text_color": "#ff0000"
      },
      "choice_03": {
        "branching": "test_scene_03",
        "text_color": "#ffffff"
      }
    },
    ...
}
```
**Gameplay Type:**<br>
Please note that a '**gameplay_type**' key value must be **reading|choice** strings.<br><br>

**Background:**<br>
The '**background**' key have information about background sprite.<br>
The '**background_sprite_sheet**' key must have backgrounds name keys from 'backgrounds_sprites.json' as a value.<br>
The '**background_animation**' key must have a relevant animation name from background texture json file data.<br>
More about this further in «[Backgrounds and its sprite](#Backgrounds-and-its-sprites)» paragraph.<br><br>

**Past Scene:**<br>
The '**past_scene**' key contains information about the previous scene.<br>
The **first scene** must have the '**START**' key value.<br><br>

**Actors:**<br>
Please note that an **actors** characters keys must match certain values:<br>
**character_animation** - can be any key from the dictionary 'characters_sprites.json'. <br>
More about this further in «[Characters and their sprites](#Characters-and-their-sprites)» paragraph.<br>
**character_plan** - may have values **background_plan|first_plan**.<br>
**character_start_position** - may have values **right|middle|left**.<br><br>

:eye_speech_bubble:**Specific for Reading GamePlay:**<br>
* **Next Scene:**<br>
The '**next_scene**' key value contains information about the next scene to be switched to.<br>
Last scene must have the '**FINISH**' key value.<br>
Please note that this only switches the reading gameplay scene.<br>
As example 'test_scene_01' scene.<br><br>

* **Speaker Name Color:**<br>
The **hex-code** value of the **speaker_name_color** key obviously contains a color setting that will be assigned to the speaker's name while scene rendered.<br><br>

* **Speech Text Color:**<br>
The **hex-code** value of the **speech_text_color** key obviously contains a color setting that will be assigned to the speach text while scene rendered.<br><br>

:speech_balloon:**Specific for Choice GamePlay:**<br>
* **Choices:**<br>
The '**choices**' key value contains links to text localisation as keys.<br>
The '**branching**' work like 'next_scene' key for reading gameplay.<br>
Please note that this only switches the choice gameplay scene.<br>
The '**text_color**' key control color of text on choice button.<br>
As example 'test_scene_02' scene.<br>

More information about reading and choice gameplay text is specified in the «[Text and Localization](#Text-and-Localization)» paragraph.<br><br>

**Special Effects:**<br>
Currently under development.<br><br>

**Sounds:**<br>
The nested dictionary of the **"sounds"** key contains the keys and values of the sound effects and music<br>
that will be played at the start of the scene and will be interrupted at the transition to the next one.<br>
Please note that the keys **"voice_channel"**, **"sound_channel"** and **"music_channel"** can contain either a string with a name, without a file extension, or **false** as values.<br>

## Characters and their sprites:
Information about the characters is stored in a 'characters_sprites.json 'file.<br>
It needs to list the names by which the game will look for characters.<br>
**Please note** that the name specified here is how the key is used in the **actors** key in **'screenplay.json'** file!<br>
And this name is in no way related to the one you can set in the dialogs!<br>
Texture data file name and animations available to the character from this file.<br>
**File location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Scripts<br>
                              └── :file_folder:Json_data<br>
                                       └── :page_facing_up:characters_sprites.json<br>
**Example of 'characters_sprites.json' file:**
```json
{
  "Character_01": {
    "texture": "blank_pink",
    "animations": {
      "1": "animation_1",
      "2": "animation_2",
      "3": "animation_3"
    }
  },
  
  "Character_02": {
    "texture": "blank",
    "animations": {
       "1": "black",
       "2": "pink",
       "3": "blue",
       "4": "green"
    }
  }
}
```
In this case, two options for implementing a character sprite are indicated:<br>
**Character_01** is the character with an animated sprite.<br>
**Character_02** is the character without animations.<br>
The difference is that in the **animation** key for a static sprite, static poses are actually specified, not animations that will be played frame by frame.<br><br>

Regardless of the type of animations the character has.<br>
You must set the **texture** key value to the name of the texture image and the texture storyboard settings.<br>
Please note the names of these two files must match!<br><br>

Let's first discuss the sprite **texture settings sprite sheet files**.<br>
**Files location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Scripts<br>
                              └── :file_folder:Json_data<br>
                                       └── :file_folder:Texture_data<br>
                                                └── :file_folder:Characters<br>
                                                        └── :page_facing_up:*.json **(Can be your sprite sheet json)**<br>

For static sprites, the following settings are typical:<br>
* **sprite_sheet** value is **False**.<br>
* **statick_frames** simply contains the name of the frames with their x|y coordinates.<br>
The coordinates for each frame are specified as the top left corner and the bottom right corner, respectively.<br>

**Example of such a 'statick_sprite_sheet.json' file:**
```json
{
  "sprite_sheet": false,
  "statick_frames": {
     "black": {
       "top_left_corner": {
         "x": 25,
         "y": 49
          },
       "bottom_right_corner": {
         "x": 280,
         "y": 618
       }
     },
     "pink": {
       "top_left_corner": {
         "x": 344,
         "y": 49
          },
       "bottom_right_corner": {
         "x": 568,
         "y": 618
       }
     }
  }
}
```

For animation sprites, the following settings are typical:<br>
* **sprite_sheet** value is **True**.<br>
* **animations** value contains not just frames but settings for each animation.
    * **time_duration** -animation playback time as float.
    * **frames** - list of frames with their x|y coordinates.<br>
    The coordinates for each frame are specified as the top left corner and the bottom right corner, respectively.<br>

**Example of such a 'animation_sprite_sheet.json' file:**
```json
{
  "sprite_sheet": true,
  "animations": {
    "animation_1": {
      "time_duration": 1.0,
      "frames": {
        "1": {
          "top_left_corner": {
            "x": 21,
            "y": 21
          },
          "bottom_right_corner": {
            "x": 342,
            "y": 940
          }
        }
      }
    },

    "animation_2": {
      "time_duration": 1.0,
      "frames":{
        "1": {
          "top_left_corner": {
            "x": 21,
            "y": 1000
          },
          "bottom_right_corner": {
            "x": 342,
            "y": 1919
          }
        }

      }
    }

  }
}
```

Sprite images must be in **png** format and stored in a 'Characters' folder.<br>
**Folder location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Images<br>
                              └── :file_folder:Characters<br>
                                       └── :framed_picture:*.png **(Can be your image file)**<br>

## Backgrounds and its sprites:
Information about the backgrounds and its sprites must be entered into the 'backgrounds_sprites.json' file.<br>
The names that will be given here are used to create scenes in 'screenplay.json' fie.

**File location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Scripts<br>
                              └── :file_folder:Json_data<br>
                                       └── :page_facing_up:backgrounds_sprites.json<br>
**Example of 'backgrounds_sprites.json' file:**
```json
{
  "back_ground_01": {
    "texture": "blank",
    "animation": "default"
  },
  
  "settings_menu": {
    "texture": "blank",
    "animation": "default"
  }
}
```
As you can see from the example, names are also used for game menus.<br>
All menu, except for gameplay, have their background plans.<br>

All settings are similar to the settings described above for the characters.<br>
You also need to specify the path to the file with the settings and the image of the texture.<br>
Their names should also match.<br>
And you also need to set the name of the animation from the settings file.<br>

**Files location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Scripts<br>
                              └── :file_folder:Json_data<br>
                                       └── :Texture_data<br>
                                                └── :file_folder:Backgrounds<br>
                                                         └── :page_facing_up:*.json **(Can be your sprite sheet json)**<br>
**Example of statick background_sprite_sheet_texture_data.json file:**
```json
{
  "sprite_sheet": false,
  "statick_frames": {
     "default": {
       "top_left_corner": {
         "x": 0,
         "y": 0
          },
       "bottom_right_corner": {
         "x": 1916,
         "y": 865
       }
     }
  }
}
```
You can read more about how the texture files are arranged in the «[Characters and their sprites](#Characters-and-their-sprites)» paragraph.<br>

Images must be in **jpg** format and stored in a 'Backgrounds' folder.<br>
**Folder location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Images<br>
                              └── :Backgrounds<br>
                                       └── :framed_picture:*.jpg **(Can be your image file)**<br>

However, you can change the sprite's format requirement by modifying it in the code.

## User Interface:
Information about the standard user interface is contained in 'ui_buttons_data.json' files and 'ui_menu_text_data.json'.<br>
Information about localisation of standard interface in «[Text and Localization](#Text-and-Localization)» paragraph.

**Below** examples with **json`s** describes the code that needs to be changed if you want to supplement the standard menus with your own.

**Files locations:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Scripts<br>
                              └── :file_folder:Json_data<br>
                                       └── :file_folder:User_Interface<br>
                                                 ├── :page_facing_up:ui_sprites.json<br>
                                                 ├── :file_folder:UI_Buttons<br>
                                                 │       ├── :page_facing_up:ui_buttons_data.json<br>
                                                 │       └── :file_folder:Buttons_config_files<br>
                                                 │                └── :page_facing_up:ui_\*\_buttons.json **(Can be your button file)**<br>
                                                 └── :file_folder:UI_Menu_texts<br>
                                                          ├── :page_facing_up:ui_menu_text_data.json<br>
                                                          └── :file_folder:Text_config_files<br>
                                                                   └── :page_facing_up:ui_\*_menu_text.json **(Can be your menu text file)**<br>

**User Interface Buttons:**<br><br>
All button configurations are initially described in the 'ui_buttons_data.json' file.<br>
This file contains an array that lists the names of configuration files for all menu buttons.<br>
**Example of buttons in ui_buttons_data.json file:**
```json
[
    "ui_exit_menu_buttons",
    "ui_game_menu_buttons",
    "ui_gameplay_buttons",
    "ui_load_menu_buttons",
    "ui_save_menu_buttons",
    "ui_settings_menu_buttons",
    "ui_settings_status_buttons",
    "ui_start_menu_buttons",
    "ui_back_to_start_menu_status_menu_buttons",
    "ui_creators_menu_buttons"
]
```

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
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Images<br>
                              └── :file_folder:User_Interface<br>
                                       └── :file_folder:Buttons<br>

The button sprite texture images must be described in the 'ui_sprites.json' file.<br>
**Example of buttons in ui_sprites.json file:**
```json
{
  "Buttons": [
    "dialogues_choice_button",
    "exit_menu_buttons",
    "fast_forward",
    "game_menu",
    "game_menu_buttons",
    "hide_interface",
    "next_scene",
    "past_scene"
  ],

  "Menu_Substrate": [
    "blank_big"
  ],

  "Save_System": [
    "screen_preview_empty"
  ],

  "Text_Canvas": [
    "text_canvas"
  ]
}
```
* **Buttons** - list of textures that can be assigned to buttons.
* **Menu_Substrate** - list of textures on top of which text in the menu can be written.
* **Save_System** - despite the fact that this is an array, there is only one possible texture option for empty save cells.
* **Text_Canvas** - similar but for the text that the player reads during reading gameplay.
They are treated as static images and are loaded as is, meaning each file should contain a complete image of the object.<br>

**User Interface Menu Text:**<br><br>
All text configurations are initially described in the 'ui_menu_text_data.json' file.<br>
This file contains an array that lists the names of configuration files for all menu texts.<br>
**Example of buttons in ui_buttons_data.json file:**
```json
[
    "ui_back_to_start_menu_status_menu_text",
    "ui_exit_menu_text",
    "ui_settings_status_menu_text",
    "ui_creators_menu_text"
]
```

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
* **text** key contains as value link to text in localisation.
* **coordinates** key contains as value dictionary with multipliers for the coordinates on which the text will be positioned, from the center.
* **color** key contains as value color like string.

Please note that the '**substrate**' key contains the name of the sprite, as the value.<br>
Sprites must be in **png** format and stored in a 'Menu_Substrate' folder.<br>
**Folder location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Images<br>
                              └── :file_folder:User_Interface<br>
                                       └── :file_folder:Menu_Substrate<br>

**Learn more about coding your own interface:**<br>

**Files locations:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Scripts<br>
                              └── :file_folder:User_Interface<br>
                                       ├── :page_facing_up:Interface_Controller.py<br>
                                       ├── :page_facing_up:UI_Menu_Text.py<br>
                                       ├── :page_facing_up:UI_Button_Factory.py<br>
                                       ├── :file_folder:UI_Buttons<br>
                                        |       ├── :page_facing_up:UI_Base_Button.py<br>
                                        |       └── :page_facing_up:UI_\*\_Button.py **(Can be your button file)**<br>
                                       └── :file_folder:UI_Menus<br>
                                                └── :page_facing_up:UI_*_menu.py **(Can be your menu file)**<br>

**Buttons for new menu:**<br>
To create new buttons, in any case, you need to update the collections of the **ButtonFactory** class from 'UI_Button_Factory.py' file.<br>
If you want to use **standard button coordinates**.<br>
Simply update the lists under the **"Interface collections"** comment.<br>
**Example:**
```python
# Interface collections:
_yes_no_menus: tuple = (
    'exit_menu',
    'settings_status_menu',
    'back_to_start_menu_status_menu'
)
_long_buttons_menus: tuple = (
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
_button_collections: dict = {
    'yes_no_menus': {
        'button_object': YesNoButton,
        'allowable_menus': _yes_no_menus
    },
    'long_buttons_menus': {
        'button_object': LongButton,
        'allowable_menus': _long_buttons_menus
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
    }
}
```
As a key for your menu collection element will act **"type"** key in your menus json file.<br>
Please note that **None** key is reserved for reading gameplay UI.<br>
In a nested dictionary, the **'object'** key value is your menu object.<br>
If your menu does not have static text, set the value of the '**text_file**' key to 'None'.

You will also need to add your buttons to 'ui_localizations_data.json', and localization.json 'eng.json' as example.<br>
And create and fill a new 'ui_*_menu_buttons.json' file, for your menu.

Finally, you will need to program your menu to work in a new python file.<br>
The 'UI_Start_menu.py' as example.

**Informative text for new menu:**<br>
If you need to add static text, with or without a background, to your new menu then a new menu needs to be added to 'text_menu_localization.csv'.<br>
More information about it «[Text and Localization](#Text-and-Localization)» paragraph.

You will also need to add a new menu to 'UI_Menu_Text.py' **MenuText** class '**scale**' method`s list.<br>
Or you can use the standard coordinates by adding a list for such text at the beginning of the MenuText class.<br>
**Example:**
```python
# Set menu lists:
_yes_no_menu_text_list: list[str] = [
    'back_to_start_menu_status_menu',
    'exit_menu',
    'settings_status_menu',
]
_back_menu_text_list: list[str] = [
    'creators_menu'
]
```

## Text and Localization:

For convenience, all text localizations are made in the form of files with tables in CSV format.<br>
This approach allows you to simply add a column for each new language.<br>
Due to the specific nature of game text, tabulation is used as a separator.<br>
Please pay **attention** to this fact.<br>
This means that you **cannot** use the **Tab** character in any text, names or titles.<br><br>

**Files locations:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Localisation<br>
                              └── :file_folder:Main<br>
                                       ├── :page_facing_up:button_menu_localization.csv<br>
                                       ├── :page_facing_up:screenplay_localization.csv<br>
                                       └── :page_facing_up:text_menu_localization.csv<br>

**Button menu localization:**<br>
Example:

| button_id           | eng      | ru         |
|---------------------|----------|------------|
| start_menu_new_game | New game | Новая игра |
| start_menu_continue | Continue | Продолжить |
| start_menu_load     | Load     | Загрузить  |
| start_menu_settings | Settings | Настройки  |
| start_menu_creators | Creators | Создатели  |
| start_menu_exit     | Exit     | Выйти      |

* **button_id** keep button id from ui_*menu_buttons.json files.<br>
* **eng** and **ru** are examples of string values which will be displayed on the buttons depending on the language settings.<br>

**Screenplay localization:**<br>
Example:

| scene_id      | scene_type | choice_id | eng                     | ru                         |
|---------------|------------|-----------|-------------------------|----------------------------|
| test_scene_01 | reading    | Null      | Test Chan::Hello World! | Тестовая Тян::Привет Мир!  |
| test_scene_02 | choice     | choice_01 | Go to Scene 01          | Перейти к сцене 01         |
| test_scene_02 | choice     | choice_02 | ERROR!                  | ОШИБКА!                    |
| test_scene_02 | choice     | choice_03 | Go to Scene 03          | Перейти к сцене 03         |
| test_scene_03 | reading    | Null      | Test Chan::New Scene!   | Тестовая Тян::Новая Сцена! |

* **scene_id**<br>
Keep the scene names for 'screenplay.json' file.<br>
Please note that the values in this column may be repeated depending on the gameplay.

* **scene_type**<br>
Can have value reading|choice.<br>
Scenes with "**reading**" type have only one line.<br>
Scenes with "**choice**" can have multiple lines.<br>
Their number depends on the number of options to choose from.<br>
It is not recommended to make the selection text too large to avoid bugs.

* **choice_id**<br>
Value can be Null or choice id from 'screenplay.json' file.<br>
**Null** for reading gameplay type scenes. **Choice id** name for choice gameplay scenes.

* **eng** and **ru** are examples of string values which will be displayed on the choice buttons or text canvas depending on the language settings.<br>
Please note the combination of symbols "**::**" in this case is a separator for the name and text that the character says in the **Reading** gameplay type scene.<br>
This means that you **cannot use this combination of characters** in either text or character names for reading gameplay.

**Text menu localization:**<br>
Example:

| text_id                             | eng                                                                            | ru                                                                                |
|-------------------------------------|--------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| back_to_start_menu_status_menu_text | Would you like to return to the main menu?\nAll unsaved progress will be lost! | Вы хотите вернутся в главное меню?\nВесь несохраненный прогресс будет потерян!    |
| exit_menu_text                      | Would you like to exit the game?\nAll unsaved progress will be lost!           | Вы хотите выйти из игры?\nВесь несохраненный прогресс будет потерян!              |
| settings_status_menu_text           | Would you like to change the game settings?                                    | Вы желаете изменить настройки игры?                                               |
| creators_menu_text                  | Character artist - ...\nBackground artist - ...\nProgramming - ...             | Художник по персонажам - ...\nХудожник задних планов- ...\nПрограммирование - ... |

* **text_id** - id for "**text**" key in 'ui_*_menu_text.json' file.
* **eng** and **ru** are examples of string values which will be displayed depending on the language settings.<br>
Please note that the standard line break character "**\n**" is used here and is written together between lines.

## The name and icon of the game window:
In order to change the program name, you need to change the value of the variable '**app_name**' in 'Visual_novel_game.py'.<br>
**File location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :page_facing_up:Visual_novel_game.py

**Example of app_name variable:**
```python
app_name: str = "Visual Novel"
```

In order to change the program window icons, please replace the icon files in the '**Icons**' folder.<br>
Icons images must be in **png** format and have the default size and titles.<br>
**Folder location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Images<br>
                              └── :file_folder:User_Interface<br>
                                       └── :file_folder:Icons<br>

## GamePlay:
All gameplay code is stored in the folder 'GamePlay'.<br>
If you need to program your gameplay element, add it to the constructor of class '**GamePlayAdministrator**' from 'GamePlay_Administrator.py' file.<br>
'**gameplay_input**' method of this class control of gameplay.

**Files locations:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :file_folder:Scripts<br>
                              └── :file_folder:GamePlay<br>
                                       ├── :page_facing_up:GamePlay_Administrator.py<br>
                                       └── :page_facing_up:GamePlay_*.py **(Can be your gameplay file)**<br>

## Default game settings:
The default settings are stored in a file **'user_settings'**.<br>
The game reads them at startup and saves them there, with the consent to change by the user, after setting.

**File location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     └── :page_facing_up:user_settings<br>

## Sound System:
The **SoundDirector** class is responsible for working with sound.<br>
Inside, it works with three audio channels responsible for character speech, music and sound effects.<br>
All sounds and music files **must be** in **MP3** format.<br>
You can read more about installing audio tracks to game scenes in paragraph «[Settings of scenes](#Settings-of-scenes)».<br>

Your sound files should be located in their appropriate directories.<br>
However, there is a condition if you have multiple voice covers.<br>
In this case, you will have to change the value of the **"single_voiceover_language"** attribute in the **Sound_Director** class from **True** to **False**.<br>
After this, you will need to add a sub folder for your voice acting to the **Voice** folder.<br>
And place sound files in it.<br>
When this option is enabled, the audio track select from folder stored in the **"voice_acting_language"** attribute of the **SettingsKeeper** class will be automatically selected.<br>
This attribute can be changed in the settings menu, or in the settings file.<br>
Naturally, this voice acting does not have to be voice localization. But it is important to consider changes in the storage principle when enabling the option.

**Files locations:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :file_folder:Assets<br>
                     ├── :file_folder:Sounds<br>
                      |       ├── :file_folder:Effects<br>
                      |        |       └── :musical_note:\*.mp3 **(Can be your sound file)**<br>
                      |       ├── :file_folder:Music<br>
                      |        |       └── :musical_note:\*.mp3 **(Can be your music file)**<br>
                      |       └── :file_folder:Voice<br>
                      |                ├── :musical_note:\*.mp3 **(Can be your sound file)**<br>
                      |                └── :file_folder:eng **(Optional!!!: Can be your localization folder)**<br>
                      |                        └── :musical_note:\*.mp3 **(Optional!!!:Can be your sound file)**<br>
                     └── :file_folder:Scripts<br>
                              ├── :file_folder:Application_layer<br>
                               |       └── :page_facing_up:Sound_Director.py<br>
                              └── :file_folder:Json_data<br>
                                       └── :page_facing_up:menu_sound_settings.json

To install sounds and music in the menus, you need to modify the "*menu_sound_settings.json*" file.<br>
**Example of menu sound settings.:**<br>
```json
{
  "start_menu": {
    "music_channel": "blank",
    "sound_channel": false
  }
}
```
The values of the sound and music keys must also be either **false** or the **name of the file** located in the corresponding folder.<br>
If you add a sound effect, it will only play once.

## How the program works:

'Visual_novel_game.py' initializes game and call 'GameMaster' class.<br>
During the initiation process, the script creates the '**SettingsKeeper**' object that is responsible for the game settings.<br>
The **GameMaster** class control game loop and generates lower-level entities that control the gameplay.<br>
* **StageDirector** - Controls the actions on the stage.<br>
Controls who and what will say as well as the appearance of the characters.<br>
Manages the scene background.<br>
Generates a '**Character**', '**Background**' and '**DialoguesWords**' objects used to control staging.
* **SoundDirector** - Play music, sound effects and speech for the scene if necessary.
* **SceneValidator** - controls the order of the scenes.<br>
Stores inside itself information about the type of scene with which the StageDirector and the SoundDirector.
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
**./**:open_file_folder:Application<br>
   ├── :page_facing_up:Visual_novel_game.py<br>
   └── :file_folder:Assets<br>
            └── :file_folder:Scripts<br>
                     ├── :file_folder:Application_layer<br>
                     │       ├── :page_facing_up:Game_Master.py<br>
                     │       ├── :page_facing_up:Reactions_to_input_commands.py<br>
                     │       ├── :page_facing_up:Settings_Keeper.py<br>
                     │       ├── :page_facing_up:Sound_Director.py<br>
                     │       └── :page_facing_up:Stage_Director.py<br>
                     ├── :file_folder:Game_objects<br>
                     │       ├── :page_facing_up:Background.py<br>
                     │       ├── :page_facing_up:Character.py<br>
                     │       ├── :page_facing_up:Dialogues.py<br>
                     │       └── :page_facing_up:Scene_Validator.py<br>
                     ├── :file_folder:GamePlay<br>
                     │       └── :page_facing_up:GamePlay_Administrator.py<br>
                     ├── :file_folder:Render<br>
                     │       └── :page_facing_up:Render.py<br>
                     └── :file_folder:User_Interface<br>
                              ├── :page_facing_up:Interface_Controller.py<br>
                              └── :page_facing_up:UI_Button_Factory.py<br>

Please note that the name of some classes does not correspond to the files where they are contained.<br>
But according to the meaning of the names of the given files, it is still clear where they are.

## Logging:
The program creates a log file and writes messages about critical problems to it.<br>
**File location:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
            └── :page_facing_up:logg_file.txt

## Save and Load system:
Game saves are located in the 'Saves' folder.<br>
The game save is a subfolder with a simple json file marked as 'save' format and a png image.<br>
Please note that the subfolder and the save file **must have the same name**.<br>
**Files locations:**<br>
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
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
**./**:open_file_folder:Source_code<br>
   └── :file_folder:Application<br>
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

### Special Effects:
It is planned to create template special effects for display on scenes.

### Console utilities:
* Utility for simplified texture data assembly
* Localisation parser utility
* Utility for compiling games for different operating systems.

# Known Problems:

### Incorrect sRGB profile:
```text
libpng warning: iCCP: known incorrect sRGB profile
```
Appears due to extra information in the sRGB profile when converting to PNG.<br>
Because of this, after the program ends, a warning message appears in the terminal.<br>
Actually this warning is not an error.<br>

To avoid this behavior, resave your sprites using the correct settings.<br>

As an example of resaving in Photoshop:
* Open your **png** image.
* Select the "**file**" in the upper left corner.
* Select the "**save as**" in the drop-down list that appears.
* In the file saving window that opens uncheck the box opposite **ICC Profile: sRGB IEC61966-2.1**
* Resave your png image.

As an example of resaving in Krita:
* Open your **png** image.
* Around the middle of the menu at the top of the program window, select an **image**.
* Select the "**Properties**" in the drop-down list that appears.
* In the menu that opens, select the **Image Color Space**.
* Switch profile to **sRGB-elle-V2-srgbtrс.icc**<br>
Usually it is marked as **Default**.
* Select the "**file**" in the upper left corner.
* Select the "**save as**" in the drop-down list that appears.
* Resave your png image.

There are other solutions to this problem using the operating system terminal and various console utilities.<br>
:warning:**Using** the solutions suggested below, **You** assume **responsibility for any consequences!**:warning:<br>
As an example these [solutions from stackoverflow](https://stackoverflow.com/questions/22745076/libpng-warning-iccp-known-incorrect-srgb-profile/22747902#22747902).

### Problems installing Python on Windows:

When installing Python from the official website, you may encounter the fact that the operating system or IDE cannot find it.<br>
There are several ways to solve this problem:
* The easiest way to fix this problem is to install Python using the Microsoft Store.<br>
You can find a program that gives access to it directly on your PC using Windows search.
* Try to **reinstall** Python and select the checkbox "**Add Python to environment variables**".
* Add Python to your operating system's environment variables manually.

***

:hearts: **Thank you** for your interest in my work! :hearts:<br><br>
