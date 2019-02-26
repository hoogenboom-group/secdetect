#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 23:47:19 2018

@author: isabel
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 20:48:27 2018

@author: isabel
"""
import numpy as np
import matplotlib.pyplot as plt
import math, time, skimage, os, sys
from skimage.feature import canny
from skimage import color, exposure, io
from skimage.transform import rescale, hough_circle, hough_circle_peaks
from skimage.exposure import rescale_intensity
from skimage.draw import circle_perimeter
from skimage.segmentation import felzenszwalb
import warnings
import time


def prTrue(gt):
    trues = 0
    for i in range(gt.shape[0]):
        for j in range(gt.shape[1]):
            if gt[i,j]:
                trues += 1
    return trues/gt.size

def getGT(skim):
    sensitivity = 0
    GT = np.zeros((skim.shape[0], skim.shape[1]), dtype=bool)
    for i in range(0, skim.shape[0]):
        for j in range(0,skim.shape[1]):
            if skim[i,j,0] > sensitivity: #and skim[i,j,1] < 0.10 and skim[i,j,2] < 0.10:
                GT[i,j] = True
    return GT


def downsizeTo(im, size):
    imSize = im.shape[0]*im.shape[1]
    if (imSize > size):
        ratio = math.pow(size/imSize, 0.5)
        im = rescale(im, ratio, anti_aliasing=False) # TODO
        print("RESCALED to ", size) 
    else:
        print("NOT RESCALED")
    return im


GTdestination1 = '/Users/isabel/Documents/BEP/Ground Truths/Cropped/full_02_08_18GT.jpg'
GTdestination2 = '/Users/isabel/Documents/BEP/Ground Truths/Cropped/full_05_12_17_GT.jpg'
GTdestination3 = '/Users/isabel/Documents/BEP/Ground Truths/Cropped/full_no_idea_GT.jpg'
GTdestination4 = '/Users/isabel/Documents/BEP/Ground Truths/Cropped/full_normal_GT.jpg'

GTfilename1 = os.path.join(skimage.data_dir, GTdestination1)
GTskim1 = io.imread(GTfilename1)

GTfilename2 = os.path.join(skimage.data_dir, GTdestination2)
GTskim2 = io.imread(GTfilename2)

GTfilename3 = os.path.join(skimage.data_dir, GTdestination3)
GTskim3 = io.imread(GTfilename3)

GTfilename4 = os.path.join(skimage.data_dir, GTdestination4)
GTskim4 = io.imread(GTfilename4)




norm1 = prTrue(getGT(GTskim1))
norm2 = prTrue(getGT(GTskim2))
norm3 = prTrue(getGT(GTskim3))
norm4 = prTrue(getGT(GTskim4))

res1 = np.zeros((1,2))
res2 = np.zeros((1,2))
res3 = np.zeros((1,2))
res4 = np.zeros((1,2))

for pixsize in [0.16, 0.08, 0.04,0.03,0.02,0.01, 0.005]:
    size = int((19.15/pixsize)**2)
    GT1 = downsizeTo(GTskim1, size)
    pr = prTrue(getGT(GT1))
    res1 = np.append(res1,[[pixsize,pr]], axis = 0)
    
    GT2 = downsizeTo(GTskim2, size)
    pr = prTrue(getGT(GT2))
    res2 = np.append(res2,[[pixsize,pr]], axis = 0)
    
    GT1 = downsizeTo(GTskim3, size)
    pr = prTrue(getGT(GT1))
    res3 = np.append(res3,[[pixsize,pr]], axis = 0)
    
    GT1 = downsizeTo(GTskim4, size)
    pr = prTrue(getGT(GT1))
    res4 = np.append(res4,[[pixsize,pr]], axis = 0)