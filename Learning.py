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
    def __init__(self):
        self.TestDataObjList = []
    def loadDataFromFile(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            self.TestDataObjList.append(self.parseStrLineToTDO(line))

    def parseStrLineToTDO(self, line):
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



def runNTimesWithWeight(N, WeightScoreObj):
    writeRuntimeWeightsToFile(WeightScoreObj)
    for i in range(N):
        runOnce()


#runs one test of tetris game.  Tetris game should run by using specified weights that have been written to a file, runtimeWeights.csv
#Tetris.py should be run with os.system
#Tetris.py is yet to be configured for this properly yet, but after playing around with it a few days ago, having tetris.py ran once for each game
#should make this simpler and easier
#At the end of run, tetris should write to a file and exit
def runOnce():
    os.system("py tetris.py learningDataFile.csv")

def clearLearningFile():
    open('learningDataFile.csv', 'w').close()

def getAvgScoreFromFile():
    totalSum = 0
    countLines = 0
    f = open('learningDataFile.csv', 'r')
    lines = f.readlines()
    for line in lines:
        splitted = line.strip().split(',')
        totalSum += int(splitted[0])
        countLines += 1
    if countLines == 0:
        return 0
    return totalSum / countLines


"""
write weights that tetris.py will pull from when it is running in learning mode
"""
def writeRuntimeWeightsToFile(weightStoreObj): # FORMAT: flush, full_line, fully_enclosed, multiple_enclosed, height, second_block, height_spectrum, score
    f = open("runtimeWeights.csv", "w")
    f.write(weightStoreObj.weightsToCommaSepStr())



print(getAvgScoreFromFile())
humanFoundBestWeights = WeightScoreObj(0,30,-50,-10,1,0,0.1,0.1)
clearLearningFile()
runNTimesWithWeight(3, humanFoundBestWeights)


