import json
import math
import re
import argparse


def getUser(key):
    res=re.search('.([\d+]+?)-[G|F]-[\d]+\.tif',key)
    return str(int(res.group(1)))
def getDistance(boundPoints,genPoints):
    totalDistance = 0
    for numPoint,point in enumerate(genPoints):
        totalDistance += (point[0]-boundPoints[numPoint][0]) **2 + (point[1] - boundPoints[numPoint][1])**2
    return math.sqrt(totalDistance)

def getForgeryNumber(key):
    b = re.search('.G-([\d]+?)\.tif',key)
    return int(b.group(1))

def modelAccuraccy(vec,toTest):
    count = 0
    for i in vec:
        if (i==toTest):
            count +=1
    return (count/len(vec))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('SigBounds24')
    parser.add_argument('SigBounds18')
    parser.add_argument('SigBounds12')
    parser.add_argument('genPoints')
    parser.add_argument('forgPoints')
    args = parser.parse_args()

    w24 = json.load(open(args.SigBounds24))
    w18 = json.load(open(args.SigBounds18))
    w12 = json.load(open(args.SigBounds12))
    genSigs24 = json.load(open(args.genPoints ))
    forgSigs = json.load(open(args.forgPoints))

    genSigs18 = {}
    genSigs12 = {}
    for i in genSigs24:
        if(getForgeryNumber(i)>12):
            genSigs12[i] = genSigs24[i]

    for i in genSigs24:
        if(getForgeryNumber(i)>18):
            genSigs18[i] = genSigs24[i]
    

    resForg24 = [(getDistance(w24[getUser(i)]['vertical'][0], forgSigs[i]['vPoints']) <= w24[getUser(i)]['vertical'][1]) and (getDistance(w24[getUser(i)]['horizontal'][0], forgSigs[i]['hPoints']) <= w24[getUser(i)]['horizontal'][1]) for i in forgSigs]
    resForg18 = [(getDistance(w18[getUser(i)]['vertical'][0], forgSigs[i]['vPoints']) <= w18[getUser(i)]['vertical'][1]) and (getDistance(w18[getUser(i)]['horizontal'][0], forgSigs[i]['hPoints']) <= w18[getUser(i)]['horizontal'][1]) for i in forgSigs]
    resForg12 = [(getDistance(w12[getUser(i)]['vertical'][0], forgSigs[i]['vPoints']) <= w12[getUser(i)]['vertical'][1]) and (getDistance(w12[getUser(i)]['horizontal'][0], forgSigs[i]['hPoints']) <= w12[getUser(i)]['horizontal'][1]) for i in forgSigs]
    resGenSigs18 = [(getDistance(w18[getUser(i)]['vertical'][0], genSigs18[i]['vPoints']) <= w18[getUser(i)]['vertical'][1]) and (getDistance(w18[getUser(i)]['horizontal'][0], genSigs18[i]['hPoints']) <= w18[getUser(i)]['horizontal'][1]) for i in genSigs18]
    resGenSigs12 = [(getDistance(w12[getUser(i)]['vertical'][0], genSigs12[i]['vPoints']) <= w12[getUser(i)]['vertical'][1]) and (getDistance(w12[getUser(i)]['horizontal'][0], genSigs12[i]['hPoints']) <= w12[getUser(i)]['horizontal'][1]) for i in genSigs12]
    
    results = {}
    results['n = 18'] = [modelAccuraccy(resGenSigs18,True),modelAccuraccy(resForg18,False)]
    results['n = 12'] = [modelAccuraccy(resGenSigs12,True),modelAccuraccy(resForg12,False)]
    
    json.dump(results,open(args.path+'results','w'))
    
