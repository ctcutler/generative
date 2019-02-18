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

def main():
    SCALE = 85
    IMAGE_WIDTH = 16 * SCALE
    IMAGE_HEIGHT = 9 * SCALE
    MARGIN = int(SCALE / 2)
    WHITE = np.array((255, 255, 255))
    BLACK = np.array((0, 0, 0))
    LINE_WIDTH = 5

    solid = init_solid(IMAGE_WIDTH, IMAGE_HEIGHT, WHITE)
    height = IMAGE_HEIGHT - (MARGIN * 2)
    line_flat = np.tile(BLACK, LINE_WIDTH * height)
    line = line_flat.reshape(height, LINE_WIDTH, BLACK.size)
    first_line = draw_line(solid, (MARGIN, MARGIN), line)
    save_image('sl.png', first_line)

if __name__== "__main__":
    main()

