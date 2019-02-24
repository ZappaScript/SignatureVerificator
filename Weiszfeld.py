import math
import json
import re
import statistics
a = json.load(open('signatures/list.genuine3.points'))

def getUser(x):
    b = re.search('(.+?)/',x).end()
    return (int(x[:b-1]))

for x in range(1, len(a)//24 + 1): dictTest[str(x)] = [a[key] for key in a if getUser(key)==x  ]
for x in range(0,25): dictTest['55'][x]['hPoints'][0]
for x in range(0,24): dictTest['55'][x]['hPoints'][0]
pointsToTest =[]
for x in range(0,24): pointsToTest.append(dictTest['55'][x]['hPoints'][0])

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
    y = [300,300]
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

for i in range (1,56): 
    dAvgStd = []
    medians = []
    for p in range(0,31):  
        points = [dictTest[str(i)][x]['hPoints'][p] for x in range(0,24) ]
        median = weiszfeldApproximation(points)
        d = pointsDistances(points,median)
        dAvgStd.append( (statistics.mean(d),statistics.stdev(d)))
        medians.append(median)
    treshold = 0
    for a in dAvgStd:
        treshold += (a[0] + a[1] )**2
    treshold = math.sqrt(treshold)
    print(treshold)
