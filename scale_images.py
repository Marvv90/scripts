import os
import argparse
import cv2
import textwrap

from pathlib import Path
from argparse import ArgumentParser

parser = ArgumentParser(description=textwrap.dedent('''\
        Scale Images
    '''
    ))

parser.add_argument(
    '--path',
    type=str,
    help='Working Path (Default: %(default)s)',
    default=Path.cwd())

parser.add_argument(
    '--read',
    action=argparse.BooleanOptionalAction,
    type=bool,
    help='Output only the Resolution of Images',
    default=False)

parser.add_argument(
    '--extension',
    type=str,
    nargs='+',
    help='Image Extensions (Default: %(default)s)',
    default=['jpg', 'jpeg', 'png'])

parser.add_argument(
    '--exclude',
    type=str,
    nargs='+',
    help='Directorys to Exclude',
    default=())

parser.add_argument(
    '--width',
    type=int,
    help='New Width of the Images')

parser.add_argument(
    '--height',
    type=int,
    help='New Height of the Images')

def start():
    file_list = find_files(args.path)
    
    if not args.read:
        if (args.height or args.width) and len(file_list):
            scale(file_list)
        else:
            if not len(file_list):
                print('No Images found')
            else:
                print('Please set Width or Height')
    else:
        read_resolution(file_list)



def find_files(path):
    file_list = []

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in args.exclude]
        for file_name in files:
            if file_name.lower().endswith(tuple(args.extension)):
                file_list.append(os.path.join(root, file_name))

    return file_list
 
def scale(files):
    for index, file in enumerate(files):
        img = cv2.imread(file)

        height, width, _ = img.shape
        aspect_ratio = width / height

        if args.height:
            new_height = args.height
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = args.width
            new_height = int(new_width / aspect_ratio)

        resize_image = cv2.resize(img, (new_width, new_height))

        cv2.imwrite(file, resize_image)

        print(f'{index+1}/{len(files)} Resized: {file}')

def read_resolution(files):
    for index, file in enumerate(files):
        img = cv2.imread(file)
        
        height, width, _ = img.shape
        format = get_image_format(trunc(width/height))

        print(f'{index+1}/{len(files)} {file} - Resolution: {width}x{height} - Format: {format}')

def trunc(f):
    return int(f * 10 ** 2) / 10 ** 2

def get_image_format(resolution):
    if resolution == trunc(1/1):
        return '1:1'
    elif resolution == trunc(3/2):
        return '3:2'
    elif resolution == trunc(4/3):
        return '4:3'
    elif resolution == trunc(16/9):
        return '16:9'
    else: 
        return 'Unbekanntes Format'

if __name__ == '__main__':
    args = parser.parse_args()
    start()