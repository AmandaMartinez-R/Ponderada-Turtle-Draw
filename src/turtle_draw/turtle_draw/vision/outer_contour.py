import numpy as np


def extract_outer_contour(binary_image):

    """
    Extrai apenas o contorno externo.
    """

    height, width = binary_image.shape

    contour = np.full(
        (height, width),
        255,
        dtype=np.uint8
    )

    for y in range(1, height - 1):

        for x in range(1, width - 1):

            # Pixel preto = objeto
            if binary_image[y, x] == 0:

                # Região vizinha
                neighbors = binary_image[
                    y-1:y+2,
                    x-1:x+2
                ]

                # Se algum vizinho for branco
                if np.max(neighbors) == 255:

                    contour[y, x] = 0

    return contour