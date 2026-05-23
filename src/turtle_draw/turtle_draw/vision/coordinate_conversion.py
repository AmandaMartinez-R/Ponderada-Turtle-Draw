import cv2
import numpy as np
import matplotlib.pyplot as plt

from turtle_draw.vision.grayscale import (
    rgb_to_grayscale
)
from turtle_draw.vision.blur import (
    apply_blur)
from turtle_draw.vision.sobel import (
    apply_sobel
)
from turtle_draw.vision.threshold import (
    apply_threshold
)
from turtle_draw.vision.contours import (
    find_contours
)
from turtle_draw.vision.filter_contours import (
    filter_contours
)


TURTLESIM_SIZE = 11.0


def pixel_to_turtle(
    x_pixel,
    y_pixel,
    image_width,
    image_height
):
    """
    Converte pixel para coordenada do turtlesim.
    """

    # Escala X
    x_turtle = (
        x_pixel / image_width
    ) * TURTLESIM_SIZE

    # Escala Y + inversão
    y_turtle = TURTLESIM_SIZE - (
        (y_pixel / image_height)
        * TURTLESIM_SIZE
    )

    return (x_turtle, y_turtle)


def convert_contours_to_turtle(
    contours,
    image_width,
    image_height
):
    """
    Converte todos os contornos.
    """

    turtle_contours = []

    for contour in contours:

        converted = []

        for x, y in contour:

            turtle_point = pixel_to_turtle(
                x,
                y,
                image_width,
                image_height
            )

            converted.append(turtle_point)

        turtle_contours.append(converted)

    return turtle_contours


def main():

    # Carrega imagem
    image = cv2.imread("images/input/dog.png")

    if image is None:
        raise FileNotFoundError(
            "Imagem não encontrada."
        )

    # RGB
    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    # Pipeline
    gray = rgb_to_grayscale(image)

    blurred = apply_blur(gray)

    sobel = apply_sobel(blurred)

    binary = apply_threshold(
        sobel,
        threshold=100
    )

    # Contornos
    contours = find_contours(binary)

    filtered_contours = filter_contours(
        contours,
        min_size=50
    )

    # Dimensões
    image_height, image_width = binary.shape

    # Conversão
    turtle_contours = convert_contours_to_turtle(
        filtered_contours,
        image_width,
        image_height
    )

    print(
        f"\nContornos convertidos: "
        f"{len(turtle_contours)}"
    )

    # Mostra primeiros pontos
    first_contour = turtle_contours[0]

    print("\nPrimeiros pontos convertidos:\n")

    for point in first_contour[:10]:

        print(point)

    # Visualização
    plt.figure(figsize=(8, 8))

    plt.imshow(binary, cmap='gray')

    plt.title(
        "Imagem usada para gerar coordenadas"
    )

    plt.axis("off")

    plt.show()


if __name__ == "__main__":
    main()