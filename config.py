import configparser


class VideoConfig:
    def __init__(self):
        self.frame = 30
        self.size = 'hd720'
        self.overlay_file = ''
        self.overlay_file_a = 0.1
        self.speed = 1


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
        self.video.speed = config.getfloat('video', 'speed')

        self.audio.ar = config.get('audio', 'ar')

