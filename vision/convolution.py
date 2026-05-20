import numpy as np
import matplotlib.pyplot as plt
import cv2

from vision.grayscale import rgb_to_grayscale


def apply_convolution(image, kernel):
    """
    Aplica convolução manual em uma imagem
    """

    # Dimensões da imagem
    image_height, image_width = image.shape

    # Dimensões do kernel
    kernel_height, kernel_width = kernel.shape

    # Calcula padding
    pad_h = kernel_height // 2
    pad_w = kernel_width // 2

    # Cria imagem com padding
    padded_image = np.pad(
        image,
        ((pad_h, pad_h), (pad_w, pad_w)),
        mode='constant'
    )

    # Cria saída vazia
    output = np.zeros_like(image)

    # Percorre pixels da imagem
    for y in range(image_height):

        for x in range(image_width):

            # Extrai região local
            region = padded_image[
                y:y + kernel_height,
                x:x + kernel_width
            ]

            # Multiplicação elemento a elemento
            value = np.sum(region * kernel)

            # Salva resultado
            output[y, x] = value

    return output


def main():

    # Carrega imagem
    image = cv2.imread("images/input/dog.png")

    # BGR -> RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Grayscale
    gray = rgb_to_grayscale(image)

    # Kernel simples de teste
    kernel = np.array([
        [1, 0, -1],
        [1, 0, -1],
        [1, 0, -1]
    ])

    # Aplica convolução
    result = apply_convolution(gray, kernel)

    # Mostra resultado
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(gray, cmap='gray')
    plt.title("Original")

    plt.subplot(1, 2, 2)
    plt.imshow(result, cmap='gray')
    plt.title("Convolução")

    plt.show()


if __name__ == "__main__":
    main()