# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import shutil
import ffmpeg


def split_audio(video):
    print('>>> split_audio')
    output_dir = '../output/audio'
    os.makedirs(output_dir)
    video.output(f'{output_dir}/audio.wav', start_number=0)\
        .overwrite_output()\
        .run(quiet=True)


def split_video_2_img(video):
    print('>>> split_video_2_img')
    output_dir = '../output/frame'
    os.makedirs(output_dir)
    video.output(f'{output_dir}/%d.jpg', start_number=0)\
        .overwrite_output()\
        .run(quiet=True)


def merge():
    print('>>> merge')
    frame_dir = '../output/frame/%d.jpg'
    audio_path = '../output/audio/audio.wav'
    f_in = ffmpeg.input(frame_dir, framerate=30)
    a_in = ffmpeg.input(audio_path)
    ffmpeg.filter(f_in, filter_name='scale', size='hd720', force_original_aspect_ratio='increase')
    ffmpeg.concat(f_in, a_in, v=1, a=1).output('../output/output.mp4').run(quiet=True)


def ob(file_path):
    print('========== start ==========')
    output_dir = '../output'
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    input_video = ffmpeg.input(file_path, ss=0, r=30)
    split_audio(input_video)
    split_video_2_img(input_video)
    merge()
    print('========== finish ==========')


if __name__ == '__main__':
    ob('../input/v1.mp4')
