import numpy as np


def erode(binary_image):

    """
    Erosão manual.
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

            # Todos precisam ser brancos
            if np.min(region) == 255:

                output[y, x] = 255

            else:

                output[y, x] = 0

    return output