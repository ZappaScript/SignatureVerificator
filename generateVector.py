import argparse
import math
import json
import re
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
    for key in forGen:
        print(key)              
        
        firstFile,secondFile = key[4:-4].split('_')                  
        cMass = math.sqrt((forgJson[firstFile+'.tif'][0][0] - genJson[secondFile + '.tif'][0][0])**2 + (forgJson[firstFile+'.tif'][0][1]-genJson[secondFile+'.tif'][0][1] )**2)           
        occupancyRatio = abs(forgJson[firstFile+'.tif'][1] -genJson[secondFile+'.tif'][1]  ) / ((forgJson[firstFile+'.tif'][1]+genJson[secondFile+'.tif'][1])/2 )   
        aspectRatio = abs(forgJson[firstFile+'.tif'][2] -genJson[secondFile+'.tif'][2]  ) / ((forgJson[firstFile+'.tif'][2]+genJson[secondFile+'.tif'][2])/2 )   
        densityRatio = abs(forgJson[firstFile+'.tif'][3] -genJson[secondFile+'.tif'][3]  ) / ((forgJson[firstFile+'.tif'][3]+genJson[secondFile+'.tif'][3])/2 )   
        harrisCorner = abs(forgJson[firstFile+'.tif'][4] -genJson[secondFile+'.tif'][4]  ) / ((forgJson[firstFile+'.tif'][4]+genJson[secondFile+'.tif'][4])/2 )   
        forGen[key].extend((cMass,occupancyRatio,aspectRatio,densityRatio,harrisCorner))
    json.dump(forGen,open( args.path + 'forgenVectors' ,'w'))




    for key in genGen:              
        print(key)
        
        firstFile,secondFile = key[4:-4].split('_')
        cMass = math.sqrt((genJson[firstFile+'.tif'][0][0] - genJson[secondFile + '.tif'][0][0])**2 + (genJson[firstFile+'.tif'][0][1]-genJson[secondFile+'.tif'][0][1] )**2)           
        occupancyRatio = abs(genJson[firstFile+'.tif'][1] -genJson[secondFile+'.tif'][1]  ) / ((genJson[firstFile+'.tif'][1]+genJson[secondFile+'.tif'][1])/2 )   
        aspectRatio = abs(genJson[firstFile+'.tif'][2] -genJson[secondFile+'.tif'][2]  ) / ((genJson[firstFile+'.tif'][2]+genJson[secondFile+'.tif'][2])/2 )   
        densityRatio = abs(genJson[firstFile+'.tif'][3] -genJson[secondFile+'.tif'][3]  ) / ((genJson[firstFile+'.tif'][3]+genJson[secondFile+'.tif'][3])/2 )   
        harrisCorner = abs(genJson[firstFile+'.tif'][4] -genJson[secondFile+'.tif'][4]  ) / ((genJson[firstFile+'.tif'][4]+genJson[secondFile+'.tif'][4])/2 )   
        genGen[key].extend((cMass,occupancyRatio,aspectRatio,densityRatio,harrisCorner)) 
    json.dump(genGen,open( args.path + 'gengenVectors' ,'w'))