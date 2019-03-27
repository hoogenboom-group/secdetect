from pathlib import Path
import random

from skimage.io import imread

data_dir = Path(__file__).absolute().parent

__all__ = ['load', 'load_random',
           'load_1', 'load_2', 'load_3',
           'load_4', 'load_5', 'load_6',
           'load_7', 'load_8', 'load_9',
           'load_10', 'load_11', 'load_12',
           'load_13', 'load_14', 'load_15']


def load(name):
    """Load a sample overview image

    Parameters
    ----------
    name : str
        Overview image name

    Returns
    -------
    img : ndarray
        Image loaded from `secdetect.data`
    """
    fn = (data_dir / name).as_posix()
    return imread(fn)


def load_random():
    """Load a random sample overview image

    Returns
    -------
    img : ndarray
        Randomly selected image loaded from `secdetect.data`
    """
    fns = list(data_dir.glob('*.jpg'))
    rfn = random.sample(fns, 1)[0]
    return load(rfn.name)


def load_1():
    """Sample overview image 1

    Returns
    -------
    out :  ndarray
        (830, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('001.jpg')


def load_2():
    """Sample overview image 2

    Returns
    -------
    out :  ndarray
        (821, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('002.jpg')


def load_3():
    """Sample overview image 3

    Returns
    -------
    out :  ndarray
        (821, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('003.jpg')


def load_4():
    """Sample overview image 4

    Returns
    -------
    out :  ndarray
        (820, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('004.jpg')


def load_5():
    """Sample overview image 5

    Returns
    -------
    out :  ndarray
        (810, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('005.jpg')


def load_6():
    """Sample overview image 6

    Returns
    -------
    out :  ndarray
        (810, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('006.jpg')


def load_7():
    """Sample overview image 7

    Returns
    -------
    out :  ndarray
        (810, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('007.jpg')


def load_8():
    """Sample overview image 8

    Returns
    -------
    out :  ndarray
        (810, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('008.jpg')


def load_9():
    """Sample overview image 9

    Returns
    -------
    out :  ndarray
        (807, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('009.jpg')


def load_10():
    """Sample overview image 10

    Returns
    -------
    out :  ndarray
        (811, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('010.jpg')


def load_11():
    """Sample overview image 11

    Returns
    -------
    out :  ndarray
        (808, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('011.jpg')


def load_12():
    """Sample overview image 12

    Returns
    -------
    out :  ndarray
        (808, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('012.jpg')


def load_13():
    """Sample overview image 13

    Returns
    -------
    out :  ndarray
        (808, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('013.jpg')


def load_14():
    """Sample overview image 14

    Returns
    -------
    out :  ndarray
        (808, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('014.jpg')


def load_15():
    """Sample overview image 15

    Returns
    -------
    out :  ndarray
        (808, 1024, 3) uint8 image
        Resolution: ~25um/px
    """
    return load('015.jpg')
