import json
import re
import cv2
import numpy as np

f = open('BHSig260FIX/Hindi/list.forgery.thinnedCharVec')
f = f.readlines()
forgeries = json.load(open('forgery.characteristics_vector'))
for line in f:
    fileName = re.search('.tif',line)
    img= cv2.imread(line[:fileName.end(0)],0)
    res = cv2.cornerHarris(img,2,3,0.04)
    numCorners = len(np.where(res > 0.01 * res.max())[0])
    forgeries[line[22:fileName.end(0)]].append(numCorners) 
     
json.dump(forgeries,open('forgeries.characteristics_vector','w'))

    
     
genuines = json.load(open('genuine.characteristics_vector'))
f = open('BHSig260FIX/Hindi/list.genuine.thinnedCharVec')
f = f.readlines()
for line in f:
    fileName = re.search('.tif',line)
    img= cv2.imread(line[:fileName.end(0)],0)
    res = cv2.cornerHarris(img,2,3,0.04)
    numCorners = len(np.where(res > 0.01 * res.max())[0])
    genuines[line[22:fileName.end(0)]].append(numCorners) 
    
json.dump(genuines,open('genuines.characteristics_vector','w'))


    
