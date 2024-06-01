import argparse
import os
import glob
from PIL import Image

print("trimming version.0.2019.05.15.1000\n")

params = {}
params['extension'] = "png"
params['suffix'] = "_crop"

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--extension', default='png')
parser.add_argument('-s', '--suffix', default='_crop')
parser.add_argument('target_path')
parser.add_argument('x', type=int)
parser.add_argument('y', type=int)
parser.add_argument('width', type=int)
parser.add_argument('height', type=int)
args = parser.parse_args()

if len(vars(args)) != 7:
    print("usage: triming [options] <target_path> <x> <y> <width> <height>")
    print(" target_path: target path")
    print(" x: x")
    print(" y: x")
    print(" width: width")
    print(" height: height")
    print(" [options] -e : extension. default is 'png'")
    print("           -s : suffix. default is '_crop'")
    exit()

params['target_path'] = args.target_path
params['x'] = args.x
params['y'] = args.y
params['width'] = args.width
params['height'] = args.height

def split_path(filepath):
    path, filename = os.path.split(filepath)
    file, extension = os.path.splitext(filename)
    return {'path': path, 'file': file, 'extension': extension}

crop_param = (params['x'], params['y'], params['width'], params['height'])
print(crop_param)

try:
    for image_file in glob.glob(f"{params['target_path']}/**/*.{params['extension']}", recursive=True):
        if params['suffix'] in image_file:
            continue
        print(image_file)
        image = Image.open(image_file)
        cropped_image = image.crop(crop_param)
        spath = split_path(image_file)
        outpath = f"{spath['path']}/{spath['file']}{params['suffix']}{spath['extension']}"
        cropped_image.save(outpath)
    print('complete.')
except Exception as err:
    print(err)
    exit()
