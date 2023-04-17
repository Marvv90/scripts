import os
import logging
import textwrap
import argparse

from PIL import Image
from pathlib import Path
from argparse import ArgumentParser

parser = ArgumentParser(description=textwrap.dedent('''\
        Konvertiere Bilder zu Webp
    '''
    ))

parser.add_argument(
    '--exclude',
    type=str,
    nargs='+',
    help='Directorys to Exclude',
    default=())

parser.add_argument(
    '--extension',
    type=str,
    nargs='+',
    help='Image Extensions (Default: %(default)s)',
    default=['jpg', 'jpeg', 'png'])

parser.add_argument(
    '--path',
    type=str,
    help='The working Path (Default: %(default)s)',
    default=Path.cwd())

parser.add_argument(
    '--output',
    type=bool,
    action=argparse.BooleanOptionalAction,
    help="Write the Image Name in Logfile",
    default=True)

parser.add_argument(
    '--replace',
    type=bool,
    action=argparse.BooleanOptionalAction,
    help="Replace Old Images with new Converted Images",
    default=True)

def start():
    if args.output:
        logging.basicConfig(filename='{}/files.log'.format(args.path), level=logging.INFO, format='%(asctime)s - %(message)s')

    convert_images_in_folder(args.path, args.output)
 
 
def convert_image_to_webp(file_path, output):
    try:
        with Image.open(file_path) as im:
            webp_file_path = os.path.splitext(file_path)[0] + '.webp'
            im.save(webp_file_path, 'webp', lossless=True)
            if output:
                logging.info('%s', file_path)
            return webp_file_path
    except Exception:
        return None
 
 
def convert_images_in_folder(folder_path, output):
    total_images = 0
    converted_images = 0
    
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in args.exclude]
        for file_name in files:
            if file_name.lower().endswith(tuple(args.extension)):
                total_images += 1
 
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in args.exclude]
        for file_name in files:
            if file_name.lower().endswith(tuple(args.extension)):
                file_path = os.path.join(root, file_name)
                webp_file_path = convert_image_to_webp(file_path, output)
                if webp_file_path:
                    if args.replace:
                        os.replace(file_path, webp_file_path)
                    converted_images += 1
                    print('{}/{}: Konvertiert zu WebP: {}'.format(converted_images, total_images, file_path))
 
 
if __name__ == '__main__':
    args = parser.parse_args()
    start()
 