from pygame import display, time, QUIT, quit, Surface
import pygame.event

from Assets.Scripts.Render import render
from Assets.Scripts.Stage_Director import StageDirector
"""
Contains app shell code.
"""
# Display settings:
screen_size_x = 1280
screen_size_y = 720
# screen_size_x = 1920
# screen_size_y = 1080
# screen_size_x = 360
# screen_size_y = 120

screen = display.set_mode((screen_size_x, screen_size_y))
display.set_caption("Visual Novel")

"""
Assets load:
"""
# Stage Director settings:
director = StageDirector(screen=screen)

# ------Test
director.set_scene(location='back_ground_01')
#  - Test Render
render(screen=screen,
       background=director.background_surface,
       characters_list=director.characters_dict)
"""
MAIN Coroutine!:
"""
program_running = True
main_cycle_fps_clock = time.Clock()
main_cycle_fps = 20

while program_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
            program_running = False
    main_cycle_fps_clock.tick(main_cycle_fps)
