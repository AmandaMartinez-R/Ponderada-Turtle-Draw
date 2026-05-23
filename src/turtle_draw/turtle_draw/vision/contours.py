import cv2
import numpy as np
import matplotlib.pyplot as plt

from turtle_draw.vision.grayscale import (
    rgb_to_grayscale
)
from turtle_draw.vision.blur import (
    apply_blur
)
from turtle_draw.vision.sobel import (
    apply_sobel
)
from turtle_draw.vision.threshold import (
    apply_threshold
)


def get_neighbors(x, y):
    """
    Retorna os 8 vizinhos do pixel
    """

    return [
        (x-1, y-1),
        (x,   y-1),
        (x+1, y-1),

        (x-1, y),
        (x+1, y),

        (x-1, y+1),
        (x,   y+1),
        (x+1, y+1),
    ]


def find_contours(binary_image):
    """
    Detecta contornos manualmente
    """

    height, width = binary_image.shape

    # Marca pixels visitados
    visited = np.zeros_like(binary_image, dtype=bool)

    contours = []

    # Percorre todos os pixels
    for y in range(height):

        for x in range(width):

            # Pixel branco e não visitado
            if binary_image[y, x] == 255 and not visited[y, x]:

                component = []
                stack = [(x, y)]
                in_component = {(x, y)}

                while stack:

                    cx, cy = stack.pop()
                    component.append((cx, cy))

                    for nx, ny in get_neighbors(cx, cy):

                        if (
                            0 <= nx < width
                            and
                            0 <= ny < height
                            and
                            binary_image[ny, nx] == 255
                            and
                            (nx, ny) not in in_component
                        ):
                            in_component.add((nx, ny))
                            stack.append((nx, ny))

                for px, py in component:
                    visited[py, px] = True

                def neighbor_count(p):
                    return sum(
                        1
                        for nx, ny in get_neighbors(p[0], p[1])
                        if (nx, ny) in in_component
                    )

                start_point = min(component, key=neighbor_count)

                ordered = []
                walked = set()
                current = start_point

                while current is not None:

                    ordered.append(current)
                    walked.add(current)

                    next_point = None

                    for nx, ny in get_neighbors(
                        current[0],
                        current[1]
                    ):
                        if (
                            (nx, ny) in in_component
                            and
                            (nx, ny) not in walked
                        ):
                            next_point = (nx, ny)
                            break

                    current = next_point

                while len(walked) < len(in_component):

                    remaining = [
                        p for p in component if p not in walked
                    ]
                    last = ordered[-1]

                    nearest = min(
                        remaining,
                        key=lambda p: (
                            (p[0] - last[0])**2
                            + (p[1] - last[1])**2
                        )
                    )

                    current = nearest

                    while current is not None:

                        ordered.append(current)
                        walked.add(current)

                        next_point = None

                        for nx, ny in get_neighbors(
                            current[0],
                            current[1]
                        ):
                            if (
                                (nx, ny) in in_component
                                and
                                (nx, ny) not in walked
                            ):
                                next_point = (nx, ny)
                                break

                        current = next_point

                contours.append(ordered)

    return contours


def main():

    # Carrega imagem
    image = cv2.imread("images/input/dog.png")

    if image is None:
        raise FileNotFoundError(
            "Imagem não encontrada."
        )

    # BGR -> RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Pipeline
    gray = rgb_to_grayscale(image)

    blurred = apply_blur(gray)

    sobel = apply_sobel(blurred)

    binary = apply_threshold(sobel, threshold=100)

    # Detecta contornos
    contours = find_contours(binary)

    print(f"Contornos encontrados: {len(contours)}")

    # Mostra imagem
    plt.figure(figsize=(8, 8))
    plt.imshow(binary, cmap='gray')
    plt.title("Imagem Binária")
    plt.axis("off")

    plt.show()

    # Mostra tamanho dos maiores contornos
    contour_sizes = [len(c) for c in contours]

    contour_sizes.sort(reverse=True)

    print("\nMaiores contornos:")

    for i, size in enumerate(contour_sizes[:10]):
        print(f"{i+1}: {size} pixels")


if __name__ == "_main_":
    main()