import argparse
import math
import json
import re
import numpy as np
import pickle
from sklearn.metrics.pairwise import chi2_kernel
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
   
    parser.add_argument("simpleForgeriesXor")
    parser.add_argument("genuineChars")
    parser.add_argument("name")
    args = parser.parse_args()
    
    genGen = json.load(open( args.simpleForgeriesXor ))
    genJson = json.load(open( args.genuineChars))
    gengenDict = {}
    forgenDict = {}
    



    for num,key in enumerate(genGen):              
        
        firstFile,secondFile = key[:-4].split('_')      

        fFHoG = genJson[firstFile+'.tif'][:1200]
        fFLBP = genJson[firstFile+'.tif'][1200:]
        sFHoG = genJson[secondFile+'.tif'][:1200]
        sFLBP = genJson[secondFile+'.tif'][1200:]
        
        HoG_chi2 = [chi2_kernel([fFHoG[i*8:(i+1)*8]],[sFHoG[i*8:(i+1)*8 ]]).ravel()[0] for i in range (0,150) ]
        LBP_chi2 = [chi2_kernel([fFLBP[i*10:(i+1)*10]],[sFLBP[i*10:(i+1)*10 ]]).ravel()[0] for i in range (0,30) ]
        gengenDict[key] = np.concatenate((HoG_chi2,LBP_chi2),axis = 0).tolist()
        print(num)

      
    with open(args.path + args.name ,'w+') as handle:
        ##pickle.dump(gengenDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        json.dump(gengenDict,handle)


