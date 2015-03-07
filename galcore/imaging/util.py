"""Imaging utilities.
"""

import math
import PIL.Image


def read_image(inio):
    """
    """

    try:
        inio.seek(0)
    except AttributeError:
        raise # See why this raises. I'd rather not just "pass" this at
              #     least without GOOD reason.
        
        pass  # inio should be a path. (???)

    return PIL.Image.open(inio)


def preserve_aspect(x, y, *bound):
    """Binds the x or y size component to the bound args (x,y) or (x,)
    provided while keeping the aspect ratio. i.e. (resize image)
    
    x, y  - dimensions to be bound.
    bound - args containing the constraints to bind the x and/or y to.
    """

    x, y = float(x), float(y)

    bound_x, *bound_y = bound   # py3 only. <3

    if bound_x and x > bound_x:
        x, y = bound_x, y / (x / bound_x)

    if bound_y and y > bound_y[0]:
        x, y = x / (y / bound_y[0]), bound_y[0]

    return math.ceil(x), math.ceil(y)


def resize_image(image, *bound, aspect_alg=preserve_aspect,
                 filter_alg=PIL.Image.NEAREST):
    """Given an input `PIL.image` object, a bound tuple (x, y),
    returns PIL.Image instance of a resized image.
    """

    return image.resize(aspect_alg(*image.size + bound), filter_alg)