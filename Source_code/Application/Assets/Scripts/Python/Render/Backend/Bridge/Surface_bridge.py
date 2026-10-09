from ..Wrapper import (
    create_surface,
    get_size,
    apply_texture,
    scale_surface
)
from ..Protocol import SurfaceProtocol
"""
Contains code responsible for Surface bridge.
"""


class SurfaceBridge:
    """
    A SurfaceBridge object can be drawn on the screen or on another Surface as a texture during rendering.
    """
    def __init__(
            self,
            *,
            width: int = 0,
            height: int = 0,
            texture_data: dict[str, SurfaceProtocol | tuple[int, int]] | None = None
    ):
        """
        :param width: New Surface pixel width.
                      0 by default.
        :param height: New Surface pixel height.
                      0 by default.
        :param texture_data: A dictionary containing data for creating a surface
                             that already has a texture applied.
                             As example: {
                                "texture": SurfaceProtocol,
                                "coordinates": tuple[int(X), int(Y)]
                             }
                             None by default
        """
        self._instance: SurfaceProtocol = create_surface(
            width=width,
            height=height
        )

        if texture_data:
            self.apply_texture(
                surface=texture_data["texture"],
                coordinates=texture_data["coordinates"]
            )

    def get_size(self) -> tuple[int, int]:
        """
        Calculation low-level Surface x/y size.
        """
        return get_size(
            self._instance
        )

    def scale(
            self, *,
            width: int,
            height: int,
            fast: bool = False
    ):
        """
        Scale Surface to x/y size in pixels.
        :param width: New width(X) size.
        :param height: New height(Y) size.
        :param fast: If True a coarser and faster scaling method will be selected.
        """
        self._instance: SurfaceProtocol = scale_surface(
            surface=self._instance,
            width=width,
            height=height,
            fast=fast
        )

    def apply_texture(
            self, *,
            surface: "SurfaceBridge" | SurfaceProtocol,
            coordinates: tuple[int, int] = (0, 0)
    ):
        """
        Attach texture low-level Surface to another low-level Surface.
        :param surface: Surface object with texture.
        :param coordinates: The x/y coordinates on the Surface from which the texture should be rendered in pixels.
                            As example:
                            (0, 0) ┌────────────────→ X
                                   │
                                   │   ┌──────────┐
                                   │   │          │
                                   │   │          │
                                   │   └──────────┘
                                   │
                                   ↓
                                   Y
        """
        apply_texture(
            texture=
            surface.get_texture()
            if type(surface).__name__ == self.__class__.__name__
            else surface,
            surface=self._instance,
            coordinates=coordinates
        )

    def get_texture(self) -> SurfaceProtocol:
        """
        Get low-level Surface object instance.
        """
        return self._instance
