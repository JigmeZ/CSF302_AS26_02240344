"""Find the closest pair of points."""

from math import hypot


def _result(points, first, second):
    i, j = sorted((points[first][2], points[second][2]))
    distance = hypot(points[first][0] - points[second][0],
                     points[first][1] - points[second][1])
    return distance, i, j


def closest_pair_brute(points):
    """Return (distance, first_index, second_index) using every pair."""
    if len(points) < 2:
        raise ValueError("at least two points are required")

    best = None
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            candidate = (hypot(points[i][0] - points[j][0],
                               points[i][1] - points[j][1]), i, j)
            if best is None or candidate < best:
                best = candidate
    return best


def closest_pair(points):
    """Return the closest pair using divide and conquer."""
    if len(points) < 2:
        raise ValueError("at least two points are required")

    numbered = [(x, y, i) for i, (x, y) in enumerate(points)]
    by_x = sorted(numbered, key=lambda point: (point[0], point[1], point[2]))
    by_y = sorted(numbered, key=lambda point: (point[1], point[0], point[2]))

    def solve(x_points, y_points):
        if len(x_points) <= 3:
            return min((_result(x_points, i, j)
                        for i in range(len(x_points) - 1)
                        for j in range(i + 1, len(x_points))))

        middle = len(x_points) // 2
        left_x = x_points[:middle]
        right_x = x_points[middle:]
        left_ids = {point[2] for point in left_x}
        left_y = [point for point in y_points if point[2] in left_ids]
        right_y = [point for point in y_points if point[2] not in left_ids]

        left_best = solve(left_x, left_y)
        right_best = solve(right_x, right_y)
        best = min(left_best, right_best)

        middle_x = right_x[0][0]
        strip = [point for point in y_points
                 if abs(point[0] - middle_x) <= best[0]]
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):
                candidate = _result(strip, i, j)
                if candidate < best:
                    best = candidate
        return best

    return solve(by_x, by_y)

