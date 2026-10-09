from .Window_wrapper import (
    create_window,
    screen_clear,
    draw_on_window,
    get_window_size,
    set_window_icon,
    set_window_name
)
from .Surface_wrapper import (
    create_surface,
    get_size,
    apply_texture,
    scale_surface
)
from .Graphics_subsystem_wrapper import screen_flip
"""
Public API for C code wrapper.
"""
