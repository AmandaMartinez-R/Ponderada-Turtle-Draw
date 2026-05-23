import cv2
import numpy as np
import matplotlib.pyplot as plt

from turtle_draw.vision.grayscale import (
    rgb_to_grayscale)
from turtle_draw.vision.blur import (
    apply_blur
)
from turtle_draw.vision.convolution import (
    apply_convolution)


def apply_sobel(image):
    """
    Aplica operador Sobel manual.
    """

    # Kernel Sobel X
    sobel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])

    # Kernel Sobel Y
    sobel_y = np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ])

    # Gradiente horizontal
    gx = apply_convolution(image, sobel_x).astype(np.float32)
    # Gradiente vertical
    gy = apply_convolution(image, sobel_y).astype(np.float32)

    # Magnitude do gradiente
    gradient_magnitude = np.sqrt(gx**2 + gy**2)

    # Normaliza para 0-255
    gradient_magnitude = (
        gradient_magnitude / gradient_magnitude.max()
    ) * 255

    return gradient_magnitude.astype(np.uint8)


def main():

    # Carrega imagem
    image = cv2.imread("images/input/dog.png")

    # BGR -> RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Grayscale
    gray = rgb_to_grayscale(image)

    # Blur
    blurred = apply_blur(gray)

    # Sobel
    edges = apply_sobel(blurred)

    # Exibição
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(gray, cmap='gray')
    plt.title("Grayscale")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(blurred, cmap='gray')
    plt.title("Blur")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(edges, cmap='gray')
    plt.title("Sobel")
    plt.axis("off")

    plt.show()


if __name__ == "__main__":
    main()