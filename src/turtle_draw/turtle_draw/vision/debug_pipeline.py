import cv2
import numpy as np
import matplotlib.pyplot as plt

from turtle_draw.vision.grayscale import (
    rgb_to_grayscale
)
from turtle_draw.vision.blur import (
    apply_blur
)
from turtle_draw.vision.threshold import (
    apply_threshold
)
from turtle_draw.vision.closing import (
    apply_closing)
from turtle_draw.vision.invert import (
    invert_image)
from turtle_draw.vision.outer_contour import (
    extract_outer_contour
)


def main():

    # Carrega imagem
    image = cv2.imread(
        'images/input/dog.png'
    )

    # Verifica erro
    if image is None:

        print("Imagem não encontrada.")
        return

    # BGR -> RGB
    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    # Grayscale
    gray = rgb_to_grayscale(image)

    # Blur
    blurred = apply_blur(gray)

   # Threshold
    binary = apply_threshold(
    blurred,
    threshold=120
    )

    # Inverte imagem
    inverted = invert_image(binary)

    # Closing
    closed = apply_closing(inverted)

    # Contorno externo
    outer = extract_outer_contour(
    closed
    )


    # Desinverte
    closed = invert_image(closed)

    # Cria figura
    fig, axes = plt.subplots(1, 7, figsize=(24, 5))

    # Original
    axes[0].imshow(image)
    axes[0].set_title('Original')

    # Grayscale
    axes[1].imshow(
        gray,
        cmap='gray'
    )
    axes[1].set_title('Grayscale')

    # Blur
    axes[2].imshow(
        blurred,
        cmap='gray'
    )
    axes[2].set_title('Blur')

    # Threshold
    axes[3].imshow(
    binary,
    cmap='gray'
    )
    axes[3].set_title('Threshold')

    # Invertida
    axes[4].imshow(
    inverted,
    cmap='gray'
    )
    axes[4].set_title('Inverted')

    # Closing
    axes[5].imshow(
    closed,
    cmap='gray'
    )
    axes[5].set_title('Closing')   

    # Contorno externo
    axes[6].imshow(
    outer,
    cmap='gray'
    )
    axes[6].set_title(
    'Outer Contour'
    ) 

    # Remove eixos
    for ax in axes:

        ax.axis('off')

    plt.tight_layout()

    plt.show()


if __name__ == '__main__':

    main()