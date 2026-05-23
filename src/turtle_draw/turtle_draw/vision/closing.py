from turtle_draw.vision.dilation import (
    dilate
)

from turtle_draw.vision.erosion import (
    erode
)


def apply_closing(binary_image):

    """
    Closing mais forte.
    """

    output = binary_image

    # Dilata várias vezes
    for _ in range(30):

        output = dilate(output)

    # Erode várias vezes
    for _ in range(30):

        output = erode(output)

    return output