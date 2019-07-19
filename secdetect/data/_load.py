from pathlib import Path
import random

from skimage.io import imread

data_dir = Path(__file__).absolute().parent


def load(n=None):
    """Load a sample overview image by name

    Parameters
    ----------
    n : int (optional)
        Overview image number available in `secdetect.data` as 'n.jpg'
        If not provided, image will be chosen randomly from `secdetect.data`

    Returns
    -------
    img : ndarray
        Image loaded from `secdetect.data`
    """
    if n is None:
        paths = list(data_dir.glob('*.jpg'))
        fn = random.sample(paths, 1)[0].as_posix()
    else:
        fn = (data_dir / f'{int(n):03}.jpg').as_posix()
    return imread(fn)
