import cv2 as cv
import random
from functools import reduce
import numpy as np
def centerOfMass(img):
    
    indexes = np.where(img==0)
    
    meanY = reduce(lambda x, y: x+y,indexes[0]) / len(indexes[0])
    meanX = reduce(lambda x, y: x+y,indexes[1])  / len(indexes[1])
    return (meanY,meanX)

def verticalS2(img,x0,x1,y0,y1,iterations):
    if (iterations > 0):
        randomDebug = str(random.random())
        
        center = centerOfMass(img[y0:y1,x0:x1])
        center = (int(round(center[0])+y0),int(round(center[1])+x0 ))
        
        
        leftSubdivision =  horizontalS2(img,x0,center[1],y0,y1, iterations - 1)
        rightSubdivision = horizontalS2(img,center[1],x1,y0,y1,iterations - 1)
        cv.line(img, (center[1],y0), (center[1],y1), (255,0,0))
        cv.circle(img, (center[1],center[0]), 5, (200,200,0), -1)
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
        
        cv.line(img, (x0,center[0]), (x1,center[0]), (0,255,0))
        cv.circle(img, (center[1],center[0]), 5, (0,200,200), -1)
        return [center] + topSubdivision + bottomSubdivision
    return []