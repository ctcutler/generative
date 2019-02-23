import random

import numpy as np
from PIL import Image

def save_image(file_name, image_data):
    img = Image.fromarray(np.uint8(image_data), 'RGB')
    img.save(file_name)

def init_solid(width, height, rgb):
    tiled = np.tile(rgb, width * height)
    return np.reshape(tiled, (height, width, 3))

def draw_line(canvas, position, line):
    c = canvas.copy()
    (x, y) = position
    height = line.shape[0]
    width = line.shape[1]

    c[x:x+height, y:y+width] = line

    return c

def random_walk(how_often, length, minimum, maximum, start):
    w = []
    c = start
    for i in range(length):
        if random.random() < how_often:
            if random.random() < .5:
                c = max(minimum, c - 1)
            else:
                c = min(maximum, c + 1)
        w.append(c)
    return w

def make_line(height, seed):
    # generate "rotation" offsets
    #    for every row, .05 chance of either rotating by 1 in either direction
    # rotate seed as needed while tiling (or after)

    offsets = random_walk(.05, height, 0, 4, 0)
    line = np.tile(seed, height).reshape(height, 5, 3)

    for i in range(height):
        line[i] = np.roll(line[i], offsets[i], 0)

    return line

def main():
    SCALE = 85
    IMAGE_WIDTH = 16 * SCALE
    IMAGE_HEIGHT = 9 * SCALE
    MARGIN = int(SCALE / 2)
    WHITE = np.array((255, 255, 255))
    LINE_WIDTH = 5

    HARD = np.array((
        0, 0, 0,
        0, 0, 0,
        0, 0, 0,
        0, 0, 0,
        0, 0, 0,
    ))

    SOFT1 = np.array((
        64, 64, 64,
        32, 32, 32,
        0, 0, 0,
        32, 32, 32,
        64, 64, 64,
    ))

    SOFT2 = np.array((
        128, 128, 128,
        64, 64, 64,
        0, 0, 0,
        64, 64, 64,
        128, 128, 128,
    ))

    SOFT3 = np.array((
        192, 192, 192,
        96, 96, 96,
        0, 0, 0,
        96, 96, 96,
        192, 192, 192,
    ))

    SOFT_LEFT1 = np.array((
        0, 0, 0,
        64, 64, 64,
        96, 96, 96,
        112, 112, 112,
        120, 120, 120,
    ))

    SOFT_LEFT2 = np.array((
        64, 64, 64,
        0, 0, 0,
        64, 64, 64,
        96, 96, 96,
        112, 112, 112,
    ))

    SOFT_LEFT3 = np.array((
        0, 0, 0,
        64, 64, 64,
        96, 96, 96,
        128, 128, 128,
        192, 192, 192,
    ))

    SKINNY1 = np.array((
        0, 0, 0,
        0, 0, 0,
        0, 0, 0,
        255, 255, 255,
        255, 255, 255,
    ))

    SKINNY2 = np.array((
        0, 0, 0,
        0, 0, 0,
        255, 255, 255,
        255, 255, 255,
        255, 255, 255,
    ))

    SKINNY3 = np.array((
        0, 0, 0,
        255, 255, 255,
        255, 255, 255,
        255, 255, 255,
        255, 255, 255,
    ))

    line = init_solid(IMAGE_WIDTH, IMAGE_HEIGHT, WHITE)
    height = IMAGE_HEIGHT - (MARGIN * 2)

    for (i, line_seed) in enumerate([HARD, SOFT1, SOFT2, SOFT3, SOFT_LEFT1, SOFT_LEFT2,
        SOFT_LEFT3, SKINNY1, SKINNY2, SKINNY3]):
        line = draw_line(
            line, (MARGIN, (MARGIN * (i+1)) + (5 * i)),
            make_line(height, line_seed)
        )
    save_image('sl.png', line)

if __name__== "__main__":
    main()

