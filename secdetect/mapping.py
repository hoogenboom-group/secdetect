import numpy as np
from scipy.spatial import ConvexHull
from shapely import affinity
from shapely.geometry import box


__all__ = ['find_minimum_bounding_rectangle']


def generate_tiles(section, field_width, overlap):

    # Aliases
    w = field_width
    o = overlap
    w_sub = w - 2*o*w

    # Convert section coordinates to x, y points
    points = section.coords[:, ::-1]  # row, col --> x, y

    # Compute minimum bounding rectangle
    rect = find_minimum_bounding_rectangle(points)
    x1, y1 = rect[0]  # right-most vertex
    x2, y2 = rect[1]  # top-most vertex
    x3, y3 = rect[2]  # left-most vertex
    x4, y4 = rect[3]  # bottom-most vertex

    # Calculate rotation
    theta = np.arctan2(y2-y3, x2-x3) + np.pi/2

    # Calculate tiling stuff
    L = np.sqrt((x1-x2)**2 + (y1-y2)**2)
    H = np.sqrt((x3-x2)**2 + (y3-y2)**2)
    Nx = int(np.ceil((L-o*w)/(w-o*w))) + 1
    Ny = int(np.ceil((H-o*w)/(w-o*w))) + 1

    # Tiles
    ii, jj = np.meshgrid(np.arange(Nx), np.arange(Ny))
    tiles = []
    subtiles = []
    for i, j in zip(ii.ravel(), jj.ravel()):

        # Tile center points
        x = x2 + i*w*(1-o)*np.cos(theta) - j*w*(1-o)*np.sin(theta)
        y = y2 + j*w*(1-o)*np.cos(theta) + i*w*(1-o)*np.sin(theta)

        # Create tiles as `shapely.box` objects and rotate
        tile = box(x-w/2, y-w/2, x+w/2, y+w/2)
        tile = affinity.rotate(tile, theta, use_radians=True)
        tiles.append(tile)

        # Create subtiles as `shapely.box` objects and rotate
        subtile = box(x-w_sub/2, y-w_sub/2, x+w_sub/2, y+w_sub/2)
        subtile = affinity.rotate(subtile, theta, use_radians=True)
        subtiles.append(subtile)

    return tiles, subtiles


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

    Notes
    -----
    * Flip coordinates if computing from a `skimage.RegionProperties` object
      >>> points = region.coords[:, ::-1]  # row, col --> x, y

    References
    ----------
    [1] https://stackoverflow.com/a/33619018/5285918
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
    rect[0] = np.dot([x1, y2], r)  # right-most vertex
    rect[1] = np.dot([x2, y2], r)  # top-most vertex
    rect[2] = np.dot([x2, y1], r)  # left-most vertex
    rect[3] = np.dot([x1, y1], r)  # bottom-most vertex

    return rect
