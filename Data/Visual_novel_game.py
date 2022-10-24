from time import time

from pygame import display, time, QUIT, quit, Surface, SRCALPHA
import pygame.event

from Assets.Scripts.Scene import Background
from Assets.Scripts.Character import Character, characters_generator
from Assets.Scripts.Render import render, character_sprite_size
from Assets.Scripts.Assets_load import image_load, font_load, sound_load
from Assets.Scripts.Director import StageDirector
"""
Contains app shell code.
"""
# Настройки экрана:
screen_size_x = 1920
screen_size_y = 1280

screen = display.set_mode((screen_size_x, screen_size_y))
display.set_caption("Visual Novel")

# Surface settings:
background = Surface((screen_size_x, screen_size_y))
"""
Assets load:
"""
characters_list: dict = characters_generator(background_surface=background)
# Scenes assets:
back_ground_01: Surface = image_load(art_name='scane_name', file_format='png', asset_type='Scenes')
test = {'back_ground_01': back_ground_01}
director = StageDirector(characters=characters_list,
                         protagonist='Name',
                         scenes=test,
                         screen=screen,
                         background=background)
director.set_scene(location='back_ground_01')

"""
MAIN CARUTINE!:
"""
program_running = True
main_cycle_fps_clock = time.Clock()
main_cycle_fps = 20

# # Test---------------
render(screen=screen, background=background, characters_list=characters_list)


while program_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
            program_running = False
    main_cycle_fps_clock.tick(main_cycle_fps)
