import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tempfile
import subprocess

video = '9QGjhPp2Gjs.2'
masks_dir = f'data/masks/{video}'
out_res = (320, 180)


def draw_text(base, label):
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

    # get a font
    fnt = ImageFont.truetype("FreeMono.ttf", 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text((0, 0), label, font=fnt, fill=(255, 32, 32, 192))

    out = Image.alpha_composite(base, txt)
    return out


with tempfile.TemporaryDirectory() as tmpdir:
    start_frame = None
    for mask_file in os.listdir(masks_dir):
        mask_frame = f'{masks_dir}/{mask_file}'
        frame, label = mask_file.split('.')[:2]
        start_frame = int(frame) if start_frame is None else min(start_frame, int(frame))
        input_frame = f'download/stills/{video}/{frame}.jpg'
        out_path = os.path.join(tmpdir, frame + '.jpg')
        with Image.open(mask_frame) as im:
            im = im.resize(out_res)
            im = im.convert(mode='RGBA')
            im = draw_text(im, label)
            mask = np.asarray(im)
        with Image.open(input_frame) as im:
            im = im.resize(out_res)
            im = im.convert(mode='RGBA')
            raw = np.asarray(im)
        output = np.concatenate([raw, mask], axis=1)
        im = Image.fromarray(output)
        im = im.convert(mode='RGB')
        im.save(out_path)
        print(f'wrote {out_path}')
    in_seq = os.path.join(tmpdir, '%04d.jpg')
    proc = subprocess.run(['ffmpeg',
                           '-framerate', '5',
                           '-start_number', '45',
                           '-i', in_seq,
                           '-y',
                           'output.gif'], stdout=subprocess.PIPE)
    if proc.returncode != 0:
        raise ValueError(f'bad return code {proc.returncode}')

