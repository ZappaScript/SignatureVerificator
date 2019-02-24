import characteristicsExtractor as ce
import cv2        
import argparse
import multiprocessing as mp
import json
import re
counter = None
total = None
charVecList = None
def init(args):
    global counter
    global charVecList
    counter = args[0]
    charVecList = args[1]


def computePoints(path):
    
    global counter
    global charVecList
    img = cv2.imread(path.strip(),1)                 
    h,w = img.shape[:2]                                                   
    
    try:                      
        pointsV = ce.verticalS2(img,0,w,0,h,5)                                
    except TypeError:
        print(path)
    
    pointsH = ce.horizontalS2(img,0,w,0,h,5)                              
    a = re.search('/[\d]+/',path.strip())
    charVecList.append([path.strip()[a.start()+1:],{'vPoints':pointsV,'hPoints':pointsH} ])  
    




if __name__ == '__main__':
    vecDict = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("file")
    args = parser.parse_args()
    charVecList = mp.Manager().list()
                                                             
    resFile = open(args.path+args.file+'.points','w')
    files = open(args.path+args.file)
    files = [args.path+x for x in files.readlines()]
    with mp.Pool(processes = 4, initializer = init, initargs = ([counter,charVecList], )) as p:
        p.map(computePoints,files)                                    
                       
        

    for objs in charVecList:                 
        vecDict[objs[0]] = objs[1]                                                   
    json.dump(vecDict,resFile)
    resFile.close()  