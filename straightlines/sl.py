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

def make_line(height, seed):
    # in addition to experimenting with how quickly the sides fade out,
    # play with how close the middle is to one side or the other

    return np.tile(seed, height).reshape(height, 5, 3)

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

    line = init_solid(IMAGE_WIDTH, IMAGE_HEIGHT, WHITE)
    height = IMAGE_HEIGHT - (MARGIN * 2)

    for (i, line_seed) in enumerate([HARD, SOFT1, SOFT2, SOFT3]):
        line = draw_line(
            line, (MARGIN, (MARGIN * (i+1)) + (5 * i)),
            make_line(height, line_seed)
        )
    save_image('sl.png', line)

if __name__== "__main__":
    main()

