import configparser


class VideoConfig:
    def __init__(self):
        self.frame = 30
        self.size = 'hd720'
        self.overlay_file = ''
        self.overlay_file_a = 1
        self.video_b=''
        self.speed = 1
        self.ob_frame_p1 = 6
        self.ob_frame_p2 = 4
        self.ob_frame_p3 = 12


class AudioConfig:
    def __init__(self):
        self.ar = '64k'


class Config:
    def __init__(self):
        self.input = ''
        self.output = ''
        self.res = ''
        self.video = VideoConfig()
        self.audio = AudioConfig()

    def read_config(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        self.input = config.get('base', 'input')
        self.output = config.get('base', 'output')
        self.res = config.get('base', 'res')

        self.video.frame = config.getint('video', 'frame')
        self.video.size = config.get('video', 'size')
        self.video.overlay_file = config.get('video', 'overlay')
        self.video.overlay_file_a = config.getfloat('video', 'overlay_a')
        self.video.video_b = config.get('video', 'video_b')
        self.video.speed = config.getfloat('video', 'speed')
        self.video.ob_frame_p1 = config.getint('video', 'ob_frame_p1')
        self.video.ob_frame_p2 = config.getint('video', 'ob_frame_p2')
        self.video.ob_frame_p3 = config.getint('video', 'ob_frame_p3')

        self.audio.ar = config.get('audio', 'ar')

