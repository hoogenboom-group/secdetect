import numpy as np

from skimage.measure import ransac, CircleModel
from skimage.util import crop

__all__ = ['find_ring', 'crop_to_ring']


def find_ring(edges, ransac_kws=None):
    """Detects sample holder ring from edges using RANSAC

    Parameters
    ----------
    edges : ndarray
        Edges from e.g. Canny edge finder
    ransac_kws : dict (optional)
        Keyword arguments for `skimage.measure.ransac`

    Returns
    -------
    params : tuple
        Fitting parameters of detected circle as (cx, cy, r)

    References
    -----
    [1] https://stackoverflow.com/a/31708007/5285918
    [2] https://stackoverflow.com/a/28287741/5285918
    """
    # Handle ransac keywords
    if ransac_kws is None:
        ransac_kws = {}
    # Set defaults
    ransac_kws.setdefault('min_samples', 3)
    ransac_kws.setdefault('residual_threshold', 1)
    ransac_kws.setdefault('max_trials', 500)

    coords = np.column_stack(np.nonzero(edges))
    model, inliers = ransac(coords, CircleModel, **ransac_kws)
    cy, cx, r = model.params
    return (cx, cy, r)


def crop_to_ring(image, cx, cy, radius):
    """Removes background and crops image to inside of sample holder ring

    Parameters
    ----------
    image : ndarray
        Input image
    cx : int
        Center x coordinate of circle
    cy : int
        Center y coordinate of circle
    r : int
        Radius of circle

    Returns
    -------
    cropped : ndarray
        Cropped image
    """
    # Determine if multichannel
    multichannel = image.ndim > 2
    # Ensure parameters are integer
    cx = int(cx)
    cy = int(cy)
    r = int(radius)
    # Mask image
    h, w = image.shape[:2]  # get height and width of image
    Y, X = np.ogrid[:h, :w]  # create ogrid over image
    mask = (X - cx)**2 + (Y - cy)**2 > r**2  # create mask
    image[mask] = 0  # apply mask
    # Crop to square around circle
    if multichannel:  # don't crop from color axis
        crop_width = [(cy-r, h-(r+cy)), (cx-r, w-(r+cx)), (0, 0)]
    else:
        crop_width = [(cy-r, h-(r+cy)), (cx-r, w-(r+cx))]
    # Clip negative values to 0
    crop_width = np.clip(crop_width, a_min=0, a_max=None)
    cropped = crop(image, crop_width=crop_width, copy=True)
    return cropped
