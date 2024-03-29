import argparse
import json
import youtube_dl
from youtube_dl.utils import DownloadError
import os
import sys
from vpn import vpns, get_vpn

parser = argparse.ArgumentParser(
    description='raw video downloader')
parser.add_argument('--input',  '-i',
                    dest="input",
                    metavar='INPUT',
                    help='path to text file containing youtube video IDs, with optional slice times',
                    default='data/videos.txt')
parser.add_argument('--output', '-o',
                    dest="output",
                    metavar='OUTPUT',
                    help='output file path',
                    default='download/compiled.json')
parser.add_argument('--download',
                    dest="download",
                    metavar='DOWNLOAD',
                    help='download videos if true',
                    default=False)
parser.add_argument('--cache_dir',
                    dest="cache_dir",
                    metavar='CACHE_DIR',
                    help='video download path',
                    default='download/cache')
parser.add_argument('--clean',
                    dest="clean",
                    metavar='CLEAN',
                    help='remove missing videos from output records (do not download)',
                    default=False)
parser.add_argument('--vpn',
                    dest="vpn",
                    metavar='VPN',
                    help=f'name of vpn driver (options are {vpns.keys()})',
                    default=None)
args = parser.parse_args()

if args.vpn != None:
    print(f'Using {args.vpn}')
    vpn = get_vpn(args.vpn)
else:
    print('Warning: not using VPN. You are likely '
          'to be blocked by YouTube at some point.')
    vpn = None

if not os.path.exists(args.cache_dir):
    os.makedirs(args.cache_dir)

completed = []
videos = []

completed_path = os.path.join(os.path.dirname(args.output), '.completed.txt')

try:
    with open(completed_path) as f:
        completed = json.loads(f.read())
except:
    pass

if os.path.exists(args.output):
    with open(args.output) as f:
        videos = json.loads(f.read())


def write_completed():
    dir = os.path.dirname(completed_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(completed_path, 'w') as f:
        f.write(json.dumps(completed))


def write_videos():
    dir = os.path.dirname(args.output)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(args.output, 'w') as f:
        f.write(json.dumps(videos))


def process_video(video, ydl, download):
    videos.append({
        k: video[k] for k in ['id',
                              'ext',
                              'vcodec',
                              'uploader_id',
                              'channel_id',
                              'duration',
                              'width',
                              'height',
                              'fps']
    })
    id = video['id']
    path = os.path.join(args.cache_dir, id + '.mp4')
    if os.path.exists(path):
        print(f'{id} already downloaded')
    elif download:
        ydl.extract_info(
            f'https://youtube.com/watch?v={id}',
            download=True,
        )


if args.clean:
    new_videos = [video
                  for video in videos
                  if os.path.exists(os.path.join(args.cache_dir,
                                                 video['id'] + '.mp4'))]
    print(f'Removed {len(videos)-len(new_videos)} videos')
    videos = new_videos
    write_videos()
    sys.exit(0)

with open(args.input, "r") as f:
    lines = []
    for line in f:
        line = line.strip().split(',')[0]
        if line == '' or line.startswith('#'):
            # Comment or blank line
            continue
        lines.append(line)

with youtube_dl.YoutubeDL({
    'verbose': True,
    'outtmpl': args.cache_dir + '/%(id)s.%(ext)s',
}) as ydl:
    for line in lines:
        if line in completed:
            print(f'Skipping {line}')
            continue
        retry = True
        while retry:
            retry = False
            try:
                result = ydl.extract_info(
                    line,
                    download=False,
                )
                if 'entries' in result:
                    # It is a playlist
                    for video in result['entries']:
                        process_video(video, ydl, args.download)
                else:
                    # Just a single video
                    process_video(result, ydl, args.download)
            except:
                print(f'Caught exception: {sys.exc_info()}')
                if sys.exc_info()[0] is DownloadError and vpn != None:
                    vpn.reconnect()
                    print(f'Retrying {line}')
                    retry = True
                    continue
                else:
                    raise
        write_videos()
        completed.append(line)
        write_completed()
