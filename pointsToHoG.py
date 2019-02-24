import cv2
import numpy as np
from skimage.feature import *
import json
import argparse
import characteristicsExtractor as ce
import re    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("file")
    parser.add_argument("medians")
    args = parser.parse_args()
    path = args.path
    fileName = args.file
    bins = [float(i) for i in range(1,9)]         
    z = json.load(open(path+fileName))
    dictRes = {}
    for enum,file in enumerate(z):
        img = cv2.imread(path+file,0)
        b = [ z[file]['hPoints'][x] for x in [0, 1, 2, 3, 6, 9, 10, 13, 16, 17, 18, 21, 24, 25, 28]]
        
        img = cv2.copyMakeBorder(img,64,64,64,64,cv2.BORDER_CONSTANT,0)
        pointsHoGHistograms = []
        pointsLBPHistograms = []
        
        for it,i in enumerate(b):

            h = hog(img [i[0]:i[0]+64,i[1]:i[1]+64],orientations=8, pixels_per_cell=(32, 32),cells_per_block=(1, 1),multichannel=False)
            h2 = [(h[i]+ h[i+8] +h[i+16]+h[i+24])/4 for i in range(0,8) ]
            lbp = local_binary_pattern(img[i[0]:i[0]+64,i[1]:i[1]+64],8,1,'uniform')
            lbp = np.histogram(lbp,bins=np.arange(0,11),range=(0,10))[0].astype('float')
            lbp /= sum(lbp) 
            pointsHoGHistograms = np.concatenate((pointsHoGHistograms,h2,h), axis = 0)
            pointsLBPHistograms = np.concatenate((pointsLBPHistograms,lbp),axis = 0)
        ##b= z[file]['vPoints']
        b = [ z[file]['vPoints'][x] for x in [0, 1, 2, 3, 6, 9, 10, 13, 16, 17, 18, 21, 24, 25, 28]]
        
        for it,i in enumerate(b):
            h = hog(img [i[0]:i[0]+64,i[1]:i[1]+64],orientations=8, pixels_per_cell=(32, 32),cells_per_block=(1, 1),multichannel=False)
            h2 = [(h[i]+ h[i+8] +h[i+16]+h[i+24])/4 for i in range(0,8) ]
            lbp = local_binary_pattern(img[i[0]:i[0]+64,i[1]:i[1]+64],8,1,'uniform')
            lbp = np.histogram(lbp,bins=np.arange(0,11),range=(0,10))[0].astype('float')
            lbp /= sum(lbp) 
            pointsHoGHistograms = np.concatenate((pointsHoGHistograms,h2,h), axis = 0)
            pointsLBPHistograms = np.concatenate((pointsLBPHistograms,lbp),axis = 0)
        
        print(enum,re.search('[\d]+/(.+?)$',file).group(1) )
        dictRes[re.search('[\d]+/(.+?)$',file).group(1)] = np.concatenate((pointsHoGHistograms,pointsLBPHistograms),axis = 0).tolist()
    json.dump(dictRes,open(path+ fileName +'.LBPHoG64','w+'))
