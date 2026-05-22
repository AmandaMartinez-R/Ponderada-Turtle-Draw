import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../../../../'
        )
    )
)
import cv2

from vision.grayscale import rgb_to_grayscale
from vision.blur import apply_blur
from vision.sobel import apply_sobel
from vision.threshold import apply_threshold
from vision.contours import find_contours
from vision.filter_contours import filter_contours
from vision.coordinate_conversion import (
    convert_contours_to_turtle
)


def generate_drawing_path():

    """
    Gera trajetória completa para desenho.
    """

    # Caminho absoluto da raiz do projeto
    project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '../../../../'
    )
)
    # Caminho completo da imagem
    image_path = os.path.join(
    project_root,
    'images',
    'input',
    'dog.png'
    )

    # Carrega imagem
    image = cv2.imread(image_path)

    if image is None:

        raise FileNotFoundError(
            'Imagem não encontrada.'
        )

    # RGB
    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    # Pipeline visão computacional
    gray = rgb_to_grayscale(image)

    blurred = apply_blur(gray)

    sobel = apply_sobel(blurred)

    binary = apply_threshold(
        sobel,
        threshold=100
    )

    # Contornos
    contours = find_contours(binary)

    filtered = filter_contours(
        contours,
        min_size=50
    )

    # Dimensões
    height, width = binary.shape

    # Conversão
    turtle_contours = (
        convert_contours_to_turtle(
            filtered,
            width,
            height
        )
    )

    # Junta todos os pontos
    full_path = []

    for contour in turtle_contours:

        for point in contour[::5]:

            full_path.append(point)

    return full_path