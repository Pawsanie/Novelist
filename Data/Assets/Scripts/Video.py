from cv2 import VideoCapture, CAP_PROP_FPS  # IDE can show error but classes are exist.

from Pygame_Visual_Novel.Data.Assets.Scripts.Application_layer.Assets_load import json_load, video_load
"""
Contains the code for working with video files.
"""


class VideoBackground:
    """
    Make backgrounds from video files.
    """
    def __init__(self, *, video_name):
        """
        :param video_name: String name of video file.
        :type video_name: str
        """
        self.video: VideoCapture = VideoCapture(video_load(
            video_name=video_name,
            video_format='mp4'
        ))
        self.video_fps: int = self.video.get(CAP_PROP_FPS)
    ...


def video_generator():
    """
    Generate dictionary with name of videos like key and VideoBackground class as values.
    """
    video_list: dict = json_load([
        'Scripts',
        'Json_data',
        'video_info'
    ])
    result: dict = {}
    for video_name in video_list:
        result.update({video_name: VideoBackground(video_name=video_list[video_name]['footage'])})

    return result
