import numpy as np
from PIL import Image

def save_image(file_name, image_data):
    img = Image.fromarray(np.uint8(image_data), 'RGB')
    img.save(file_name)

def init_solid(width, height, rgb):
    a = np.array(rgb)
    tiled = np.tile(a, width * height)

    return np.reshape(tiled, (height, width, 3))

def draw_line(canvas, start, length, width):
    c = canvas.copy()
    (x, y) = start

    c[x:x+length, y:y+width] = np.array((0, 0, 0))

    return c

def main():
    SCALE = 85
    IMAGE_WIDTH = 16 * SCALE
    IMAGE_HEIGHT = 9 * SCALE
    MARGIN = int(SCALE / 2)
    WHITE = (255, 255, 255)
    LINE_WIDTH = 5

    solid = init_solid(IMAGE_WIDTH, IMAGE_HEIGHT, WHITE)
    first_line = draw_line(
        solid, (MARGIN, MARGIN), IMAGE_HEIGHT - (MARGIN * 2), LINE_WIDTH
    )
    save_image('sl.png', first_line)

if __name__== "__main__":
    main()
