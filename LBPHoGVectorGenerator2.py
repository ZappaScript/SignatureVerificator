import argparse
import math
import json
import re
import numpy as np
import pickle
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("xOrVecForgGen")
    parser.add_argument("xOrVecGenGen")
    parser.add_argument("genuineChars")
    parser.add_argument("forgeryChars")
    args = parser.parse_args()
    
    forGen = json.load(open(args.path + args.xOrVecForgGen ))
    genGen = json.load(open(args.path + args.xOrVecGenGen ))
    forgJson = json.load(open(args.path + args.forgeryChars))
    genJson = json.load(open(args.path + args.genuineChars))
    gengenDict = {}
    forgenDict = {}
    for key in forGen:
        
        firstFile,secondFile = key[:-4].split('_')                  
        forgenDict[key] = np.concatenate((forgJson[firstFile+'.tif'],genJson[secondFile + '.tif']),axis = 0)
    
    
    with open(args.path + 'forgenVectors.LBPHoG64' ,'w') as handle:
        pickle.dump(forgenDict, handle, protocol=pickle.HIGHEST_PROTOCOL)



    for key in genGen:              
        
        firstFile,secondFile = key[:-4].split('_')                  
        gengenDict[key] = np.concatenate((genJson[firstFile+'.tif'],genJson[secondFile + '.tif']),axis = 0)
      
    with open(args.path + 'gengenVectors.LBPHoG64' ,'w') as handle:
        pickle.dump(gengenDict, handle, protocol=pickle.HIGHEST_PROTOCOL)