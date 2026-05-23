import cv2
import numpy as np
import matplotlib.pyplot as plt


def rgb_to_grayscale(image):
    """
    Converte uma imagem RGB para escala de cinza
    Fórmula:
    Gray = 0.299R + 0.587G + 0.114B
    """

    # Separa os canais
    red = image[:, :, 0]
    green = image[:, :, 1]
    blue = image[:, :, 2]

    # Aplica fórmula de luminância
    grayscale = (
        0.299 * red +
        0.587 * green +
        0.114 * blue
    )

    return grayscale.astype(np.uint8)


def main():

    # Carrega imagem
    image = cv2.imread("images/input/dog.png")

    # OpenCV carrega em BGR
    # converte para RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Converte para grayscale
    gray_image = rgb_to_grayscale(image)

    # Exibe resultado
    plt.figure(figsize=(8, 8))

    plt.imshow(gray_image, cmap='gray')
    plt.title("Imagem em Grayscale")

    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    main()