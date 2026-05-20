import cv2
import numpy as np
import matplotlib.pyplot as plt

from vision.grayscale import rgb_to_grayscale
from vision.convolution import apply_convolution


def apply_blur(image):
    """
    Aplica blur manual usando convolução
    """

    # Kernel de média 3x3
    kernel = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]) / 9

    # Aplica convolução
    blurred = apply_convolution(image, kernel)

    return blurred


def main():

    # Carrega imagem
    image = cv2.imread("images/input/dog.png")

    # BGR -> RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Grayscale
    gray = rgb_to_grayscale(image)

    # Blur
    blurred = apply_blur(gray)

    # Exibição
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(gray, cmap='gray')
    plt.title("Original Grayscale")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(blurred, cmap='gray')
    plt.title("Blur Aplicado")
    plt.axis("off")

    plt.show()


if __name__ == "__main__":
    main()