import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tempfile
import subprocess

out_res = (240, 135)


def draw_text(base, label, color=(255, 32, 32, 192)):
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

    # get a font
    fnt = ImageFont.truetype("FreeMono.ttf", 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text((0, 0), label, font=fnt, fill=color)

    out = Image.alpha_composite(base, txt)
    return out


labels = ['dura', 'suction']
videos = [
    ['9QGjhPp2Gjs.2', 45, ['dura', 'suction', 'hook']],
    ['cil034xgU0U.0', 179, ['tumor', 'suction', 'bipolar']],
    ['GJgQgvqRJMU.1', 91, ['avm', 'forceps', 'monopolar']],
]
num_frames = 30
colors = [(128, 64, 255, 128),
          (32, 255, 32, 192),
          (255, 210, 8, 192),
          (192, 32, 255, 192)]
with tempfile.TemporaryDirectory() as tmpdir:
    for i in range(num_frames):
        amalgam = None
        out_path = os.path.join(tmpdir, f'{i:04d}' + '.jpg')
        for j, (video, start, labels) in enumerate(videos):
            frame = i + start
            masks_dir = f'data/masks/{video}'
            input_path = f'download/stills/{video}/{frame:04d}.jpg'
            with Image.open(input_path) as im:
                im = im.resize(out_res)
                im = im.convert(mode='RGBA')
                row = np.asarray(im)
                composite = row.astype(np.float32)
            for label, color in zip(labels, colors):
                label_path = f'data/masks/{video}/{frame:04d}.{label}.jpg'
                if not os.path.exists(label_path):
                    # Use a black image
                    #im = np.multiply(im, color)
                    im = Image.new("RGBA", out_res, (0, 0, 0, 255))
                    im = draw_text(im, label, color)
                    im = np.asarray(im)
                    row = np.concatenate([row, im], axis=1)
                else:
                    with Image.open(label_path) as im:
                        im = im.resize(out_res)
                        im = im.convert(mode='RGBA')
                        im_raw = np.asarray(im)
                        label_px = im_raw.astype(
                            np.float32) * (np.array(color) / 255)
                        #composite = np.add(composite, label_px)
                        composite = np.add(composite, label_px)

                        #im = np.multiply(im, color)
                        im = draw_text(im, label, color)
                        im = np.asarray(im)
                        row = np.concatenate([row, im], axis=1)
            composite = composite.clip(0, 255)
            composite = composite.astype(np.uint8)
            row = np.concatenate([row, composite], axis=1)
            if j < len(videos)-1:
                bar = (np.ones((4, row.shape[1], 4)) * 255).astype(np.uint8)
                row = np.concatenate([row, bar], axis=0)
            #composite = Image.fromarray(composite)
            #composite = draw_text(composite, 'composite', (32, 255, 255, 255))
            #composite = np.asarray(composite)
            amalgam = row if amalgam is None else np.concatenate(
                [amalgam, row], axis=0)
        amalgam = Image.fromarray(amalgam)
        amalgam = amalgam.convert(mode='RGB')
        amalgam.save(out_path)
        print(f'wrote {out_path}')
    in_seq = os.path.join(tmpdir, '%04d.jpg')
    proc = subprocess.run(['ffmpeg',
                           '-framerate', '5',
                           '-start_number', '0',
                           '-i', in_seq,
                           '-y',
                           f'output.gif'], stdout=subprocess.PIPE)
    if proc.returncode != 0:
        raise ValueError(f'bad return code {proc.returncode}')
