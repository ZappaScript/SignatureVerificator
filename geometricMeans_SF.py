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
    parser.add_argument('SigBounds18')
    parser.add_argument('SigBounds12')
    parser.add_argument('genPoints')
    parser.add_argument('forgPoints')
    args = parser.parse_args()

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
    
    resForg18 = []
    resForg12 = []

    print(len(forgSigs))
    for it,i in enumerate(w18):
        
        r = [str(c) for c in range(it)] + [str(c) for c in range(it+1,3)]
        z = [x for x in genSigs24 if getUser(x) in r]
        
        resForg18 += [(getDistance(w18[i]['vertical'][0], genSigs24[choice]['vPoints']) <= w18[i]['vertical'][1]) and (getDistance(w18[i]['horizontal'][0], genSigs24[choice]['hPoints']) <= w18[i]['horizontal'][1]) for choice in z]
        resForg12 += [(getDistance(w12[i]['vertical'][0], genSigs24[choice]['vPoints']) <= w12[i]['vertical'][1]) and (getDistance(w12[i]['horizontal'][0], genSigs24[choice]['hPoints']) <= w12[i]['horizontal'][1]) for choice in z]
    
    results = {}
    results['n = 18'] = [modelAccuraccy(resForg18,False)]
    results['n = 12'] = [modelAccuraccy(resForg12,False)]
    
    json.dump(results,open('results_'+args.path,'w'))
    
