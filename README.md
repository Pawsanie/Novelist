# Visual Novel
Visual Novel app code.

## Disclaimer:
**Using** some or all of the elements of this code, **You** assume **responsibility for any consequences!**<br/>

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
At the same time, the first scene **must** be called **scene_01**...<br>
And 'past_scene' key of 'scene_01' **must** be **'START'**.<br>
In last scene next_scene key **must* be **'FINISH'**.

**File location:**<br>
./:open_file_folder:Data<br>
   ├── :file_folder:Assets<br>
            ├── :file_folder:Scripts<br>
                     ├── :file_folder:Json_data<br>
                              ├── :page_facing_up:screenplay.json<br>

**Example of one scene in json file:**
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

## Default game settings:
The default settings are stored in a file **'user_settings'**.<br>
The game reads them at startup and saves them there, with the consent to change by the user, after setting.

**File location:**<br>
./:open_file_folder:Data<br>
   ├── :file_folder:Assets<br>
            ├── :page_facing_up:user_settings<br>