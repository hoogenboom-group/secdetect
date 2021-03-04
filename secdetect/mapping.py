import numpy as np
from scipy.spatial import ConvexHull


__all__ = ['find_minimum_bounding_rectangle']


def find_minimum_bounding_rectangle(points):
    """Find the smallest possible rectangle that encloses the convex hull

    Parameters
    ----------
    points : (M, 2) array
        Points about which to find the minimum bounding rectangle

    Returns
    -------
    rect : (4, 2) array
        Vertices of the minimum bounding rectangle

    References
    ----------
    [1] https://stackoverflow.com/a/33619018/5285918

    Notes
    -----
    * Flip coordinates if computing from a `skimage.RegionProperties` object
      >>> points = region.coords[:, ::-1]  # row, col --> x, y
    """

    # Compute convex hull
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]

    # Calculate edge angles
    edges = np.zeros((len(hull_points)-1, 2))
    edges = hull_points[1:] - hull_points[:-1]
    angles = np.zeros((len(edges)))
    angles = np.arctan2(edges[:, 1], edges[:, 0])
    angles = np.abs(np.mod(angles, np.pi/2))
    angles = np.unique(angles)

    # Find rotation matrices
    rotations = np.stack([
        np.cos(angles),
        np.cos(angles - np.pi/2),
        np.cos(angles + np.pi/2),
        np.cos(angles)
    ]).T.reshape(-1, 2, 2)

    # Apply rotations to the hull
    rotation_points = np.dot(rotations, hull_points.T)

    # Find the bounding points
    min_x = np.nanmin(rotation_points[:, 0], axis=1)
    max_x = np.nanmax(rotation_points[:, 0], axis=1)
    min_y = np.nanmin(rotation_points[:, 1], axis=1)
    max_y = np.nanmax(rotation_points[:, 1], axis=1)

    # Find the box with the smallest area
    areas = (max_x - min_x) * (max_y - min_y)
    idx_min = np.argmin(areas)

    # Return the best box
    x1 = max_x[idx_min]
    x2 = min_x[idx_min]
    y1 = max_y[idx_min]
    y2 = min_y[idx_min]
    r = rotations[idx_min]

    # Create minimum bounding rectangle
    rect = np.zeros((4, 2))
    rect[0] = np.dot([x1, y2], r)
    rect[1] = np.dot([x2, y2], r)
    rect[2] = np.dot([x2, y1], r)
    rect[3] = np.dot([x1, y1], r)

    return rect
