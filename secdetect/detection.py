import numpy as np

from skimage.feature import canny
from skimage.segmentation import felzenszwalb, clear_border
from skimage.color import hed_from_rgb

from .adjust import enhance_contrast
from .ringdetect import find_ring, crop_to_ring

__all__ = ['detect_sections']


def detect_sections(image, enhance_contrast_kws=None,
                    canny_kws=None, find_ring_kws=None,
                    felzenszwalb_kws=None, clear_border_kws=None):
    """Detect sections from optical overview image

    Parameters
    ----------
    image : ndarray
        Input optical overview image
    enhance_contrast_kws : dict (optional)
        Keyword arguments for `enhance_contrast`
    canny_kws : dict (optional)
        Keyword arguments for `canny`
    find_ring_kws : dict (optional)
        Keyword arguments for `find_ring`
    felzenszwalb_kws : dict (optional)
        Keyword arguments for `felzenswalb`
    clear_border_kws : dict (optional)
        Keyword arguments for `clear_border`

    Returns
    -------
    imcb : ndarray
        Segmented image in which the intensity levels correspond to unique,
        detected sections
    """
    # Make unnecessary copy of input image to preserve it
    imin = image.copy()

    # Set default parameters for `enhance_contrast`
    if enhance_contrast_kws is None:
        enhance_contrast_kws = {}
    enhance_contrast_kws.setdefault('clip', True)
    enhance_contrast_kws.setdefault('pct', 1.0)
    enhance_contrast_kws.setdefault('channel', 2)
    enhance_contrast_kws.setdefault('conv_matrix', hed_from_rgb)

    # Set default parameters for `canny`
    if canny_kws is None:
        canny_kws = {}
    canny_kws.setdefault('sigma', 4)
    canny_kws.setdefault('low_threshold', 0.10)
    canny_kws.setdefault('high_threshold', 0.99)
    canny_kws.setdefault('use_quantiles', True)

    # Set default parameters for `find_ring`
    if find_ring_kws is None:
        find_ring_kws = {}
    find_ring_kws.setdefault('ransac_kws', None)

    # Set default parameters for `felzenswalb`
    if felzenszwalb_kws is None:
        felzenszwalb_kws = {}
    felzenszwalb_kws.setdefault('scale', 750)
    felzenszwalb_kws.setdefault('sigma', 1.0)
    felzenszwalb_kws.setdefault('min_size', 500)
    felzenszwalb_kws.setdefault('multichannel', imin.ndim>2)

    # Set default parameters for `clear_border`
    if clear_border_kws is None:
        clear_border_kws = {}
    clear_border_kws.setdefault('buffer_size', 50)

    # Enhance contrast
    imec = enhance_contrast(imin, **enhance_contrast_kws)
    # Canny edge detector for ring detection
    imcn = canny(imec, **canny_kws)
    # Find ring from edges and extract paramters (center coords, radius)
    cx, cy, r = find_ring(imcn, **find_ring_kws)
    # Crop to ring and remove background
    imcr = crop_to_ring(imin, cx=cx, cy=cy, radius=r)
    # Felzenswalb segmentation
    imfz = felzenszwalb(imcr, **felzenszwalb_kws)
    # Clear segments around border
    imcb = clear_border(imfz, **clear_border_kws)

    return imcb
