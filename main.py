import os
import config
import video_ob

CONFIG_FILE_PATH = './config.ini'


def is_input_file(path):
    return path.endswith('.mp4')


def read_config():
    ini = config.Config()
    ini.read_config(CONFIG_FILE_PATH)
    return ini


def main():
    ini_config = read_config()
    files = []
    for it in os.scandir(ini_config.input):
        if it.is_file() and is_input_file(it.path):
            files.append(os.path.abspath(it.path))

    video_ob.ob(files, ini_config.res, ini_config.output, ini_config.video, ini_config.audio)


if __name__ == '__main__':
    main()
