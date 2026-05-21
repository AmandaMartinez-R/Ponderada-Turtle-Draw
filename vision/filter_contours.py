import cv2
import numpy as np
import matplotlib.pyplot as plt

from vision.grayscale import rgb_to_grayscale
from vision.blur import apply_blur
from vision.sobel import apply_sobel
from vision.threshold import apply_threshold
from vision.contours import find_contours


def filter_contours(contours, min_size=50):
    """
    Remove contornos pequenos
    """

    filtered = []

    for contour in contours:

        if len(contour) >= min_size:
            filtered.append(contour)

    return filtered


def draw_contours(shape, contours):
    """
    Desenha contornos em uma imagem vazia
    """

    output = np.zeros(shape, dtype=np.uint8)

    for contour in contours:

        for x, y in contour:

            output[y, x] = 255

    return output


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

    print(f"\nContornos originais: {len(contours)}")

    # Filtra
    filtered_contours = filter_contours(
        contours,
        min_size=50
    )

    print(
        f"Contornos filtrados: "
        f"{len(filtered_contours)}"
    )

    # Ordena do maior para menor
    filtered_contours.sort(
        key=len,
        reverse=True
    )

    # Desenha contornos filtrados
    contour_image = draw_contours(
        binary.shape,
        filtered_contours
    )

    # Exibe
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(binary, cmap='gray')
    plt.title("Antes da Filtragem")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(contour_image, cmap='gray')
    plt.title("Após Filtragem")
    plt.axis("off")

    plt.show()

    # Mostra maiores contornos
    print("\nMaiores contornos:")

    for i, contour in enumerate(
        filtered_contours[:10]
    ):

        print(
            f"{i+1}: "
            f"{len(contour)} pixels"
        )


if __name__ == "__main__":
    main()