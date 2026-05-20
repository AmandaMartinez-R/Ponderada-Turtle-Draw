import cv2
import numpy as np
import matplotlib.pyplot as plt

from vision.grayscale import rgb_to_grayscale
from vision.blur import apply_blur
from vision.sobel import apply_sobel


def apply_threshold(image, threshold=100):
    """
    Aplica threshold binário manual.
    """

    # Cria imagem vazia
    binary_image = np.zeros_like(image)

    # Pixels maiores que threshold viram branco
    binary_image[image >= threshold] = 255

    return binary_image


def main():

    # Carrega imagem
    image = cv2.imread("images/input/dog.png")
    if image is None:
        raise FileNotFoundError(
        "Imagem não encontrada em images/input/dog.png"
    )

    # BGR -> RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Pipeline
    gray = rgb_to_grayscale(image)

    blurred = apply_blur(gray)

    sobel = apply_sobel(blurred)

    binary = apply_threshold(sobel, threshold=100)

    # Exibição
    plt.figure(figsize=(20, 5))

    plt.subplot(1, 4, 1)
    plt.imshow(gray, cmap='gray')
    plt.title("Grayscale")
    plt.axis("off")

    plt.subplot(1, 4, 2)
    plt.imshow(blurred, cmap='gray')
    plt.title("Blur")
    plt.axis("off")

    plt.subplot(1, 4, 3)
    plt.imshow(sobel, cmap='gray')
    plt.title("Sobel")
    plt.axis("off")

    plt.subplot(1, 4, 4)
    plt.imshow(binary, cmap='gray')
    plt.title("Threshold")
    plt.axis("off")

    plt.show()


if __name__ == "__main__":
    main()