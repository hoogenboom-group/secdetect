import numpy as np
from matplotlib.colors import LinearSegmentedColormap


__all__ = ['neon_cmap',
           'merge_segments']


def merge_segments(image, segments_2_merge, label=None):
    """Merge segments with fancy numpy indexing

    Parameters
    ----------
    image : array-like
        Segmented image with labels as intensity values e.g.
        [[0, 0, 1, 0],
         [2, 0, 1, 1],
         [2, 0, 1, 0],
         [0, 3, 0, 0]]

    segments_2_merge: list-like
        List of segments to merge

    label : scalar
        Label to give newly merged segment
        Defaults to lowest valued label provided

    Returns
    -------
    segments_map : array-like
        Image with merged segments

    Notes
    -----
    * Makes use of the numpy trick
    >>> a = np.array([[0, 1, 2],
                      [2, 1, 0],
                      [0, 1, 2]])
    >>> mapping = np.array([-5, 2**3, 17])
    >>> mapping[a]
    array([[-5,  8, 17],
           [17,  8, -5],
           [-5,  8, 17]])

    References
    ----------
    [1] https://stackoverflow.com/a/57916846/5285918
    """
    # Set label if not provided
    if label is None:
        label = min(segments_2_merge)
    segments_map = np.arange(np.max(image) + 1)
    segments_map[segments_2_merge] = label
    # Tricky index remapping
    return segments_map[image]


def neon_cmap():
    """Create a colormap with super bright colors above a black background"""
    # Create neon colormap
    base_colors = ['#000000',  # black
                   '#ff99aa',  # pink
                   '#ffcc00',  # orange
                   '#ffff00',  # yellow
                   '#00ff00',  # green
                   '#00ddff']  # cyan
    weights = [0] + np.linspace(0, 1, len(base_colors)-1).tolist()
    weighted_colors = list(zip(weights, base_colors))
    neon = LinearSegmentedColormap.from_list("", weighted_colors)
    return neon