"""
Created on Wed Nov  7 21:07:27 2018

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


def detectSections(destination):
    #input:     - overview image of the sample glass containing sections
    #output:    - a matrix to be placed as a grid over the sample glass, indicating for each cell True or False for wheter there is section
    
    #PARAMETERS TO BE ALTERED FOR DIFFERENT BATCHES:
    size = 1200000 
    sizeGlass = 19.15 #mm
    sideSection = 0.736 #mm #size of one side of the section
    delta = 0.23 #ratio
    limit = 0.5
    ratioGlassToPic = 0.8 #assuming the diameter of the sample glass is at least this much of the short side of the picture
    
    start = time.time()
    warnings.filterwarnings("ignore")
    
    filename = os.path.join(skimage.data_dir, destination)
    im = io.imread(filename)
    im = downsizeTo(im, size)
    OG = im
    imCircle = dab(im, 20)
    s = 1.5
    edgesCircle = canny(imCircle, sigma=s, low_threshold=0, high_threshold=1)
    ratioGlassToPic = 0.8
    circx, circy = findCircle(edgesCircle, ratioGlassToPic)
    im = cropToCircle(im, circx, circy)
    
    mm = im.shape[0]/sizeGlass #1mm in pixels
    sideSectionPix= sideSection*mm
    
    #FIRST METHOD
    prEdges = 1.1
    imEdges = SSI(im,prEdges)
    
    s = 1.8
    edges = canny(imEdges, sigma=s, low_threshold=0, high_threshold=1)
    edges = cropToCircle(edges, circx, circy, crop = False, returnBool = True)
    d = 0.02 #radio of blacked out circle
    edges = blackoutCircle(edges, circx, circy, d)
    
    deltaPix = delta* sideSectionPix
    check = findHalfCircle(sideSectionPix, deltaPix)
    viaEdges = selectFillEdges(edges, check, limit, deltaPix)
    
    #SECOND METHOD
    prFz = 7.6
    imFz = SSI(im,prFz, returnRGB = True)
    
    sc = sideSectionPix*20
    s = 2.4
    mins = int(sideSectionPix**2/5)
    viaFz = felzenszwalb(imFz, scale=sc, sigma=s, min_size=mins)
    
    viaFz = findSectionsFz(viaFz)
    viaFz = cropToCircle(viaFz, circx, circy, crop = False, returnBool = True)
    
    #COMBINE METHODS
    sections = overlap(viaEdges, viaFz)
    
    #DISPLAY RESULTS
    print("total ellapsed time = ", round(time.time()-start))
    fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(40, 40),sharex=False, sharey=False)
    ax1.set_title('Original picture')
    ax1.imshow(OG)
    ax2.set_title('result')
    ax2.imshow(sections, cmap = 'gray')
    
    return sections


#SUPPORTING FUNCTIONS
def blackoutCircle(edges, circx, circy, d): 
    #input:     - edges: boolean matrix cropped to sample glass, 
    #           - circx, circy: the coordinates of the circle in the original picture
    #           - d: ratio for how much needs to be blackedout/changed to False 
    #output:    - same image matrix but a range around the circle of the sample glass is made False
    
    minx = min(circx)
    miny = min(circy)
    d = math.ceil(edges.shape[0] * d)
    for i in range(0,circx.shape[0]):
        x = circx[i] - minx 
        y = circy[i] - miny
        edges[y-min(y, d):y+d,x-min(x, d):x+d] = False
    return edges


def cordLine(cor1, cor2):
    #input:     - coordinates between which a line should be drawn
    #output:    - coordinates spanning the line between the two input coordinates
    
    x1 = cor1[0,0]
    y1 = cor1[0,1]
    x2 = cor2[0,0]
    y2 = cor2[0,1]
    line = np.matrix([[x1, y1]])
    dydx = (y2-y1)/(x2-x1)
    curx = x1
    cury = y1
    lx = x1 + 0.5
    ly = y1 + 0.5
    rx = 0.5
    ry = 0.5
    negy = False
    negx = False
    Y2 = y2
    X2 = x2
    if(y1>y2):
        dydx *= -1
        negy = True
        Y2 = 2*y1 - y2
    if(x1>x2):
        dydx *= -1
        negx = True
        X2 = 2*x1 - x2
    while not (curx == X2 and cury == Y2):
        if lx - curx == 0:
            rx = 1
        else: 
            rx = 1 - (lx - curx)
        if ly - cury == 0:
            ry = 1
        else: 
            ry = 1 - (ly - cury)
        if ry > dydx*rx:
            ly += rx*dydx
            curx += 1
            lx = curx
        elif ry < dydx*rx:
            lx += ry/dydx
            cury += 1
            ly = cury
        else: #ry == dydx*rx
            curx +=1
            lx = curx
            cury +=1
            ly = cury
        if(negy):
            realCury = 2*y1-cury
        else:
            realCury = cury
        if (negx):
            realCurx = 2*x1-curx
        else:
            realCurx = curx
        line = np.append(line,[[realCurx,realCury]], axis = 0)
    return line   


def cropToCircle(im, circx, circy, crop = True, returnBool = False):
    #input:     - im: (possibly already cropped to fit around circle) image
    #           - circx, circy: x and y coordinates of the circle (in uncropped picture)
    #          (- crop: can be set to False if image does not need to be cropped)
    #          (- returnBool: can be set to True if returned unit needs to be boolean matrix instead of RGB image)
    #output:    - RGB image (/boolean matrix), which is cropped to the circle and outside the circle is set to black (/False)
    
    maxX = max(circx)
    minX = max(0, min(circx))
    maxY = max(circy)
    minY = max(0, min(circy))
    if crop:    
        cropped = im[minY:maxY,minX:maxX]
    else: 
        cropped = im
    c = sortCircle(circx, circy)
    borders = findBorderPerLine(c)
    borders -= minY
    if returnBool:
        d = np.zeros((cropped.shape[0],cropped.shape[1]), dtype= bool)
    else:
        d = np.zeros((cropped.shape[0],cropped.shape[1],3))
    if min(circx) <0:
        corx = min(circx)
    else:
        corx = 0
    for i in range(0, cropped.shape[1]):
        x = i + corx
        if x >= 0:
            y1=max(0,int(borders[i,0]))
            y2=min(cropped.shape[0],int(borders[i,1]))
            d[y1+1:y2-1,x] = cropped[y1+1:y2-1, x]
    return d


def dab(im, pr1, returnRGB = False):
    #input:     - im: image 
    #           - pr1: procentage with which intensity levels should be increased
    #output:    - dab image
    ihc_hed = color.rgb2hed(im)
    pr2 = 100-pr1
    d = rescale_intensity(ihc_hed[:, :, 2], out_range=(0, 1))
    p1, p2 = np.percentile(d, (pr1, pr2))
    d = exposure.rescale_intensity(d,in_range=(p1, p2))
    return d


def dist(x1,y1,x2,y2):
    #input:     - coordinates between which the distance should be calculated
    #output:    - the distance between the coordinates
    
    return math.pow(math.pow(x1-x2,2)+math.pow(y1-y2,2),0.5)


def downsizeTo(im, size):
    #input:     - image which need to be downsized to size
    #output:    - (possibly) downsized image
    
    imSize = im.shape[0]*im.shape[1]
    if (imSize > size):
        ratio = math.pow(size/imSize, 0.5)
        im = rescale(im, ratio, anti_aliasing=False)
    return im


def findCircle(edges, ratio):
    #input:     - edges: boolean matrix that is True for pixels containing an edge
    #           - ratio: the ratio that the radius of the circle maximum differs from the short side of the image
    #output:    - the x and y coordinates where the circle in the image can be found
    
    maxSize = int(min(edges.shape[0]/2, edges.shape[1]/2)/ratio)
    minSize = int(min(edges.shape[0]/2, edges.shape[1]/2) * ratio)
    step = 1
    hough_radii = np.arange(minSize, maxSize, step)
    hough_res = hough_circle(edges, hough_radii)
    accums, cx, cy, radius = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=1)
    circy, circx = circle_perimeter(cy[0], cx[0], radius[0])
    return circx, circy


def findHalfCircle(radius, delta):
    #input:     - the radius and delta in pixels
    #output:    - a 2 by n matrix containing all pixels in first and fourth quadrant that are within radius +/- delta distance of the origin
    
    minR = radius - delta - 0.5
    maxR = radius + delta + 0.5 
    halfCircle = np.zeros((1,2))
    for i in range(0,math.ceil(maxR)+1):
        j = 0
        distPix = dist(0,0,i,j)
        while (distPix<maxR):
            if (distPix>minR):
                halfCircle = np.append(halfCircle,[[i,j]], axis = 0)
            j+=1
            distPix = dist(0,0,i,j)
    halfCircle = np.delete(halfCircle, 0, 0)
    return halfCircle
    

def findSectionsFz(fz):
    #input:     - matrix separated into segments by numbers
    #output:    - boolean matrix indicating with True values where the input did not contain background
    sections = np.zeros((fz.shape[0], fz.shape[1]), dtype=bool)
    #detect background
    u, indices = np.unique(fz, return_inverse=True)
    background = u[np.argmax(np.bincount(indices))]
    for i in range(0, fz.shape[0]):
        for j in range(0, fz.shape[1]):
            if not fz[i,j] == background:
                sections[i,j] = True
    return sections


def overlap(viaEdges, viaFz):
    #input:     - two boolean matrices of the same size
    #output:    - boolean matrix indicating where viaEdges is True and viaFz is not background
     
    sections = np.zeros((viaEdges.shape[0], viaEdges.shape[1]), dtype=bool)
    for i in range(0, viaEdges.shape[0]):
        for j in range(0, viaEdges.shape[1]):
            if viaEdges[i,j] == True and viaFz[i,j] == True:
                sections[i,j] = True
    return sections


def selectFillEdges(edges, check, lim, delta):
    #input:     - edges: a boolean matrix containing the edges of an image
    #           - check: a 2 by n matrix of coordinates relative to each edge where one would expect there to be edge
    #           - lim: a limit for how much edge must be in the desired range from the checked edge, for it to be considered a section
    #output:    - a boolean matrix with true values for where section was detected
    
    filledEdges = np.zeros((edges.shape[0], edges.shape[1]), dtype=bool)
    for i in range(0, edges.shape[0]):
        for j in range(0, edges.shape[1]):
            if edges[i,j] == True:
                trueInRange = np.matrix([[i, j]])
                nChecked = 0
                for ch in check:
                    nChecked += 1
                    cx = ch.astype(int)[0]
                    cy = ch.astype(int)[1]
                    if cx+i<edges.shape[0] and cy+j<edges.shape[0]:
                        if edges[cx+i,cy+j] == True:
                            trueInRange = np.append(trueInRange,[[cx+i,cy+j]], axis = 0)
                    if -cx+i<edges.shape[0] and cy+j<edges.shape[0]:
                        if edges[-cx+i,cy+j] == True:
                            trueInRange = np.append(trueInRange,[[-cx+i,cy+j]], axis = 0)
                pr = trueInRange.shape[0]/nChecked
                if pr > lim/delta:
                    cor1 = trueInRange[0,:]
                    filledEdges[cor1[0,0], cor1[0,1]] = True
                    for k in range(1,trueInRange.shape[0]):
                        line = cordLine(cor1, trueInRange[k,:])
                        for cor in line:
                            px = cor[0,0]
                            py = cor[0,1]
                            filledEdges[px,py] = True
    return filledEdges


def SSI(im, pr1, returnRGB = False):
    #input:     - im: image that needs to be increased in contrast through stain separation
    #           - pr1: procentage with which intensity levels should be increased
    #          (- returnRGB: set to True if the returned image needs to be RGB instead of black and white)
    #output:    - (possibly RGB) contrast increased image
    
    ihc_hed = color.rgb2hed(im)
    h = rescale_intensity(ihc_hed[:, :, 0], out_range=(0, 1))
    d = rescale_intensity(ihc_hed[:, :, 2], out_range=(0, 1))
    maxd = d.max()
    zdh = np.dstack((np.zeros_like(h), maxd-d, h))
    if returnRGB == False:   
        zdh = h-d
    pr2 = 100-pr1
    p1, p2 = np.percentile(zdh, (pr1, pr2))
    zdh = exposure.rescale_intensity(zdh,in_range=(p1, p2))
    return zdh


def sortCircle(cx,cy):
    #input:     - x and y coordinates that need to be sorted
    #output:    - 2 by n matrix, sorted by x
    
    d = np.zeros((cx.size,2))
    d[:,0] = cx
    d[:,1] = cy
    d = d[d[:,0].argsort()]
    return d

def findBorderPerLine(c): 
    #input:     - 2 by n matrix containing x and y coordinates, sorted by x
    #output:    - 2 by m (=< n) matirx with for each unique x in the input the minimal and maximal y values
    
    maxX = max(c[:,0])
    minX = min(c[:,0])
    maxY = max(c[:,1])
    numLines = int(maxX - minX + 1)
    d = np.zeros((numLines,2))
    i = 0
    j = 0
    while (i < (c.shape[0])):
        l = c[i,0]
        line = l
        y1 = maxY
        y2 = 0
        while (l == line):
            check = c[i,1]
            if (check< y1):
                y1 = check
            if (check> y2):
                y2 = check
            i += 1
            if (i < c.shape[0]):
                l = c[i,0]
            else:
                l +=1
        d[j, :] = (y1,y2)
        j +=1
    return d