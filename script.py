import math
import time
import numpy as np
from PIL import Image
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
from clut.clut.clut import CLUT
from minecraft.colours import MINECRAFT_COLOURS

def rawrgb_to_rgb(r, g, b):
    return sRGBColor(r/255, g/255, b/255)

def rgb_to_rawrgb(c):
    return (round(c.rgb_r*255), round(c.rgb_g*255), round(c.rgb_b*255))

def convert_to_lab(c):
    return convert_color(c, LabColor)

def convert_to_rgb(c):
    return convert_color(c, sRGBColor)

def closest_colour(options, c):
    smallest = float('inf')
    closest = None
    for option in options:
        dist = delta_e_cie1976(option, c)
        if dist < smallest:
            smallest = dist
            closest = option
    return closest

MINECRAFT_COLOURS_RGB=list(map(lambda c: rawrgb_to_rgb(c[0], c[1], c[2]), MINECRAFT_COLOURS))
MINECRAFT_COLOURS_LAB=list(map(lambda c: convert_to_lab(c), MINECRAFT_COLOURS_RGB))

def rawrgb_closest_minecraft_colour_rawrgb(r, g, b):
    c = rawrgb_to_rgb(r, g, b)
    l = convert_to_lab(c)
    closest_l = closest_colour(MINECRAFT_COLOURS_LAB, l)
    closest_r = convert_to_rgb(closest_l)
    return rgb_to_rawrgb(closest_r)

# c = rawrgb_to_rgb(44, 235, 33)
# r = convert_to_lab(c)
# print(r)
# print(convert_to_rgb(r))
# print(delta_e_cie1976(r, convert_to_lab(rawrgb_to_rgb(22, 22, 22))))
# print(delta_e_cie1976(r, convert_to_lab(rawrgb_to_rgb(43, 235, 33))))
# print(convert_to_rgb(closest_colour(MINECRAFT_COLOURS_LAB, r)))
# print(rawrgb_closest_minecraft_colour_rawrgb(44, 235, 33))

# def update_colours(r_start, r_end):
#     for r in range(r_start, r_end):
#         print('r', r)
#         start = time.time()
#         for g in range(256):
#             for b in range(256):
#                 x, y, z = rawrgb_closest_minecraft_colour_rawrgb(r, g, b)
#                 with mutex:
#                     clut[r, g, b] = [x, y, z]
#         end = time.time()
#         print(end - start)

# num_threads=1
# range_size=256
# if range_size // num_threads != range_size / num_threads:
#     print('ERROR: invalid thread count')
#     exit(-1)
# processes: list[Process] = []
# for i in range(num_threads):
#     block = range_size // num_threads
#     start = block * i
#     end = start + block
#     p = Process(target=update_colours, args = (start, end))
#     p.start()
#     processes.append(p)
# for process in processes:
#     process.join()

# from joblib import Parallel, delayed
# from multiprocessing import Process, Lock

# mutex = Lock()


# for a color depth of 256, the lossless size is 16
LOSSLESS_SIZE=16

clut = CLUT()

for r in range(256):
    print('r', r)
    start = time.time()
    for g in range(256):
        for b in range(256):
            x, y, z = rawrgb_closest_minecraft_colour_rawrgb(r, g, b)
            clut[r, g, b] = [x, y, z]
    end = time.time()
    print(end - start)

clut.save('minecraft-colours-haldclut.png', size=LOSSLESS_SIZE)
