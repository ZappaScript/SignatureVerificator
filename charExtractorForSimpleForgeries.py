import cv2
import numpy as np
from functools import reduce
import math
from random import *
import argparse
import multiprocessing as mp
import colorVecLib as cVector
import json
import re
import random
import pdb

def getFile(i):
    preludeEnds = re.search('/(.+?)/',i).end()
    return ( i[preludeEnds:] )

def centerOfMass(img):
    
    indexes = np.where(img==0)
    
    meanY = reduce(lambda x, y: x+y,indexes[0]) / len(indexes[0])
    meanX = reduce(lambda x, y: x+y,indexes[1])  / len(indexes[1])
    return (meanY,meanX)
    
def aspectRatio(img):
    indexes = np.where(img==0)
    aspectRatio = (max(indexes[1])-min(indexes[1])) / (max(indexes[0])-min(indexes[0]))
    return aspectRatio

def occupancyRatio(img):
    aux = np.where(img==0)
    occupancyRatio = len(aux[1])/( (max(aux[1])-min(aux[1])) * (max(aux[0])-min(aux[0])))
    return occupancyRatio

def densityRatio(img):    
    aux = np.where(img==0)
    meanX = math.floor( (max(aux[1])+min(aux[1]))/2  )
    leftPixels = len(list(filter(lambda x: x < meanX, aux[1])))
    rightPixels = len(aux[1])-leftPixels
    return leftPixels/rightPixels

def verticalS2(img,x0,x1,y0,y1,iterations):
    if (iterations > 0):
        randomDebug = str(random.random())
        
        center = centerOfMass(img[y0:y1,x0:x1])
        center = (int(round(center[0])+y0),int(round(center[1])+x0 ))
        ##cv2.imwrite('signatures/v'+str(iterations)+'_'+randomDebug+'_left.png',img[y0:y1,x0:center[1]])
        ##cv2.imwrite('signatures/v'+str(iterations)+'_'+randomDebug+'_right.png',img[y0:y1,center[1]:x1])
        leftSubdivision =  horizontalS2(img,x0,center[1],y0,y1, iterations - 1)
        rightSubdivision = horizontalS2(img,center[1],x1,y0,y1,iterations - 1)##center previously had a +1
        return [center] + leftSubdivision + rightSubdivision
    return []

def horizontalS2(img,x0,x1,y0,y1,iterations):
    if (iterations > 0):
        randomDebug = str(random.random())
        
        center = centerOfMass(img[y0:y1,x0:x1])
        center = (int(round(center[0])+y0),int(round(center[1])+x0 ))
        if(y0==center[0]):
            print('here')
        ##cv2.imwrite('signatures/h'+str(iterations)+'_'+randomDebug+'_top.png',img[y0:center[0],x0:x1])
        ##cv2.imwrite('signatures/h'+str(iterations)+'_'+randomDebug+'_bot.png',img[center[0]:y1,x0:x1])
        topSubdivision =  verticalS2(img,x0,x1,y0,center[0], iterations - 1)
        bottomSubdivision = verticalS2(img,x0,x1,center[0],y1,iterations - 1)##center previously had a +1
        return [center] + topSubdivision + bottomSubdivision
    return []

def colorVector(img):
    
    black = len(np.where(img==0)[0])
    red = len(np.where(img==[0,0,255])[0])
    green = len(np.where(img==[255,0,0])[0])
    blue = len(np.where(img==[0,255,0])[0])
    bColor1 = len(np.where(img==[155,159,255])[0])
    bColor2 = len(np.where(img==[100,96,0])[0])
    white = len(np.where(img==[255,255,255])[0])
    cyan = len(np.where(img==[255,255,0])[0])
    magenta = len(np.where(img==[0,255,255])[0])
    yellow = len(np.where(img==[255,0,255])[0])
    
    return [ black, red, green, blue, bColor1, bColor2, white, cyan, magenta, yellow ]
          
counter = None
total = None
charVecList = None
def init(args):
    global counter
    global charVecList
    counter = args[0]
    charVecList = args[1]

def harrisCorners(img):
    res = cv2.cornerHarris(img,2,3,0.04)
    numCorners = len(np.where(res > 0.01 * res.max())[0])
    return numCorners

def colorVectorWrapper(path):
    
    global counter
    global charVecList
    ##img = cv2.imread(path,1)
    charVec = [path,cVector.colorVector(path).tolist()]
    charVecList.append(charVec)
    with counter.get_lock():
        counter.value += 1
        i = int (counter.value)
        
        print (i , ': ', ( i / total) * 100)



def funcsWrapper(path):
    
    global counter
    global charVecList
    img = cv2.imread(path,0)
    charVec = [path,centerOfMass(img), occupancyRatio(img), aspectRatio(img), densityRatio(img), harrisCorners(img)]
    charVecList.append(charVec)
    with counter.get_lock():
        counter.value += 1
        i = int (counter.value)
        
        print (i , ': ', ( i / total) * 100)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("simpleForgery")
    

    args = parser.parse_args()

    for i in [args.simpleForgery]:
        with open(args.path+i) as f:
            charDict3 = {}
            files = f.readlines()
            files = list(map(lambda x : args.path + x.strip(),files))
            counter = mp.Value('i', 0)
            charVecList = mp.Manager().list()
            total = len(files)
            print(files)
            with mp.Pool(processes = 4, initializer = init, initargs = ([counter,charVecList], )) as p:
                p.map(colorVectorWrapper,files)
            for c in charVecList:
                charDict3[getFile(c[0])] = c[1]
            json.dump(charDict3,open(args.path+i+'.characteristics','w+'))