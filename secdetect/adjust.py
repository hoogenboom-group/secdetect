import numpy as np

from skimage import img_as_float
from skimage.exposure import rescale_intensity
from skimage.color import separate_stains
from skimage.transform import rescale


__all__ = ['scale',
           'clip_intensity',
           'enhance_contrast']


def scale(image, scale_src, scale_tgt=10, rescale_kws=None):
    """Scale overview image to desired um/px
    
    Parameters
    ----------
    image : ndarray
        Input image
    scale_src : float
        Scale of source image in um/px
    scale_tgt : float (optional)
        Desired scale of output image
    rescale_kws : dict (optional)
        Keyword arguments for `skimage.transform.rescale`
    
    Returns
    -------
    out : ndarray
        Downscaled image
    """
    multichannel = image.ndim > 2
    # Handle rescale keywords
    if rescale_kws is None:
        rescale_kws = {}
    # Set defaults
    rescale_kws.setdefault('order', 3)
    rescale_kws.setdefault('mode', 'reflect')
    rescale_kws.setdefault('multichannel', multichannel)
    rescale_kws.setdefault('anti_aliasing', True)

    s = scale_src / scale_tgt
    out = rescale(image, scale=s, **rescale_kws)
    return out


def clip_intensity(image, pct=1):
    """Clips intensity levels by a given percentage

    Parameters
    ----------
    image : ndarray
        Input image
    pct : scalar
        Percentage by which to clip intensity

    Returns
    -------
    out : ndarray
        Rescaled image with dtype float

    Notes
    -----
    * For rgb or multichannel images, clips intensity levels within each 
      channel rather than wrt to the whole image
    """
    image = img_as_float(image)
    multichannel = image.ndim > 2
    if not multichannel:
        p1, p2 = np.percentile(image, (pct, 100-pct))
        out = rescale_intensity(image, in_range=(p1, p2))
    else:
        out = np.dstack([clip_intensity(im.T, pct=pct) for im in image.T])
    return out


def enhance_contrast(image, clip=True, pct=1, channel=None, conv_matrix=None):
    """Enhance contrast of input image

    Parameters
    ----------
    image : ndarray
        Input image
    clip : bool
        Whether to clip the intensity levels
    pct : scalar
        Percentage by which to clip intensity
    channel : int (or None)
        Which channel (R, B, G) to return 
        (post-deconvolution if `conv_matrix` is given)
        Should be the case that `channel < image.ndim`
    conv_matrix : ndarray
        Stain separation matrix as described by G. Landini [1]

    Returns
    -------
    out : ndarray
        Enhanced contrast image

    References
    ----------
    [1] http://www.mecourse.com/landinig/software/software.html
    """
    out = img_as_float(image)
    multichannel = image.ndim > 2
    # Deconvolve colors if given a convolution matrix
    if multichannel and conv_matrix is not None:
        multichannel = True
        out = separate_stains(out, conv_matrix)
    # Convert to greyscale if given a channel
    if channel is not None:
        out = out[:, :, channel]
    # Clip intensity levels
    if clip:
        out = clip_intensity(out, pct)
    return rescale_intensity(out, out_range=(0.0, 1.0))
