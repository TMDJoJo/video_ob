import os
import shutil
import ffmpeg


g_res = 'res'
g_output = 'output'
g_video = None
g_audio = None
g_debug = False


def split_audio(video, file_name):
    print('>>> split_audio')
    output_dir = os.path.join(g_output, f'{file_name}/audio')
    os.makedirs(output_dir)
    (ffmpeg
     .output(video, f'{output_dir}/audio.wav', start_number=0, ar=g_audio.ar)
     .overwrite_output()
     .run(quiet=True)
     )


def split_video_2_img(video, file_name):
    print('>>> split_video_2_img')
    output_dir = os.path.join(g_output, f'{file_name}/frame')
    os.makedirs(output_dir)
    video.output(f'{output_dir}/%d.png', start_number=0)\
        .overwrite_output()\
        .run(quiet=True)


def merge_output(file_name):
    print('>>> merge_output')
    frame_dir = os.path.join(g_output, f'{file_name}/frame/%d.png')
    audio_path = os.path.join(g_output, f'{file_name}/audio/audio.wav')
    output_file_path = os.path.join(g_output, f'{file_name}.mp4')
    overlay_file_path = os.path.join(g_res, g_video.overlay_file)

    f_in = (ffmpeg.input(frame_dir, framerate=30)
            .filter('scale', size=g_video.size, force_original_aspect_ratio='increase'))
    a_in = ffmpeg.input(audio_path)
    overlay_file = (ffmpeg.input(overlay_file_path)
                    .filter('colorchannelmixer', aa=g_video.overlay_file_a)
                    .filter('scale', size=g_video.size, force_original_aspect_ratio='increase'))

    (ffmpeg
     .concat(f_in, a_in, v=1, a=1)
     .overlay(overlay_file)
     .output(output_file_path)
     .run(quiet=not g_debug)
     )


def ob_file(file_path):
    print(f'>>> ob file {file_path}')
    file_name = os.path.basename(file_path).split('.')[0]
    input_video = ffmpeg.input(file_path)
    split_audio(input_video, file_name)
    split_video_2_img(input_video, file_name)
    merge_output(file_name)


def ob(file_path_array, res_dir, output_dir, video_config, audio_config):
    print('========== start ==========')
    global g_res, g_output, g_video, g_audio
    g_res = res_dir
    g_output = output_dir
    g_video = video_config
    g_audio = audio_config
    if os.path.isdir(g_output):
        shutil.rmtree(g_output)
    os.makedirs(g_output)

    for file_path in file_path_array:
        ob_file(file_path)

    print('========== finish ==========')
