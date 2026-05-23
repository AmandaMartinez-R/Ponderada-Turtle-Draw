import math


def optimize_path(points):

    """
    Ordena pontos usando
    nearest neighbor.
    """

    if not points:
        return []

    remaining = points.copy()

    optimized = []

    current = remaining.pop(0)

    optimized.append(current)

    while remaining:

        nearest = min(
            remaining,
            key=lambda p: distance(
                current,
                p
            )
        )

        optimized.append(nearest)

        remaining.remove(nearest)

        current = nearest

    return optimized


def distance(p1, p2):

    """
    Distância euclidiana.
    """

    x1, y1 = p1
    x2, y2 = p2

    return math.sqrt(
        (x2 - x1) ** 2
        +
        (y2 - y1) ** 2
    )