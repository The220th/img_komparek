# -*- coding: utf-8 -*-

import os
import PIL
from PIL import Image


def getFilesList(dirPath: str) -> list:
    return [os.path.join(path, name) for path, subdirs, files in os.walk(dirPath) for name in files]

# return images only
def image_filter(images_list: list) -> list:
    allowed = ["BLP", "BMP", "DDS", "DIB", "EPS", "GIF", "ICNS", "ICO", "IM", "JPEG", "JPG", "MSP", "PCX", "PNG", "APNG", "PPM", "SGI", "SPIDER", "TGA", "TIFF", "XBM"]
    res = []
    for im_i in images_list:
        filename, file_extension = os.path.splitext(im_i)
        if(file_extension != "" and file_extension.upper()[1:] in allowed):
            res.append(im_i)
    return res

def alert_about_error(msg: str):
    print(f"\n=====ERROR!!!=====\n{msg}\n===============\n\n")

def get_str_info_about_image(image_path: str) -> str:
    try:
        im = Image.open(image_path)
        return f"{image_path}: {im.size}"
    except:
        return f"{image_path}: not image"

def bits_to_str(bits_hash: list):
    LETTERS_16 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    if(len(bits_hash) % 4 != 0):
        bits = list(bits_hash) + [0]*(4-(len(bits_hash)%4))
    else:
        bits = bits_hash
    
    res = ""
    for i in range(0, len(bits), 4):
        LETTERS_16_i = int(f"{bits[i]}{bits[i+1]}{bits[i+2]}{bits[i+3]}", 2)
        res += LETTERS_16[LETTERS_16_i]
    return res

# return bits list with size = SQUARE_SIZE*SQUARE_SIZE
def calc_img_dif_hash(image_path: str) -> list:
    #try:
# https://habr.com/ru/post/120562/
# https://habr.com/ru/post/120577/
# https://overcoder.net/q/120723/%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC-%D1%81%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9
# https://github.com/JohannesBuchner/imagehash
        SQUARE_SIZE = 8

        im = Image.open(image_path)
        im.load()
        im = im.resize((SQUARE_SIZE, SQUARE_SIZE), Image.Resampling.NEAREST)
        im.convert('RGB')
        img_size = im.size
        grays, gray_avg = [], 0
        for i in range(img_size[0]):
            for j in range(img_size[1]):
                img_pixel = im.getpixel((i, j))
                r, g, b = img_pixel[0], img_pixel[1], img_pixel[2]
                gray = (0.3 * r) + (0.59 * g) + (0.11 * b) # The Weighted Method or luminosity method
                gray_avg += gray
                grays.append(gray)
        gray_avg /= SQUARE_SIZE*SQUARE_SIZE
        bits = []
        for gray_i in grays:
            if(gray_i > gray_avg):
                bits.append(1)
            else:
                bits.append(0)
        
        return bits

    #except:
    #    alert_about_error(f"Cannot calc_img_dif_hash of \"{image_path}\". ")
        return [0]*(SQUARE_SIZE*SQUARE_SIZE)

if __name__ == '__main__':
    
    root_path = "."
    all_files = getFilesList(root_path)
    all_imgs = image_filter(   [os.path.abspath(file_i) for file_i in all_files]   )
    for img_i in all_imgs:
        hash_bin = calc_img_dif_hash(img_i)
        print(f"{get_str_info_about_image(img_i)}, hash={bits_to_str(hash_bin)}")