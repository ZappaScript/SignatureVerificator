import cv2
import numpy as np
import multiprocessing as mp
import argparse
import re
import characteristicsExtractor as ce

def getUserFromString(x):
    return( int(re.search('(.+?)/',x).group(1)))

def cropAndResize(img):
    ##imgF = cv2.imread(route+subroute1,1)
    ##imgG = cv2.imread(route+subroute2,1)


    bbImgF = np.where((img == [0,0,0]).all(axis = 2))
    cropImgF = img[min(bbImgF[0]):max(bbImgF[0]),min(bbImgF[1]):max(bbImgF[1])]
    res = cv2.resize(cropImgF,(500,200), interpolation = cv2.INTER_NEAREST)
    res = cv2.copyMakeBorder(res, 8, 8, 20, 20, cv2.BORDER_REPLICATE,None, [255,255,255]) 
    return res

def denoisingThinning(img):
    kernel2 = np.ones((2,2),np.uint8)
    img = cv2.dilate(img,kernel2,iterations=1)
    img = cv2.erode(img,kernel2,iterations=1)
    return img


def _xOr(args):
    
    ##print(routeG[0:-4],routeF)
    
    imgG = cv2.imread(route+args[0][0:-4]+'_tm.tif',1)
    imgF = cv2.imread(route+args[1][0:-4]+'_t.tif',1)
    imgB = cv2.imread(route+args[0][:-4]+'_t.tif',1)   
    imgA = cv2.imread(route+args[1][:-4]+'_t.tif',1)   
    
    a = ce.centerOfMass(imgA)                                                    
    b = ce.centerOfMass(imgB)                                                    
    tr = (int(round(a[0]-b[0])) ,int(round(a[1]-b[1])))                          
    tb = 0                                                                       
    lr = 0                                                                       
    if (tr[0] >0):                                                               
        tb = (0,tr[0])                                                           
    else:                                                                        
        tb = (abs(tr[0]),0)                                                      
                                                                                 
    if (tr[1] > 0):                                                                                 
        lr = (0,tr[1])                                                                              
    else:                                                                                             
        lr = (abs(tr[1]),0)                                                                           
    
    imgF =cv2.copyMakeBorder(imgF,tb[0],tb[1],lr[0],lr[1],cv2.BORDER_REPLICATE) 
    
    h1,w1 = imgG.shape[:2]
    h2,w2 = imgF.shape[:2]
    
    hResize = max(h1,h2)
    wResize = max(w1,w2)

    if(hResize-h1 != 0):
        if((hResize-h1)%2 == 0):
            imgG = cv2.copyMakeBorder(imgG,(hResize-h1)//2,(hResize-h1)//2,0,0,cv2.BORDER_REPLICATE)
        else :
            imgG = cv2.copyMakeBorder(imgG,(hResize-h1)//2+1,(hResize-h1)//2,0,0,cv2.BORDER_REPLICATE)
    if(hResize-h2 !=0):
        if((hResize-h2)%2 == 0):
            imgF = cv2.copyMakeBorder(imgF,(hResize-h2)//2,(hResize-h2)//2,0,0,cv2.BORDER_REPLICATE)
        else :
            imgF = cv2.copyMakeBorder(imgF,(hResize-h2)//2+1,(hResize-h2)//2,0,0,cv2.BORDER_REPLICATE)
    if(wResize - w1 != 0):
        if((wResize-w1)%2 == 0):
            imgG = cv2.copyMakeBorder(imgG,0,0,(wResize-w1)//2,(wResize-w1)//2,cv2.BORDER_REPLICATE)
        else :
            imgG = cv2.copyMakeBorder(imgG,0,0,(wResize-w1)//2+1,(wResize-w1)//2,cv2.BORDER_REPLICATE)

    if(wResize - w2 != 0):
        if((wResize-w2)%2 == 0):
            imgF = cv2.copyMakeBorder(imgF,0,0,(wResize-w2)//2,(wResize-w2)//2,cv2.BORDER_REPLICATE)
        else :
            imgF = cv2.copyMakeBorder(imgF,0,0,(wResize-w2)//2+1,(wResize-w2)//2,cv2.BORDER_REPLICATE)

    res = cv2.bitwise_xor(imgG,imgF)
    a = re.search('[\d]+/',args[1])
    b = re.search('[\d]+/',args[0])

    ##resPath = args[0][b.end():-4]+'_'+args[1][a.end():-4]+'.tif'
    resPath = args[0][:-4]+'_'+args[1][a.end():-4]+'.tif' ##Added this 01/06/2018
    cv2.imwrite(route+resPath,res)
    print(route+resPath)
    return resPath
    ##return resPath2


counter = None
total = None
nameList = None
def init(args):
    global counter
    global nameList
    counter = args[0]
    nameList = args[1]

def xOr(args):
    
    writtenFile = _xOr(args)
    global counter
    global nameList
    nameList.append(writtenFile)
    with counter.get_lock():
        counter.value += 1
        i = int (counter.value)
        
        print (i , ': ', ( i / total) * 100)
    ##print(args)
    
global route
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("file")
    args = parser.parse_args()
    route = args.path
    with open(args.path + args.file) as f:
        
        f = f.readlines()
        f = list(map (  (lambda x: x.strip().split() ),f))
        total = len(f)
        counter = mp.Value('i', 0)
        nameList = mp.Manager().list()
        
        with mp.Pool(processes = 4, initializer = init, initargs = ([counter,nameList], )) as p:
            p.map(xOr,f)
    
    with open(route  +args.file+'.xor','w+') as w:

        for i in sorted(nameList,key=lambda x: getUserFromString(x) ):
        ##for i in nameList: ##added this on 01/06/2018, delete if you want to generate other than simple forgery pairs
            w.write(i+'\n')
