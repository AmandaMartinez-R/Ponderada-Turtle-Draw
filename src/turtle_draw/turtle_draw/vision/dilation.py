import numpy as np


def dilate(binary_image):

    """
    Dilatação manual.
    """

    height, width = binary_image.shape

    output = np.copy(binary_image)

    kernel_size = 3
    offset = kernel_size // 2

    for y in range(offset, height - offset):

        for x in range(offset, width - offset):

            region = binary_image[
                y-offset:y+offset+1,
                x-offset:x+offset+1
            ]

            # Se algum pixel for branco
            if np.max(region) == 255:

                output[y, x] = 255

    return output