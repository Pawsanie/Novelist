from pygame import display
"""
Contains code responsible for Render backend API wrapper.
"""


def screen_flip():
    """
    Flip low-level window and render new image.
    """
    display.update()
