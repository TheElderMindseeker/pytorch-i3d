import os
import json
import random
import subprocess
import urllib.parse

with open('folders.txt', 'r') as fold_file:
    class_paths = [line.strip() for line in fold_file if line.strip()]

classes = dict()

for idx, class_path in enumerate(class_paths):
    class_name = os.path.basename(class_path)
    for root, _, filenames in os.walk(class_path):
        for filename, ext in map(os.path.splitext, filenames):
            if ext != '.mp4':
                continue
            filename_q = urllib.parse.unquote(filename)
            if filename_q not in classes:
                duration = str(subprocess.check_output(
                    ('ffprobe', '-v', 'error', '-show_entries',
                     'format=duration', '-of',
                     'default=noprint_wrappers=1:nokey=1',
                     os.path.join(root, filename + ext))),
                               encoding='utf-8').strip()
                classes[filename_q] = {
                    'subset':
                    'training' if random.random() < 0.8 else 'testing',
                    'duration': float(duration),
                    'actions': [[idx, 0, float(duration)]]
                }

print(json.dumps(classes, indent=2))
