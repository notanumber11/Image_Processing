from __future__ import division
import cv2

from SymbolsProcessing.SymbolsSamples.Sample import Sample
from SymbolsProcessing.SymbolsSamples.SampleClub import SampleClub
from SymbolsProcessing.SymbolsSamples.SampleDiamond import SampleDiamond
from SymbolsProcessing.SymbolsSamples.SampleHeart import SampleHeart
from SymbolsProcessing.SymbolsSamples.SampleSpade import SampleSpade
from Utilities.preprocessing import Preprocessing


class ClasifyCandidates:
    thresholdArea = 50
    thresholdSize = 0.1
    font = cv2.FONT_HERSHEY_SIMPLEX
    symbolsColour = (0, 255, 255)
    idColour = (0, 255, 0)


    pathClub = "SampleImages/sample_clubs2.jpg"
    pathDiamond = "SampleImages/sample_diamonds2.jpg"
    pathHeart = "SampleImages/sample_hearts2.jpg"
    pathSpades = "SampleImages/sample_spades2.jpg"

    # List of symbols
    symbols = ['spades', 'clubs', 'heart', 'diamond']

    def __init__(self, pathClub = pathClub,pathDiamond = pathDiamond,pathHeart = pathHeart,pathSpades=pathSpades):

        # SampleImages
        img, gray, threshold, contours = Preprocessing.preprocessingImage(pathDiamond)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        self.diamond = Sample(img,threshold,contours[0])

        img, gray, threshold, contours = Preprocessing.preprocessingImage(pathClub)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        self.clubs = Sample(img,threshold,contours[0])

        img, gray, threshold, contours = Preprocessing.preprocessingImage(pathHeart)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        self.heart = Sample(img,threshold,contours[0])

        img, gray, threshold, contours = Preprocessing.preprocessingImage(pathSpades)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        self.spades = Sample(img,threshold,contours[0])


        # List of samples
        self.listSamples = [self.spades,self.clubs,self.heart,self.diamond]
        self.sampleHeart = SampleHeart(self.heart)
        self.sampleDiamond = SampleDiamond(self.diamond)
        self.sampleClubs = SampleClub(self.clubs)
        self.sampleSpade = SampleSpade(self.spades)


    def clasifyCandidates(self, img, listSamples):

        listFinal = []
        for i, sample in enumerate(listSamples):

            flagSpades = self.isSpade(sample)

            flagClubs = self.isClub(sample)

            flagHearts = self.isHeart(sample)

            flagDiamonds = self.isDiamond(sample)

            isSymbol = flagClubs or flagDiamonds or flagHearts or flagSpades


            if isSymbol:
                listFinal.append(sample)

            # if    isSymbol:
                # self.sampleDiamond.printDiamond(sample)
                # self.sampleHeart.printHeart(sample)
                # self.sampleSpade.printSpade(sample)
                # self.sampleClubs.printClub(sample)
                # cv2.imshow("classifyCandidates.py", sample.img)
                # cv2.waitKey()

            sample.stringResult = sample.label

        return listFinal

    def showSamples(self, listSamples):
        for sample in listSamples:
            self.showSample(sample)

    def showSample(self, sample):
        cv2.imshow("sample", sample.img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def TrueXor(self, iterable):
        it = iter(iterable)
        return any(it) and not any(it)

    def printInfo(self):
        for i in range(len(self.listSamples)):
            print "------------> ", self.symbols[i]
            print 'Red = ', self.listSamples[i].percentageRed, 'Red = ', self.listSamples[i].percentageRed
            # print "Area symbol = ", self.listSamples[i].contourArea
            # print "Area rectangle ", self.listSamples[i].rectangleArea
            print "Relation area ", self.listSamples[i].relationArea
            # print "perimeter symbol = ", self.listSamples[i].contourPerimeter
            # print "perimeter rectangle ", self.listSamples[i].rectanglePerimeter
            print "Relation perimeter ", self.listSamples[i].relationPerimeter
            print "Aspect Ratio = ", self.listSamples[i].aspectRatio

    def isSpade(self, sample):
        isSpade = self.sampleSpade.isSpade(sample) and sample.bestMatchShape > self.sampleSpade.matchShape
        if isSpade :
            sample.bestMatchShape = self.sampleSpade.matchShape
            sample.label = 'S'
        return isSpade

    def isClub(self, sample):
        isClub = self.sampleClubs.isClub(sample) and sample.bestMatchShape > self.sampleClubs.matchShape
        if isClub :
            sample.bestMatchShape = self.sampleClubs.matchShape
            sample.label = 'C'
        return isClub

    def isHeart(self, sample):
        isHearts = self.sampleHeart.isHeart(sample) and sample.bestMatchShape > self.sampleHeart.matchShape
        if isHearts :
            sample.bestMatchShape = self.sampleHeart.matchShape
            sample.label = 'H'
        return isHearts

    def isDiamond(self, sample):
        isDiamond = self.sampleDiamond.isDiamond(sample) and sample.bestMatchShape > self.sampleDiamond.matchShape
        if isDiamond :
            sample.bestMatchShape = self.sampleDiamond.matchShape
            sample.label = 'D'
        return isDiamond

