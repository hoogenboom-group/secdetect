#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 21:41:44 2018

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


def getGT(skim, sensitivity):
    GT = np.zeros((skim.shape[0], skim.shape[1]), dtype=bool)
    for i in range(0, skim.shape[0]):
        for j in range(0,skim.shape[1]):
            if skim[i,j,0] > sensitivity: 
                GT[i,j] = True
    return GT

def getResult(im):
    result = np.zeros((im.shape[0], im.shape[1]), dtype=bool)
    minR = im.min()
    for i in range(0, im.shape[0]):
        for j in range(0,im.shape[1]):
            if im[i,j] > minR: 
                result[i,j] = True
    return result

def compare(result, GT):
    pic = np.zeros((result.shape[0], result.shape[1], 3))
    if result.shape[0] == GT.shape[0] and result.shape[1] == GT.shape[1]:
        truePos = 0
        falsePos = 0
        trueNeg = 0
        falseNeg = 0
        right = 0
        wrong = 0
        for i in range(0,result.shape[0]):
            for j in range(0,result.shape[1]):
                if result[i,j] == True:
                    if GT[i,j] == True:
                        pic[i,j,1] = 1
                        truePos += 1
                        right += 1
                    else:
                        pic[i,j,0] = 1
                        pic[i,j,1] = 0.9
                        falsePos += 1
                        wrong += 1
                else: #result == False
                    if GT[i,j] == True:
                        pic[i,j,0] = 1
                        falseNeg += 1
                        wrong += 1
                    else:
                        pic[i,j,:] = 1
                        trueNeg += 1
                        right += 1
        
        fig2, (ax1) = plt.subplots(ncols= 1, nrows=1, figsize=(40, 40),sharex=False, sharey=False)
        ax1.set_title('results')
        ax1.imshow(pic)
        plt.show()
        return truePos, falsePos, trueNeg, falseNeg
    else:
        print("shapes of result and ground truth don't fit")
        return 0,0,0,0

def printResults(result, GT, GTdestination):
    truePos, falsePos, trueNeg, falseNeg = compare(result,GT)
    right = truePos+trueNeg
    wrong = falsePos +  falseNeg
    pos = truePos + falsePos
    neg = trueNeg +falseNeg
    precisionTot = right/(right+wrong)
    precisionPos = truePos/(truePos+falseNeg)
    precisionNeg = trueNeg/(trueNeg+falsePos)
    recall = truePos/(pos)
    print("picture used: ", GTdestination)
    print("HOW DID WE DO:\n ", round(100*precisionTot, 1),"% was identified correctly \n ", round(100*precisionPos, 1),"% of the positives was identified correctly \n ",round(100*precisionNeg, 1),"% of negatives was identified correctly \n ", round(100*recall, 1),"% of positives found were truly positives \n " )
    return precisionPos, recall


def compareToGT(result, GTdestination):
    GTfilename = os.path.join(skimage.data_dir, GTdestination)
    GTim = io.imread(GTfilename)
    
    resultResized = resize(result.astype(int), (GTim.shape[0], GTim.shape[1]), anti_aliasing=False)
    resultBool = getResult(resultResized)
    GT = getGT(GTim, 0)
    
    precision, recall = printResults(resultBool, GT, GTdestination)
    return precision, recall
    
    
    
    

