import numpy as np

from skimage.feature import canny, blob_log
from skimage.segmentation import felzenszwalb, clear_border
from skimage.color import hed_from_rgb

from .adjust import enhance_contrast
from .ringdetect import find_ring, crop_to_ring

__all__ = [
    'remove_background',
    'detect_sections_rough',
    'detect_sections_blob'
]


def remove_background(image, enhance_contrast_kws=None,
                      canny_kws=None, find_ring_kws=None):
    """Remove background from optical overview image

    Parameters
    ----------
    image : 2D (RGB or BW) array
        Input optical overview image
    enhance_contrast_kws : dict (optional)
        Keyword arguments for `enhance_contrast`
    canny_kws : dict (optional)
        Keyword arguments for Canny edge detector
    find_ring_kws : dict (optional)
        Keyword arguments for `find_ring`

    Returns
    -------
    imcr : 2D (RGB or BW) array
        Input image with removed background
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

    # Enhance contrast
    imec = enhance_contrast(imin, **enhance_contrast_kws)
    # Canny edge detector for ring detection
    imcn = canny(imec, **canny_kws)
    # Find ring from edges and extract paramters (center coords, radius)
    cx, cy, r = find_ring(imcn, **find_ring_kws)
    # Crop to ring and remove background
    imcr = crop_to_ring(imin, cx=cx, cy=cy, radius=r)
    return imcr


def detect_sections_rough(image, felzenszwalb_kws=None, clear_border_kws=None):
    """Detect sections using Felzenszwalb segmentation

    Parameters
    ----------
    image : 2D (RGB or BW) array
        Input optical overview image
    felzenszwalb_kws : dict (optional)
        Keyword arguments for Felzenswalb segmentation
    clear_border_kws : dict (optional)
        Keyword arguments for `clear_border`

    Returns
    -------
    imcb : 2D (RGB or BW) array
        Segmented image in which the intensity levels correspond to unique,
        detected sections
    """
    # Make unnecessary copy of input image to preserve it
    imin = image.copy()

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

    # Remove background
    imcr = remove_background(imin)
    # Felzenswalb segmentation
    imfz = felzenszwalb(imcr, **felzenszwalb_kws)
    # Clear segments around border
    imcb = clear_border(imfz, **clear_border_kws)
    return imcb

def detect_sections_blob(image, blob_log_kws=None):
    """Detect sections using Laplacian of Gaussian blob analysis

    Parameters
    ----------
    image : 2D (RGB or BW) array
        Input optical overview image
    blob_log_kws : dict
        Keyword arguments for `blob_log`

    Returns
    -------
    blobs : 2D BW array
        Detected blobs
    """
    # Make unnecessary copy of input image to preserve it
    imin = image.copy()

    # Set default parameters for ``
    if blob_log_kws is None:
        blob_log_kws = {}
    blob_log_kws.setdefault('min_sigma', 8)
    blob_log_kws.setdefault('max_sigma', 12)
    blob_log_kws.setdefault('num_sigma', 3)
    blob_log_kws.setdefault('threshold', 0.1)
    blob_log_kws.setdefault('overlap', 0.2)

    # Remove background
    imcr = remove_background(imin)

    # Get rough segmentation to use as mask
    imfz = felzenszwalb(imcr, scale=750, sigma=1,
                        min_size=500, multichannel=True)
    imcb = clear_border(imfz, buffer_size=50)
    mask = imcb > 0

    # Apply mask to enhanced overview image
    imec = secdetect.enhance_contrast(imcr, channel=2,
                                      conv_matrix=hed_from_rgb)
    masked = np.where(mask, imec, 0)

    # Blob analysis
    blobs = blob_log(masked, **blob_log_kws)
    return blobs
