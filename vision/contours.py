import cv2
import numpy as np
import matplotlib.pyplot as plt

from vision.grayscale import rgb_to_grayscale
from vision.blur import apply_blur
from vision.sobel import apply_sobel
from vision.threshold import apply_threshold


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

                contour = []

                # Pilha para DFS
                stack = [(x, y)]

                visited[y, x] = True

                while stack:

                    current_x, current_y = stack.pop()

                    contour.append((current_x, current_y))

                    # Explora vizinhos
                    for neighbor_x, neighbor_y in get_neighbors(
                        current_x,
                        current_y
                    ):

                        # Verifica limites
                        if (
                            0 <= neighbor_x < width
                            and
                            0 <= neighbor_y < height
                        ):

                            # Branco e não visitado
                            if (
                                binary_image[
                                    neighbor_y,
                                    neighbor_x
                                ] == 255
                                and
                                not visited[
                                    neighbor_y,
                                    neighbor_x
                                ]
                            ):

                                stack.append(
                                    (neighbor_x, neighbor_y)
                                )

                                visited[
                                    neighbor_y,
                                    neighbor_x
                                ] = True

                contours.append(contour)

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


if __name__ == "__main__":
    main()