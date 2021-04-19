# secdetect

Small package for detecting tissue sections on ITO-coated glass

### Installation
1. Vastly overcomplicated but highly recommended environment setup with conda
```
$ conda create -n secdetect matplotlib jupyterlab shapely
$ conda activate secdetect
$ (secdetect) conda install -c conda-forge nodejs=15
$ (secdetect) pip install tqdm ipympl ipywidgets
$ (secdetect) jupyter labextension install @jupyter-widgets/jupyterlab-manager
$ (secdetect) jupyter labextension install jupyter-matplotlib
$ (secdetect) jupyter nbextension enable --py widgetsnbextension
```

2. Install secdetect from github repo
```
$ (secdetect) pip install git+https://github.com/lanery/secdetect.git
```

### Getting started
See `secdetect/notebooks/example.ipynb`

### Other resources for segmentation
* [scikit-image segmentation examples](https://scikit-image.org/docs/stable/auto_examples/#segmentation-of-objects)
  * [Watershed segmentation](https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_watershed.html#sphx-glr-auto-examples-segmentation-plot-watershed-py)
  * [Comparison of segmentation and superpixel algorithms](https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_segmentations.html#sphx-glr-auto-examples-segmentation-plot-segmentations-py)
  * [Segmenting human cells in mitosis](https://scikit-image.org/docs/stable/auto_examples/applications/plot_human_mitosis.html#sphx-glr-auto-examples-applications-plot-human-mitosis-py)

* [ilastik](https://www.ilastik.org/)
  * [Download](https://www.ilastik.org/download.html)
  * [Object classification workflow](https://www.ilastik.org/documentation/objects/objects)

* [DigitalSreeni's youtube channel](https://www.youtube.com/channel/UC34rW-HtPJulxr5wp2Xa04w/featured)
  * [Image segmentation using K-means](https://www.youtube.com/watch?v=6CqRnx6Ic48&t=461s&ab_channel=DigitalSreeni)
  * [Image segmentation using traditional machine learning](https://www.youtube.com/watch?v=OUCwt8loM6s&ab_channel=DigitalSreeni) (part 1 in a series)
  * [Image segmentation using U-net](https://www.youtube.com/watch?v=azM57JuQpQI&ab_channel=DigitalSreeni) (part 1 in a series)
