import os
import random
import shutil
import ffmpeg
from PIL import Image
from PIL import ImageEnhance
from torchvision import transforms

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


def p_bhd(file_path):
    img = Image.open(file_path).convert('RGB')
    enhancer = ImageEnhance.Contrast(img)
    enhanced_image = enhancer.enhance(0.98)
    enhanced_image.save(file_path)


def tsf_img_random(file_name):
    print('>>> tsf_img')
    frame_dir = os.path.join(g_output, f'{file_name}/frame')
    index = 0
    i = 0
    b = True
    frame_list = os.listdir(frame_dir)
    frame_list.sort(key=lambda x: int(x[:-4]))
    for name in frame_list:
        if index % 35 == 0:
            b = True
            i = random.randint(0, 35 - 1)
        if b and index % 35 == i:
            p_bhd(os.path.abspath(os.path.join(frame_dir, name)))
            b = False
        index += 1


def ob_frame(v1_file_name, v2_file_name):
    v1_frame_dir = os.path.join(g_output, f'{v1_file_name}/frame/')
    v2_frame_dir = os.path.join(g_output, f'{v2_file_name}/frame/')

    v1_frame_list = os.listdir(v1_frame_dir)
    v1_frame_list.sort(key=lambda x: int(x[:-4]))

    v2_frame_list = os.listdir(v2_frame_dir)
    v2_frame_list.sort(key=lambda x: int(x[:-4]))

    p1 = g_video.ob_frame_p1
    p2 = g_video.ob_frame_p2

    for i in range(len(v1_frame_list)):
        if i % p1 < p2:
            continue
        v1_frame_name = v1_frame_list[i]
        v1_frame_file_path = os.path.join(v1_frame_dir, v1_frame_name)

        v2_frame_name = v1_frame_list[i % len(v2_frame_list)]
        v2_frame_file_path = os.path.join(v2_frame_dir, v2_frame_name)
        shutil.copyfile(v2_frame_file_path, v1_frame_file_path)


def merge_output(file_name):
    print('>>> merge_output')
    frame_dir = os.path.join(g_output, f'{file_name}/frame/%d.png')
    audio_path = os.path.join(g_output, f'{file_name}/audio/audio.wav')
    output_file_path = os.path.join(g_output, f'{file_name}.mp4')
    overlay_file_path = os.path.join(g_res, g_video.overlay_file)

    f_in = (ffmpeg.input(frame_dir, framerate=30)
            .filter('scale', size=g_video.size))
    a_in = (ffmpeg.input(audio_path)
            #.filter('atempo', f'{g_video.speed}')
            )
    # overlay_file = (ffmpeg.input(overlay_file_path)
    #                 .filter('colorchannelmixer', aa=g_video.overlay_file_a)
    #                 .filter('scale', size=g_video.size, force_original_aspect_ratio='increase'))

    (ffmpeg
     .concat(f_in, a_in, v=1, a=1)
     #.overlay(overlay_file)
     #.filter('setpts', f'{1/g_video.speed}*PTS')
     .output(output_file_path)
     .run(quiet=not g_debug)
     )


def ob_file(file_path):
    print(f'>>> ob file {file_path}')
    file_name = os.path.basename(file_path).split('.')[0]
    file_name_b = os.path.basename(g_video.video_b).split('.')[0]
    file_path_b = os.path.join(g_res, g_video.video_b)

    input_video = ffmpeg.input(file_path)
    input_video_b = ffmpeg.input(file_path_b)

    split_audio(input_video, file_name)

    split_video_2_img(input_video, file_name)
    split_video_2_img(input_video_b, file_name_b)

    ob_frame(file_name, file_name_b)

    #tsf_img_random(file_name)
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
