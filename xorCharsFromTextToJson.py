import json
import re
import ast

f = [open('BHSig260FIX/Hindi/hindi.pairs.xor_forforCharVec'),open('BHSig260FIX/Hindi/hindi.pairs.xor_forgenCharVec'),open('BHSig260FIX/Hindi/hindi.pairs.xor_gengenCharVec') ]
for i,file in enumerate(f):
    f[i] = file.readlines()
    f[i]= list(sorted(f[i],key=lambda x : x[18:21]))
    f[i] = list ( map ( lambda x : x[22:],f[i]) )

re.compile('-H')
pattern = re.compile('-H')
forgChars = json.load(open('forgeries.characteristics_vector'))
genChars  = json.load(open('genuines.characteristics_vector'))
count = 0
pattern2 = re.compile('\.tif (.+?)$')
forforDict = {}
forgenDict = {}
gengenDict = {}
for line in f[0]:
    fileNames = pattern.search(line.split('_')[0])
    xOrChar = pattern2.search(line).group(1).split(' ')
    firstFile = line.split('_')[0][:fileNames.start(0)]+'_t.tif'
    secondFile = line.split('_')[0][fileNames.end(0)-1:]+'_t.tif'
    forforDict[re.search('(.+?)\.tif',line).group(1)] = {firstFile:forgChars[firstFile],secondFile:forgChars[secondFile],'xOr':xOrChar}

    count += 1
    if(len(xOrChar)!=10):
        print ('Error',line)

for line in f[1]:
    fileNames = pattern.search(line.split('_')[0])
    xOrChar = pattern2.search(line).group(1).split(' ')
    firstFile = line.split('_')[0][:fileNames.start(0)]+'_t.tif'
    secondFile = line.split('_')[0][fileNames.end(0)-1:]+'_t.tif'
    forgenDict[re.search('(.+?)\.tif',line).group(1)] = {firstFile:forgChars[firstFile],secondFile:genChars[secondFile],'xOr':xOrChar}

    count += 1
    if(len(xOrChar)!=10):
        print ('Error',line)

for line in f[2]:
    fileNames = pattern.search(line.split('_')[0])
    xOrChar = pattern2.search(line).group(1).split(' ')
    firstFile = line.split('_')[0][:fileNames.start(0)]+'_t.tif'
    secondFile = line.split('_')[0][fileNames.end(0)-1:]+'_t.tif'
    gengenDict[re.search('(.+?)\.tif',line).group(1)] = {firstFile:genChars[firstFile],secondFile:genChars[secondFile],'xOr':xOrChar}

    count += 1
    if(len(xOrChar)!=10):
        print ('Error',line)
json.dump(forforDict,open('hindi.forgery_forgery.vectors','w'))
json.dump(forgenDict,open('hindi.forgery_genuine.vectors','w'))
json.dump(gengenDict,open('hindi.genuine_genuine.vectors','w'))