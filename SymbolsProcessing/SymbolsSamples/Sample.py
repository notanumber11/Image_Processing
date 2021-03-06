from __future__ import division

import cv2

import numpy as np

from Utilities import utility as aux
from Utilities.preprocessing import Preprocessing


class Sample:

    def __init__(self,img,thresh,cnt, offSetX= 0, offSetY = 0):


        self.offSetX = offSetX
        self.offSetY = offSetY


        img, gray, thresh, contours = Preprocessing.preprocessingImageFromROI(img)

        contours = sorted(contours, key=cv2.contourArea)

        if(len(contours)>1):
            cnt = contours[len(contours)-1]
        else:
            cnt = contours[0]


        self.img = img
        self.cnt = cnt
        self.thresh = thresh
        # Obtain rectangle dimensions
        self.x,self.y,self.w,self.h = cv2.boundingRect(self.cnt)

        self.cx = int(self.x + self.w / 2)
        self.cy = int(self.y + self.h / 2)

        rect = cv2.minAreaRect(self.cnt)

        box = cv2.boxPoints(rect)
        self.box = np.int0(box)

        self.bestMatchShape = 1
        self.labelMatchShape = None


        # Obtain dimensions
        self.rectangleArea = self.w * self.h
        self.rectanglePerimeter = self.w*2+self.h*2
        self.contourArea = cv2.contourArea(self.cnt)
        self.contourPerimeter = cv2.arcLength(self.cnt,True)

        self.relationArea = self.contourArea/self.rectangleArea
        self.relationPerimeter = self.contourPerimeter/self.rectanglePerimeter

        self.aspectRatio = self.w/self.h
        if (self.aspectRatio>1):
            self.aspectRatio = 1/self.aspectRatio

        # Obtain percentage of red/black
        self.percentageRed,self.percentageBlack = aux.obtainColourPercentages(self.img)

        # Init to None the features that will be calculate after
        self.label = None
        self.angle = None
        self.stringResult = None
        self.ROI = None
        self.Character = None

    def printSample(self):
        print '<<< ----------------------------------- >>>'
        # print 'Rectangle area = ',self.rectangleArea
        # print 'Rectangle perimeter = ',self.rectanglePerimeter
        # print 'Contour area = ' ,self.contourArea
        # print 'Contour perimeter = ',self.contourPerimeter
        print 'Relation area = ', self.relationArea
        print 'Relation perimeter = ', self.relationPerimeter
        print 'Aspect ratio = ', self.aspectRatio

        print 'Percentage red = ', self.percentageRed
        print 'Percentage black =', self.percentageBlack
        print '<<< ----------------------------------- >>>'

    def drawSample(self):
        # Draw contours
        # cv2.drawContours(self.img, self.contours, -1, (0, 255, 255), 2)
        cv2.imshow("DrawSample",self.img[self.y:self.y+self.h,self.x:self.x+self.w])
        cv2.waitKey()
        cv2.destroyAllWindows()