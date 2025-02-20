import argparse
import os
import shutil

SVG_LOC='./frontend/src/lib/assets'
SVG_NAME='ciso.svg'

ICO_LOC='./frontend/static'
ICO_NAME='favicon.ico'

# copy the new image to the correct location, and rename the old svg and ico files then rename the new ones
def process(LOC,NAME,new_path):
    shutil.copy(new_path, LOC)
    # if there is already a .old , delete the file with the default name
    if os.path.exists(LOC + '/' + NAME + '.old'):
        os.remove(LOC + '/' + NAME)
    else:
        shutil.move(LOC + '/' + NAME, LOC + '/' + NAME + '.old')
    # rename the new file to the correct name
    os.rename(LOC + '/' + os.path.basename(new_path), LOC + '/' + NAME)
    # if there are more images in the directory, remove them
    for file in os.listdir(LOC):
        if file.endswith('.svg') and file != NAME:
            os.remove(LOC + '/' + file)

def change_images(new_svg_path, new_ico_path):
    
    if new_svg_path:
        process(SVG_LOC,SVG_NAME,new_svg_path)
        
    if new_ico_path:
        process(ICO_LOC,ICO_NAME,new_ico_path)
        
"""
utility that lets the user input a path to an image they would like to use instead of ciso assitant ones
"""
def main():
    parser = argparse.ArgumentParser(description="""Allows you to change Ciso Assistant images.
                                     Must be used in the top directory i.e "./ciso-assistant-community".
                                     Will delete previous user-added images and keep the original and the new image.""",
                                     usage="""python change_images.py --banner <path_to_svg> --icon <path_to_ico>
                                     Banner is the logo at the top left. Icon is the tab icon.""")
    parser.add_argument('--banner', type=str, help='Give the path to the desired SVG file for the banner')
    parser.add_argument('--icon', type=str, help='Give the path to the desired ICO file for the icon')

    args = parser.parse_args()

    change_images(args.banner, args.icon)


if __name__ == '__main__':
    main()