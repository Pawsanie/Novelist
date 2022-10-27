from pygame import display, time, QUIT, quit
import pygame.event

from Assets.Scripts.Gameplay import gameplay_stage_director_initialization as gameplay
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

#   - Test game:
gameplay(display_screen=screen)
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
