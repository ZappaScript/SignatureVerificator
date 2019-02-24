import cv2                                                                 
import numpy as np
##from distributed import *
import multiprocessing as mp
import argparse

def applyMorphology(imgTuple):
    ##kernel = np.ones((5,5),np.uint8)
    img = imgTuple[0]
    img = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_CONSTANT,None, [255,255,255])
    
    img = cv2.erode(img, np.ones((3,3),np.uint8) ,iterations = 1)
    erosionR = cv2.erode(img, np.ones((6,6),np.uint8), iterations = 1)
    erosionG = cv2.erode(erosionR, np.ones((10,10),np.uint8), iterations = 1)
    erosionB = cv2.erode(erosionG, np.ones((16,16),np.uint8), iterations = 1)
    diff1 = cv2.bitwise_not(cv2.subtract(img,erosionR))
    diff2 = cv2.bitwise_not(cv2.subtract(erosionR,erosionG))
    diff3 = cv2.bitwise_not(cv2.subtract(erosionG,erosionB))
    diff1[np.where((diff1 == [0,0,0]).all(axis = 2))] = [0,0,255]
    diff2[np.where((diff2 == [0,0,0]).all(axis = 2))] = [0,255,0]
    diff3[np.where((diff3 == [0,0,0]).all(axis = 2))] = [255,0,0]
    res = cv2.bitwise_and(diff1,img)
    res = cv2.bitwise_and(res,diff2)
    res = cv2.bitwise_and(diff3,res)
    res[np.where((res == [255,255,255]).all(axis = 2))] = [96,100,0]
    
    ##b_channel, g_channel, r_channel = cv2.split(res)
    ##alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50 #creating a dummy alpha channel image.
    ##img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    
    cv2.imwrite(imgTuple[1][:-4]+'m.tif',res)

def openImage(path):                                                       
    img = cv2.imread(path,1)                                          
    return (img,path)                                                             



counter = None
global total

def init(args):
    global counter
    counter = args

def filterWrapper(args):
    
    applyMorphology([cv2.imread(args,1),args])
    global counter
    with counter.get_lock():
        counter.value += 1
        i = int (counter.value)
        print (( i / total) * 100)
    ##print(args)
    
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("file")
    args = parser.parse_args()

    with open(args.path+args.file) as f:                          
        paths = f.readlines()                                                  
                                                                        
    paths = list(map((lambda x: args.path+x[:-5]+'_t.tif'),paths))                
         
    counter = mp.Value('i', 0)
    total = len(paths)                                
    with mp.Pool(processes = 4, initializer = init, initargs = (counter, )) as p:
        p.map(filterWrapper,paths)

