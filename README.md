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

1. Install secdetect from github repo
```
$ (secdetect) pip install git+https://github.com/lanery/secdetect.git
```
