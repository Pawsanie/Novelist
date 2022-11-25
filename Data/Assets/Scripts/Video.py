from moviepy.editor import VideoFileClip, preview

from .Assets_load import json_load

# pygame.display.set_caption()


def video_generator():
    video_list: dict = json_load(['Scripts',
                                  'Json_data',
                                  'video_info.json'])
    for video_name in video_list:
        video: VideoFileClip = VideoFileClip(video_list[video_name]['footage'])
#   video.preview()
