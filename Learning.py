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


def runNTimesWithWeightAndGetAvgScore(N,weights, dataFileLib, dataFileName, tetris)
    clearDataFile(dataFileName)
    tetris.runNTimesWithWeightRecordToFilename(5, weights, dataFileName)
    AdataStoreList = dataFileLib.getFileDataList(dataFileName)
    avg = AdataStoreList.getAvgScore()
    return avg

def optimizeWeightsOnePass(dataFileLib, tetris, dataFileName, learningConstant, weights, num_trials):
    firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    weights.flush += learningConstant
    secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    if secondAvg < firstAvg:
        weights.flush -= (learningConstant * 2)
    firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    weights.full_line += learningConstant
    secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    if secondAvg < firstAvg:
        weights.full_line -= (learningConstant * 2)
    firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    weights.fully_enclosed += learningConstant
    secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    if secondAvg < firstAvg:
        weights.fully_enclosed -= (learningConstant * 2)
    firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    weights.multiple_enclosed += learningConstant
    secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    if secondAvg < firstAvg:
        weights.multiple_enclosed -= (learningConstant * 2)
    firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    weights.height += learningConstant
    secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    if secondAvg < firstAvg:
        weights.height -= (learningConstant * 2)
    firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    weights.second_block += learningConstant
    secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    if secondAvg < firstAvg:
        weights.second_block -= (learningConstant * 2)
    firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    weights.height_spectrum += learningConstant
    secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    if secondAvg < firstAvg:
        weights.height_spectrum -= (learningConstant * 2)
    firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    weights.enclosed_spectrum += learningConstant
    secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
    if secondAvg < firstAvg:
        weights.enclosed_spectrum -= (learningConstant * 2)
    return weights

dataFileLib = fileData_Lib()
tetris = controlTetris_lib()
dataFileName = "learningDataFile.csv"
clearDataFile(dataFileName)
weights = WeightScoreObj(0,0,0,0,0,0,0,0)
for i in range(10):
    weights = optimizeWeightsOnePass(dataFileName, tetris, dataFileName, 0.5, weights, 5) #not gonna stay 5

print("optimum weights computed, running with them now\n")
tetris.writeNewRuntimeWeightsToFile(weights)
tetris.runOnce(dataFileName)











