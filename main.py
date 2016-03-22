from incdbscanner import *
import csv
import re

configPath = '/home/aeon/Proj/IncrementalDBSCAN/config'
#dataPath = '/home/aeon/Proj/IncrementalDBSCAN/abc.csv'
dataPath = '/home/aeon/Proj/IncrementalDBSCAN/AccidentData.csv'

def main():
    [Data,eps,MinPts]= getData()
    print len(Data)
    indbc= incdbscanner()
    indbc.incdbscan(Data, eps, MinPts)
def getData():
    Data = []

    with open(dataPath,'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            #row = re.split(r'\t+',row[0])
            Data.append([float(row[0]),float(row[1])])
            
    f = open(configPath,'r')
    
    [eps,MinPts] = parse(f.readline())
    
    print eps,MinPts
    
    return [Data,eps,MinPts]

def parse(line):
    data = line.split(" ")
    return [int(data[0]),int(data[1])]
    
            
    
main()    
