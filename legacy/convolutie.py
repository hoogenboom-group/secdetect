#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 01:43:53 2018

@author: isabel
"""

import numpy as np
import matplotlib.pyplot as plt
import math, skimage, os
from skimage.feature import canny
from skimage import color, exposure, io
from skimage.transform import rescale, hough_circle, hough_circle_peaks
from skimage.exposure import rescale_intensity
from skimage.draw import circle_perimeter
from skimage.segmentation import felzenszwalb
import warnings
import time
from skimage.transform import resize


def trySomething1(im):
    result = np.zeros((im.shape[0], im.shape[1],3))
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            b = im[i,j,0]*2.51913-im[i,j,1]*8.81729+im[i,j,2]*6.52976
            s = -im[i,j,0]*26.07505+im[i,j,1]*34.48833-im[i,j,2]*5.97303
            #print(b, s)
            result[i,j,0] = b/2.55
            result[i,j,1] = s/2.55
    fig2, (ax1, ax2, ax3) = plt.subplots(ncols=3, nrows=1, figsize=(40, 40),sharex=False, sharey=False)
    ax1.set_title('Try1')
    ax1.imshow(result[:,:,0]-result[:,:,1])
    ax2.set_title('backgr')
    ax2.imshow(result[:,:,0])
    ax3.set_title('section')
    ax3.imshow(result[:,:,1])
    return result

def trySomething2(im):
    result = np.zeros((im.shape[0], im.shape[1],3))
    
    
    
    
    
    #VERKEERD OM
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            b = im[i,j,0]*2.51913-im[i,j,1]*26.07505+im[i,j,2]*27.26978
            s = -im[i,j,0]*8.81729+im[i,j,1]*34.48833-im[i,j,2]*27.59455
            #print(b, s)
            result[i,j,0] = b/2.55
            result[i,j,1] = s/2.55
    fig2, (ax1, ax2, ax3) = plt.subplots(ncols=3, nrows=1, figsize=(40, 40),sharex=False, sharey=False)
    ax1.set_title('Try2')
    ax1.imshow(result[:,:,0]-result[:,:,1])
    ax2.set_title('backgr')
    ax2.imshow(result[:,:,0])
    ax3.set_title('section')
    ax3.imshow(result[:,:,1])
    return result

def trySomething3(im):
    #VERKEERD OM
    result = np.zeros((im.shape[0], im.shape[1],3))
    A = 8.63977
    B = 38.41277
    C = -26.42680
    D = -15.01082
    E = -30.76751
    F = 26.74153
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            b = im[i,j,0]*A+im[i,j,1]*B+im[i,j,2]*C
            s = im[i,j,0]*D+im[i,j,1]*E+im[i,j,2]*F
            #print(b, s)
            result[i,j,0] = b/2.55
            result[i,j,1] = s/2.55
    fig2, (ax1, ax2, ax3) = plt.subplots(ncols=3, nrows=1, figsize=(40, 40),sharex=False, sharey=False)
    ax1.set_title('Try3')
    ax1.imshow(result[:,:,0]-result[:,:,1])
    ax2.set_title('backgr')
    ax2.imshow(result[:,:,0])
    ax3.set_title('section')
    ax3.imshow(result[:,:,1])
    return result


def trySomething4(im):
    result = np.zeros((im.shape[0], im.shape[1],3))
    A = 8.63977
    B = -15.01082
    C = 6.37105
    D = 38.41277
    E = -30.76751
    F = -7.64526
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            b = im[i,j,0]*A+im[i,j,1]*B+im[i,j,2]*C
            s = im[i,j,0]*D+im[i,j,1]*E+im[i,j,2]*F
            #print(b, s)
            result[i,j,0] = b
            result[i,j,1] = s
    fig2, (ax1, ax2, ax3) = plt.subplots(ncols=3, nrows=1, figsize=(40, 40),sharex=False, sharey=False)
    ax1.set_title('Try4')
    ax1.imshow(result[:,:,0]-result[:,:,1], cmap = 'gray')
    ax2.set_title('backgr')
    ax2.imshow(result[:,:,0])
    ax3.set_title('section')
    ax3.imshow(result[:,:,1])
    
    res2 = result
    
    fig1, (ax1,ax2) = plt.subplots(ncols=2, nrows=1, figsize=(40, 40),sharex=False, sharey=False)
    ax1.set_title('color combi')
    print(res2[:,:,0].min(), res2[:,:,1].min(), res2[:,:,0].max(), res2[:,:,1].max())
    res2[:,:,0] -= res2[:,:,0].min()
    print(res2[:,:,0].min(), res2[:,:,1].min(), res2[:,:,0].max(), res2[:,:,1].max())
    res2[:,:,0] /= res2[:,:,0].max()
    print(res2[:,:,0].min(), res2[:,:,1].min(), res2[:,:,0].max(), res2[:,:,1].max())
    res2[:,:,1] -= res2[:,:,1].min()
    print(res2[:,:,0].min(), res2[:,:,1].min(), res2[:,:,0].max(), res2[:,:,1].max())
    res2[:,:,1] /= res2[:,:,1].max()
    print(res2[:,:,0].min(), res2[:,:,1].min(), res2[:,:,0].max(), res2[:,:,1].max())
    
    pr1 = 25
    pr2 = 100-pr1
    p1, p2 = np.percentile(result, (pr1, pr2))
    
    res2 = exposure.rescale_intensity(result,in_range=(p1, p2))
    ax1.imshow(res2)
    ax2.set_title("gray, difference")
    ax2.imshow(res2[:,:,0]-res2[:,:,1], cmap = 'gray')
    
    
    return result


def trySomething5(im):
    result = np.zeros((im.shape[0], im.shape[1],3))
    A = 9.23485
    B = -16.04472
    C = 6.80987
    D = 41.05853
    E = -32.88668
    F = -8.17184
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            b = im[i,j,0]*A+im[i,j,1]*B+im[i,j,2]*C
            s = im[i,j,0]*D+im[i,j,1]*E+im[i,j,2]*F
            #if i*j%100 == 0:
                #print(b, s)
            result[i,j,0] = b
            result[i,j,1] = s
    
    res2 = result
    res2[:,:,0] -= res2[:,:,0].min()
    res2[:,:,0] /= res2[:,:,0].max()
    res2[:,:,1] -= res2[:,:,1].min()
    res2[:,:,1] /= res2[:,:,1].max()
    
    fig2, (ax1, ax2, ax3) = plt.subplots(ncols=3, nrows=1, figsize=(40, 40),sharex=False, sharey=False)
    ax1.set_title('Background-EPON space image')
    ax1.imshow(res2)
    ax2.set_title('backgr')
    ax2.imshow(result[:,:,0])
    ax3.set_title('section')
    ax3.imshow(result[:,:,1])
    
    result = result[:,:,0]-result[:,:,1]
    pr1 = 15.5
    pr2 = 100-pr1
    p1, p2 = np.percentile(result, (pr1, pr2))
    res2 = exposure.rescale_intensity(result,in_range=(p1, p2))
    fig1, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(40, 40),sharex=False, sharey=False)
    
    ax1.set_title("gray, difference")
    ax1.imshow(result, cmap = 'gray')
    ax2.set_title("gray, difference, increased contrast")
    ax2.imshow(res2, cmap = 'gray')
    
    
    return result