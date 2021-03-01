import numpy as np
from matplotlib.colors import LinearSegmentedColormap


__all__ = ['neon_cmap']


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