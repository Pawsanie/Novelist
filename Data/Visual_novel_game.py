from time import time

from pygame import display, time, QUIT, quit, Surface, SRCALPHA
import pygame.event

from Assets.Scripts.Scene import Background
from Assets.Scripts.Character import Character, characters_generator
from Assets.Scripts.Render import render, character_sprite_size
from Assets.Scripts.Assets_load import image_load, font_load, sound_load
"""
Contains app shell code.
"""
# Настройки экрана:
screen_size_x = 1920
screen_size_y = 1200
screen = display.set_mode((screen_size_x, screen_size_y))
display.set_caption("Visual Novel")

# Surface settings:
background = Surface((screen_size_x, screen_size_y))
"""
Assets load:
"""
# Characters assets:
test_chan: Surface = image_load(art_name='tyan2', file_format='png', asset_type='Characters')
test_chan2: Surface = image_load(art_name='tyan2', file_format='png', asset_type='Characters')
# Generate characters:
characters_list: tuple = (
    test_chan,
    test_chan2,
                         )
characters_list: dict = characters_generator(characters_list=characters_list,
                                             background_surface=background)
# Scenes assets:
back_ground_01: Surface = image_load(art_name='scane_name', file_format='png', asset_type='Scenes')

# Настройка диалогового окна:
# text_canvas: Surface = Surface((screen_size_x, screen_size_y // 5))
# text_canvas.set_alpha(128)


"""
MAIN CARUTINE!:
"""
program_running = True
main_cycle_fps_clock = time.Clock()
main_cycle_fps = 20

# Test---------------
Background(surface=background, scene_image=back_ground_01)
# Character(surface=character_left, character_image=test_chan, character_size=character_size)
render(screen=screen, background=background, characters_list=characters_list)
time.wait(100)

while program_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
            program_running = False
    main_cycle_fps_clock.tick(main_cycle_fps)
