import math
import json
import re
import statistics
import argparse

def getUser(x):
    b = re.search('(.+?)/',x).end()
    return (int(x[:b-1]))



def sumA(vectors,approximation):
    x=0
    y=0
    d=0
    for vector in vectors:
        y += vector[0] / math.sqrt((vector[0]-approximation[0] )**2 + (vector[1]-approximation[1])**2)
        x += vector[1] / math.sqrt((vector[0]-approximation[0])**2 + (vector[1]-approximation[1])**2)
    for vector in vectors:
       d += 1 / math.sqrt((vector[0]-approximation[0])**2 + (vector[1]-approximation[1])**2)
    return ([ y/d, x/d ] )

def weiszfeldApproximation(vectors):
    y = [300,300] ##This can be whatever
    err = 1
    while(err>0.01):
        y1 = sumA(vectors,y)
        err = math.sqrt((y[0]-y1[0] )**2 + (y[1]-y1[1])**2) 
        y = y1
    return y

def pointsDistances(points,median):
    result = []
    for point in points:
      result.append(math.sqrt((point[0]-median[0])**2+(point[1]-median[1])**2))
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("file")
    args = parser.parse_args()
    
    dictTest = {}
    a = json.load(open(args.path+args.file))
    for x in range(1, len(a)//24 + 1): dictTest[str(x)] = [a[key] for key in a if getUser(key)==x  ]

    
    dict1 = {}
    for i in range (1,len(a)//24 + 1): 
        dAvgStdH = []
        mediansH = []
        for p in range(0,31):  
            points = [dictTest[str(i)][x]['hPoints'][p] for x in range(0,24) ]
            median = weiszfeldApproximation(points)
            d = pointsDistances(points,median)
            dAvgStdH.append( (statistics.mean(d),statistics.stdev(d)))
            mediansH.append(median)
        tresholdH = 0
        for p in dAvgStdH:
            tresholdH += (p[0] + p[1] )**2
        tresholdH = math.sqrt(tresholdH)
        
        dAvgStdV = []
        mediansV = []
        for p in range(0,31):  
            points = [dictTest[str(i)][x]['vPoints'][p] for x in range(0,24) ]
            median = weiszfeldApproximation(points)
            d = pointsDistances(points,median)
            dAvgStdV.append( (statistics.mean(d),statistics.stdev(d)))
            mediansV.append(median)
        tresholdV = 0
        for p in dAvgStdV:
            tresholdV += (p[0] + p[1] )**2
        tresholdV = math.sqrt(tresholdV)
        dict1[str(i)] = { 'vertical':[mediansV,tresholdV],'horizontal':[mediansH,tresholdH]  }
    
    dict2 = {}
    for i in range (1,len(a)//24 + 1): 
        dAvgStdH = []
        mediansH = []
        for p in range(0,31):  
            points = [dictTest[str(i)][x]['hPoints'][p] for x in range(0,18) ]
            median = weiszfeldApproximation(points)
            d = pointsDistances(points,median)
            dAvgStdH.append( (statistics.mean(d),statistics.stdev(d)))
            mediansH.append(median)
        tresholdH = 0
        for p in dAvgStdH:
            tresholdH += (p[0] + p[1] )**2
        tresholdH = math.sqrt(tresholdH)
        
        dAvgStdV = []
        mediansV = []
        for p in range(0,31):  
            points = [dictTest[str(i)][x]['vPoints'][p] for x in range(0,18) ]
            median = weiszfeldApproximation(points)
            d = pointsDistances(points,median)
            dAvgStdV.append( (statistics.mean(d),statistics.stdev(d)))
            mediansV.append(median)
        tresholdV = 0
        for p in dAvgStdV:
            tresholdV += (p[0] + p[1] )**2
        tresholdV = math.sqrt(tresholdV)
        dict2[str(i)] = { 'vertical':[mediansV,tresholdV],'horizontal':[mediansH,tresholdH]  }
    

    dict3 = {}
    for i in range (1,len(a)//24 + 1): 
        dAvgStdH = []
        mediansH = []
        for p in range(0,31):  
            points = [dictTest[str(i)][x]['hPoints'][p] for x in range(0,12) ]
            median = weiszfeldApproximation(points)
            d = pointsDistances(points,median)
            dAvgStdH.append( (statistics.mean(d),statistics.stdev(d)))
            mediansH.append(median)
        tresholdH = 0
        for p in dAvgStdH:
            tresholdH += (p[0] + p[1] )**2
        tresholdH = math.sqrt(tresholdH)
        
        dAvgStdV = []
        mediansV = []
        for p in range(0,31):  
            points = [dictTest[str(i)][x]['vPoints'][p] for x in range(0,12) ]
            median = weiszfeldApproximation(points)
            d = pointsDistances(points,median)
            dAvgStdV.append( (statistics.mean(d),statistics.stdev(d)))
            mediansV.append(median)
        tresholdV = 0
        for p in dAvgStdV:
            tresholdV += (p[0] + p[1] )**2
        tresholdV = math.sqrt(tresholdV)
        dict3[str(i)] = { 'vertical':[mediansV,tresholdV],'horizontal':[mediansH,tresholdH]  }
    
    json.dump(dict1,open(args.path+args.file+'.24Gen','w+'))
    json.dump(dict2,open(args.path+args.file+'.18Gen','w+'))
    json.dump(dict3,open(args.path+args.file+'.12Gen','w+'))
