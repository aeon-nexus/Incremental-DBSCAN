from incdbscanner import *
import csv
import re
import sys
sys.path.append('./')

configPath = 'config'
dataPath = 'AccidentData.csv'

def main():
    [Data,eps,MinPts]= getData()
    print(len(Data))
    indbc= incdbscanner()
    indbc.incdbscan(Data, eps, MinPts)
def getData():
    Data = []

    with open(dataPath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            Data.append([float(row[0]),float(row[1])])
            
    f = open(configPath,'r')
    
    [eps,MinPts] = parse(f.readline())
    
    print(eps,MinPts)
    
    return [Data,eps,MinPts]

def parse(line):
    data = line.split(" ")
    return [int(data[0]),int(data[1])]
    
            
    
main()    
