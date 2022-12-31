"""
Please edit this file to configure the system
"""

# 0: First camera in the system; 1: Second camera, 2: Third camera, etc.
CAMERA_ID = 0

# EXE file with full path. Note that forward slash (/) must be used instead of backslash (\)
VLC_EXE = "C:/Program Files/VideoLAN/VLC/vlc.exe"

# specify the folder in which JSY video files are located. Video files must be .mp4 files.
# Note that forward slash (/) must be used instead of backslash (\)
# Old: JSY_VIDEO_PATH = "C:/Users/chee-kong.low/PycharmProjects/Bowing/jsy_videos"
JSY_VIDEO_PATH = "C:/Bowing/靜思語動畫" # File names can have chinese characters.
JSY_VIDEO_EXT = ".wmv"

# Specify the filder for backgroung images
JSY_IMAGE_PATH = "C:/Bowing/images"  # Filename must not have chinese characters.

# Specify the filder for backgroung images
JSY_SOUND_PATH = "C:/Bowing/sounds"

# Set to True for production mode to show minimum information. Se to False to show detailed information.
IS_PRODUCTION = False

# Camera resolutions
CAM_WIDTH = 640
CAM_HEIGHT = 480
