import numpy as np


def trace_contour(binary_image):

    """
    Rastreia contorno contínuo.
    """

    height, width = binary_image.shape

    visited = np.zeros(
        (height, width),
        dtype=bool
    )

    contour_path = []

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),

        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1)
    ]

    for y in range(height):

        for x in range(width):

            if (
                binary_image[y, x] == 0
                and not visited[y, x]
            ):

                stack = [(x, y)]

                while stack:

                    px, py = stack.pop()

                    if (
                        px < 0
                        or py < 0
                        or px >= width
                        or py >= height
                    ):
                        continue

                    if visited[py, px]:
                        continue

                    if binary_image[py, px] != 0:
                        continue

                    visited[py, px] = True

                    contour_path.append(
                        (px, py)
                    )

                    for dx, dy in directions:

                        nx = px + dx
                        ny = py + dy

                        stack.append(
                            (nx, ny)
                        )

                return contour_path

    return contour_path