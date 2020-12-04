#!/usr/bin/env python3
import os
class WeightScoreObj(object): 
    def __init__(self, flush, full_line, fully_enclosed, multiple_enclosed, height, second_block, height_spectrum, enclosed_spectrum, score = None): 
        self.score = score
        self.flush = flush
        self.full_line = full_line
        self.fully_enclosed = fully_enclosed
        self.multiple_enclosed = multiple_enclosed
        self.height = height
        self.second_block = second_block
        self.height_spectrum = height_spectrum
        self.enclosed_spectrum = enclosed_spectrum
    def weightsToCommaSepStr(self):
        retstr = "%s,%s,%s,%s,%s,%s,%s,%s"
        return retstr % (self.flush, self.full_line, self.fully_enclosed, self.multiple_enclosed, self.height, self.second_block, self.height_spectrum, self.enclosed_spectrum)
    
class dataStoreList(object):

    def getAvgScore(self):
        totalSum = 0
        for n in self.internalList:
            totalSum += n.score
        return totalSum / len(self.internalList)


class controlTetris_lib(object): #just has funcs, no data storages 

    def runNTimesWithWeightRecordToFilename(self, N, WeightScoreObj, filename):
        writeRuntimeWeightsToFile(WeightScoreObj)
        for i in range(N):
            runOnce(filename)
    
    def runOnce(self, fileToWriteTo):
        os.system("py tetris.py " + fileToWriteTo)

    
    #changes the weights that tetris will use in next run if in learning mode
    def writeNewRuntimeWeightsToFile(self,  weightStoreObj): # FORMAT: flush, full_line, fully_enclosed, multiple_enclosed, height, second_block, height_spectrum, score
        f = open("runtimeWeights.csv", "w")
        f.write(weightStoreObj.weightsToCommaSepStr())

class fileData_Lib(object):

    def getFileDataList(self, filename):
        retList = []
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            retList.append(self.getFileDataListHelper(line))
        if len(retList) == 0:
            print("getFileDataList of " + filename + "read no data\n")
        return retList

    def inithelper(self, line):
        line = line.strip().split(",")
        flush = int(line[0])
        full_line = int(line[1])
        fully_enclosed = int(line[2])
        multiple_enclosed = int(line[3])
        height = int(line[4])
        second_block = int(line[5])
        height_spectrum = int(line[6])
        enclosed_spectrum = int(line[7])
        score = int(line[0])
        return WeightScoreObj(flush, full_line, fully_enclosed, multiple_enclosed, height, second_block, height_spectrum, score)
    
    def clearDataFile(self, filename):
        open(filename, 'w').close()














print(getAvgScoreFromFile())
humanFoundBestWeights = WeightScoreObj(0,30,-50,-10,1,0,0.1,0.1)
clearLearningFile()
runNTimesWithWeight(3, humanFoundBestWeights)


