from pathlib import Path
import random

from skimage.io import imread

data_dir = Path(__file__).absolute().parent


def load(n=None):
    """Load a sample overview image by name

    Parameters
    ----------
    n : int (optional)
        Overview image number
        (0 < n < 15) in line with image files available in `secdetect.data`
        If not provided, image will be chosen randomly from `secdetect.data`

    Returns
    -------
    img : ndarray
        Image loaded from `secdetect.data`
    """
    if n is None:
        n = random.randint(0, 15)
    fn = (data_dir / f'{int(n):03}.jpg').as_posix()
    return imread(fn)
