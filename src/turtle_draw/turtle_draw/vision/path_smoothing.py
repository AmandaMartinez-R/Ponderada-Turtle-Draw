import numpy as np


def smooth_contour(contour, window_size=5):

    """
    Suaviza contorno usando média móvel.
    """

    smoothed = []

    half_window = window_size // 2

    for i in range(len(contour)):

        x_values = []
        y_values = []

        for j in range(
            i - half_window,
            i + half_window + 1
        ):

            # Mantém índices válidos
            if 0 <= j < len(contour):

                x, y = contour[j]

                x_values.append(x)
                y_values.append(y)

        avg_x = np.mean(x_values)
        avg_y = np.mean(y_values)

        smoothed.append(
            (avg_x, avg_y)
        )

    return smoothed