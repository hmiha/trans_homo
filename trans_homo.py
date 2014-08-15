#!/usr/bin/env python

import sys
import cv2
import numpy as np
import argparse

# -- Using argparse --

parser = argparse.ArgumentParser(description = "Image translater using Homography matrix.")
parser.add_argument("-n", help = "File name")
parser.add_argument("-dh", help = "Height of destination image")
parser.add_argument("-dw", help = "Width of destination image")
args = parser.parse_args()

imgName = args.n
d_h = int(args.dh)
d_w = int(args.dw)


# -- Global Valiables --
it = 0 
src_pt = np.zeros((4,2))


# -- Draw circle in selected point

def homographySolver(src_pt, dst_pt):

    s = np.zeros((4, 3)) 
    d = np.zeros((4, 3)) 
    A = np.zeros((8, 9)) 
    b = np.zeros((9)) 
  
    for i in range(4):
        s[i][:] = (src_pt[i][0], src_pt[i][1], 1)
        d[i][:] = (dst_pt[i][0], dst_pt[i][1], 1)

    for i in range(4):
        A[ 2 * i][:] = ((s[i][0], s[i][1], 1, 0, 0, 0, -d[i][0]*s[i][0], -d[i][0]*s[i][1], -d[i][0]))
        A[ 2 * i + 1][:] = ((0, 0, 0, s[i][0], s[i][1], 1, -d[i][1]*s[i][0], -d[i][1]*s[i][1], -d[i][1]))

    l,v = np.linalg.eig(np.dot(A.T, A))

    i = np.argmin(l)

    
    for j in range(9):
        v[j][i] = v[j][i]/v[8][i]

    H = v[:,i].reshape((3,3))

    print "Homography Matrix"
    print H
    return H

def circleDrawer(x, y, src_img):

    center = (x, y)
    r = 10
    color = (255, 0, 0)
    cv2.circle(src_img, center, r, color)
    
# -- on mouse function
def onMouse(event, x, y, flags, param):
   
    global it, src_pt 

    if event == cv2.EVENT_LBUTTONDOWN:

        # -- draw circles in clicked point -- 
        circleDrawer(x, y, src_img)

        # -- get src points --
        src_pt[it][:] = x, y

        # -- count -- 
        it += 1
       
        cv2.imshow(windowName, src_img)

def pointDisplay(pt):

    print "Upper-left:  (", pt[0][0] , pt[0][1], ")"
    print "Upper-right: (", pt[1][0] , pt[1][1], ")"
    print "Lower-right: (", pt[2][0] , pt[2][1], ")"
    print "Lower-left:  (", pt[3][0] , pt[3][1], ") \n"

def getDstPoints(d_h, d_w):

    dst_pt = np.array([
        [0.  , d_h],
        [0.  , 0. ],
        [d_w , 0. ],
        [d_w , d_h]
        ])

    return dst_pt

def getHomography(src_pt, dst_pt):

    hcv = homographySolver(src_pt, dst_pt)
    #hcv_cv, mask = cv2.findHomography(src_pt, dst_pt)
    #print "cv"
    #print hcv_cv

    src_img = cv2.imread(imgName, 1)
    dst_img = cv2.warpPerspective(src_img, hcv, (d_w, d_h))
    #dst_img = cv2.warpPerspective(src_img, hcv, (4, 4))

    cv2.namedWindow("dst")
    cv2.imshow("dst", dst_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":

    src_img = cv2.imread(imgName, 1)

    # -- display usage --
    usage = "Click points from upper-left points of object. \n"
    usage = usage + "After select 4 points, press any key. \n"
    print(usage)

    # -- make new window --
    windowName = "Src_Img"
    cv2.namedWindow(windowName)

    # -- callBack -- 
    if it <= 3:
        cv2.setMouseCallback(windowName, onMouse)

    """
    src_pt[0][:] = 1.0, 1.0 
    src_pt[1][:] = 1.0, -1.0 
    src_pt[2][:] = -1.0, 1.0 
    src_pt[3][:] = -1.0, -1.0 
    """

    cv2.imshow(windowName, src_img)
    cv2.waitKey(0)

    # -- after get 4 points --

    print "** Sourse Points ** "
    pointDisplay(src_pt)

    cv2.destroyAllWindows()

    dst_pt = getDstPoints(d_h, d_w)
    """
    dst_pt = np.array([
        [4.0  , 4.0],
        [4.0  , -4.0],
        [-4.0 , 4.0],
        [-4.0 , -4.0]
        ])
    """




    print "** Translated Points ** "
    pointDisplay(dst_pt)

    getHomography(src_pt, dst_pt)
