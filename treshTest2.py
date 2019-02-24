from characteristicsExtractor import *
import json 
import os.path
import statistics


def calcTreshold(route):
    accumX=0
    accumY=0
    
    with open(route) as f:
        data = json.load(f)

    medians = {'v':[],'h':[]}
    
    for i in range(1,32):
        medianX = []
        medianY = []
        for x in range(1,25):
            medianY.append( data[str(x)]['vPoints'][i-1][0])
            medianX.append( data[str(x)]['vPoints'][i-1][1])
        medians['v'].append( (sorted(medianY)[11],sorted(medianX)[11] ))

    for i in range(1,32):
        medianX = []
        medianY = []
        for x in range(1,25):
            medianY.append( data[str(x)]['hPoints'][i-1][0])
            medianX.append( data[str(x)]['hPoints'][i-1][1])
        medians['h'].append( (sorted(medianY)[11],sorted(medianX)[11] ))

    distances = []
    
    for i in range(1,32):
        distanceFromMedian = []
        
        for x in range(1,25):
            distance =  math.sqrt((medians['h'][i-1][0] - data[str(x)]['hPoints'][i-1][0])**2 +  (medians['h'][i-1][1] - data[str(x)]['hPoints'][i-1][1])**2) 
            distanceFromMedian.append(distance)
        distances.append(distanceFromMedian)

    ##compute also the vertical distances

    
    for i in range(0,len(distances)):
        print(statistics.mean(distances[i]) , statistics.stdev(distances[i]))
        distances[i] = (statistics.mean(distances[i]) + statistics.stdev(distances[i]))**2
    
    
    return (math.sqrt(sum(distances)), medians)





