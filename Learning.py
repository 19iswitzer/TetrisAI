#!/usr/bin/env python3
import random
import os
class WeightScoreObj(object): 
    def __init__(self, flush, full_line, fully_enclosed, multiple_enclosed, height, second_block, height_spectrum, enclosed_spectrum, score=None):
        self.flush = flush
        self.full_line = full_line
        self.fully_enclosed = fully_enclosed
        self.multiple_enclosed = multiple_enclosed
        self.height = height
        self.second_block = second_block
        self.height_spectrum = height_spectrum
        self.enclosed_spectrum = enclosed_spectrum
        self.score = score
    def weightsToCommaSepStr(self):
        retstr = "%s,%s,%s,%s,%s,%s,%s,%s"
        return retstr % (self.flush, self.full_line, self.fully_enclosed, self.multiple_enclosed, self.height, self.second_block, self.height_spectrum, self.enclosed_spectrum)
    
class dataStoreList(object):

    def __init__(self, internalList):
        self.internalList = internalList

    def getAvgScore(self):
        totalSum = 0
        for n in self.internalList:
            totalSum += n.score
        return totalSum / len(self.internalList)
    
    def print(self):
        for n in self.internalList:
            print(n.weightsToCommaSepStr())


class controlTetris_lib(object): #just has funcs, no data storages 

    def runNTimesWithWeightRecordToFilename(self, N, WeightScoreObj, filename):
        self.writeNewRuntimeWeightsToFile(WeightScoreObj)
        for i in range(N):
            self.runOnce(filename)
    
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
            line = line.strip()
            wso = self.getFileDataListHelper(line)
            retList.append(wso)
        if len(retList) == 0:
            print("getFileDataList of " + filename + "read no data")

        ret_FDLIST = dataStoreList(retList)
        return ret_FDLIST

    def getFileDataListHelper(self, line):
        line = line.strip().split(",")
        flush = float(line[1])
        full_line = float(line[2])
        fully_enclosed = float(line[3])
        multiple_enclosed = float(line[4])
        height = float(line[5])
        second_block = float(line[6])
        height_spectrum = float(line[7])
        enclosed_spectrum = float(line[8])
        score = int(line[0])
        ret = WeightScoreObj(flush, full_line, fully_enclosed, multiple_enclosed, height, second_block, height_spectrum, enclosed_spectrum, score)
        return ret
    
    def clearDataFile(self, filename):
        open(filename, 'w').close()


def runNTimesWithWeightAndGetAvgScore(N,weights, dataFileLib, dataFileName, tetris):
    dataFileLib.clearDataFile(dataFileName)
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

def optimizeWeightsOnePassRandom(dataFileLib, tetris, dataFileName, learningConstant, weights, num_trials):
    weightNum = random.randrange(8)
    if weightNum == 0:
        firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        weights.flush += learningConstant
        secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        if secondAvg < firstAvg:
            weights.flush -= (learningConstant * 2)
    elif weightNum == 1:
        firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        weights.full_line += learningConstant
        secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        if secondAvg < firstAvg:
            weights.full_line -= (learningConstant * 2)
    elif weightNum == 2:
        firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        weights.fully_enclosed += learningConstant
        secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        if secondAvg < firstAvg:
            weights.fully_enclosed -= (learningConstant * 2)
    elif weightNum == 3:
        firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        weights.multiple_enclosed += learningConstant
        secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        if secondAvg < firstAvg:
            weights.multiple_enclosed -= (learningConstant * 2)
    elif weightNum == 4:
        firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        weights.height += learningConstant
        secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        if secondAvg < firstAvg:
            weights.height -= (learningConstant * 2)
    elif weightNum == 5:
        firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        weights.second_block += learningConstant
        secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        if secondAvg < firstAvg:
            weights.second_block -= (learningConstant * 2)
    elif weightNum == 6:
        firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        weights.height_spectrum += learningConstant
        secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        if secondAvg < firstAvg:
            weights.height_spectrum -= (learningConstant * 2)
    else:
        firstAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        weights.enclosed_spectrum += learningConstant
        secondAvg = runNTimesWithWeightAndGetAvgScore(num_trials, weights, dataFileLib, dataFileName, tetris)
        if secondAvg < firstAvg:
            weights.enclosed_spectrum -= (learningConstant * 2)
    return weights

dataFileLib = fileData_Lib()
tetris = controlTetris_lib()
dataFileName = "learningDataFile.csv"
dataFileLib.clearDataFile(dataFileName)
weights = WeightScoreObj(0,0,0,0,0,0,0,0)
for i in range(10):
    print("pass: " + str(i))
    print(weights.weightsToCommaSepStr())  # 0.5 = learning const, 5 = number trials for each weights
    weights = optimizeWeightsOnePassRandom(dataFileLib, tetris, dataFileName, 0.5, weights, 5) 
print("optimum weights computed, running with them now")
print("optimum Weights:")
print(weights.weightsToCommaSepStr())
tetris.writeNewRuntimeWeightsToFile(weights)
tetris.runOnce(dataFileName)












