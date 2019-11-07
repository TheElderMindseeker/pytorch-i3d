# pylint: disable=invalid-name,missing-docstring
import os
import subprocess
import urllib.parse

result_path = '/home/daniil/Documents/Projects/University/Thesis/frames'
if not os.path.exists(result_path):
    os.mkdir(result_path)

with open('definition.txt', 'r') as videos, open('err.log', 'w') as err_log:
    for video_path in videos:
        video_path = video_path.strip()
        if not video_path:
            continue

        print(f'Start working on {os.path.abspath(video_path)}')
        video_name, video_ext = os.path.splitext(os.path.basename(video_path))
        video_name = urllib.parse.unquote(video_name)
        frames_dir = os.path.join(result_path, video_name)
        if not os.path.exists(frames_dir):
            os.mkdir(frames_dir)
        else:
            print(f'Folder name clash: {video_name}')
            continue

        command = ('ffmpeg', '-i', os.path.abspath(video_path),
                   os.path.join(frames_dir, f'{video_name}-%06d.jpg'),
                   '-hide_banner', '-threads', '16')
        try:
            subprocess.check_call(command,
                                  stdout=subprocess.DEVNULL,
                                  stderr=err_log)
        except subprocess.CalledProcessError as exc:
            print(f'ffmpeg failed with return code {exc.returncode}')
