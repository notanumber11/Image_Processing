from __future__ import division
import cv2
import numpy as np
import aux as aux



class Sample:

    def __init__(self,path = None, img = None, offSetX= 0, offSetY = 0):
        self.offSetX = offSetX
        self.offSetY = offSetY
        if (img == None):
            # Load image
            self.img = cv2.imread(path)
        else:
            self.img = img

        # Obtain size
        self.rows, self.cols, _ = self.img.shape
        # Gray image
        self.imgGray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # Remove noise with Gaussian
        self.imgGray = cv2.GaussianBlur(self.imgGray, (5, 5), 0)
        # Obtain black image
        self.imgBlack = aux.changeRedToBlack(self.img)
        # Threshold the image
        ret, self.imgThreshold = cv2.threshold(self.imgBlack, 90, 255, cv2.THRESH_BINARY_INV)

        # Obtain contours
        self.contours = aux.obtainContours(self.imgBlack)

        # Garantize that we have the right contour
        lenght = len(self.contours)
        i = 0
        while i<lenght:
            if(cv2.contourArea(self.contours[0])<40):
                self.contours[0] = self.contours[i]
            else:
                break
            i+=1


        # Obtain rectangle dimensions
        self.x,self.y,self.w,self.h = cv2.boundingRect(self.contours[0])
        # Obtain dimensions
        self.rectangleArea = self.w * self.h
        self.rectanglePerimeter = self.w*2+self.h*2
        self.contourArea = cv2.contourArea(self.contours[0])
        self.contourPerimeter = cv2.arcLength(self.contours[0],True)

        self.relationArea = self.contourArea/self.rectangleArea
        self.relationPerimeter = self.contourPerimeter/self.rectanglePerimeter

        self.aspectRatio = self.w/self.h
        if (self.aspectRatio>1):
            self.aspectRatio = 1/self.aspectRatio
        # Obtain percentage of red/black
        self.percentageRed,self.percentageBlack = aux.obtainColourPercentages(self.img[self.y:self.y+self.h,self.x:self.x+self.w])





        # Draw contours
        # cv2.drawContours(self.img, self.contours, -1, (0, 255, 255), 2)
        # Testing code
        # cv2.imshow("test",self.img[self.y:self.y+self.h,self.x:self.x+self.w])
        # cv2.waitKey()

