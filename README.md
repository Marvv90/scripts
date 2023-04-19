# Scripts

## Scripts that I use 

### Convert Images
`python convert_images.py --exclude example example2 --no-output --no-replace --extension png gif`

Search in the current Working Directory after Images with the Extension `png` and `gif` and convert the Images to Webp.

Need to install:
`pip install argparse`
`pip install Pillow`

### Scale Images
`python scale_images --read`

`python scale_images --width x` or `python scale_images --height x` 

Scale Images to the Width / Height with same Aspect Ratio override old Images !!

Need to install:
`pip install argparse`
`pip install opencv-python`
