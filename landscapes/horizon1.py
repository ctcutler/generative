import random

import numpy as np
from PIL import Image

WIDTH = int(16 * 100 * .6)
HEIGHT = int(9 * 100 * .6)


def init_solid(width, height, rgb):
    a = np.array(rgb)
    tiled = np.tile(a, width * height)

    return np.reshape(tiled, (height, width, 3))

def gradient(a, rgb, scaling):
    color_deltas = (rgb - a.reshape(-1, 3)).reshape(a.shape)
    color_scaling = np.repeat(scaling, 3).reshape(a.shape)
    scaled_deltas = color_scaling * color_deltas

    return a + scaled_deltas

def noise(a, amount):
    r = (np.random.rand(*a.shape) * amount * 2) - amount
    noisy = r + a
    upper_limit = np.repeat(255, a.size).reshape(a.shape)
    lower_limit = np.repeat(0, a.size).reshape(a.shape)
    return np.minimum(upper_limit, np.maximum(lower_limit, noisy))

def save_image(file_name, image_data):
    img = Image.fromarray(np.uint8(image_data), 'RGB')
    img.save(file_name)

def color_scale(cur, total, proportion):
    """
    Goal is to make a certain proportion solid and do the gradient
    only after/above that proportion.
    """
    proportion = .85

    if cur >= total * proportion:
        n = (cur - (total * proportion)) * \
            (total/(total-(total*proportion)))
        return float(n**2) / ((total - 1)**2)
    else:
        return 0

def smooth_rands(n, low, high, variation, seed=None):
    """
    Return a sequence of n values, low <= value < high where the difference
    between each adjacent value is less than +/- variation. seed allows for
    deterministic unit testing.
    """
    random.seed(seed)
    deltas = [
        ((random.random() * 2) - 1) * variation
        for x in range(n-1)
    ]

    rands = [(random.random() * (high - low)) + low]
    prev = rands[0]
    for delta in deltas:
        next = prev + delta
        next = max(low, next)
        next = min(high, next)
        rands.append(next)
        prev = next

    return np.array(rands)

def horizon_scaling(shape):
    (height, width, depth) = shape

    # make random cutoffs
    rands = smooth_rands(width, .80, .85, .01)
    cutoff = np.tile(rands, height).reshape(height, width)

    # smooth gradient indexes
    cur = np.repeat(np.arange(height), width).reshape(height, width)
    cur = cur/cur.max()
    total = np.ones((height, width))

    # ignore inactive ones
    inactive = cur < cutoff
    cur[inactive] = cutoff[inactive]

    # create the scaling
    return ((cur - cutoff) ** 1) / ((total - cutoff) ** 1)

def main():
    blue = (75, 0, 130)
    yellow = (148, 0, 211)

    solid = init_solid(WIDTH, HEIGHT, blue)

    (top, bottom) = np.split(solid, 2)

    top_scaling = horizon_scaling(top.shape)
    bottom_scaling = horizon_scaling(bottom.shape)

    gradient_top = gradient(top, yellow, top_scaling)
    gradient_bottom = gradient(bottom, yellow, bottom_scaling)
    gradient_bottom_flipped = np.flipud(gradient_bottom)
    g = np.concatenate((gradient_top, gradient_bottom_flipped))
    g_noise = noise(g, 1)
    save_image('horizon1.png', g_noise)

if __name__== "__main__":
    main()

