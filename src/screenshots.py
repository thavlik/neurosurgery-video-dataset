import os
from util import run_cmd


vids = [
    '9QGjhPp2Gjs.2',
    'cil034xgU0U.0',
    'GJgQgvqRJMU.1',
]
for vid in vids:
    input = f'download/processed/{vid}.mp4'
    print(f'extracting frames from {input}')
    dir = f'download/stills/{vid}'
    try:
        os.removedirs(dir)
    except:
        pass
    try:
        os.makedirs(dir)
    except:
        pass
    cmd = f'ffmpeg -i {input} -r 1 -f image2 {dir}/%04d.jpg'
    run_cmd(cmd)
