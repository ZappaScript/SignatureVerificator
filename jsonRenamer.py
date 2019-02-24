import json
from auxFuncs import getName
paths = ["Model_Morph_Centered", "Modelos_combinados", "Modelos_Hist_sin_LBP", "Modelos_Morph_xOr", "Modelos_Hist_32PX", "Modelos_Hist_64PX"]
dirs = ['signatures/', 'BHSig260FIX/Hindi/','BHSig260FIX/Bengali/']

for fDir in dirs:
    for path in paths:
        newResult = {}
        jsonObject = json.load(open(fDir+path+'/simpleForgeriesResult'))
        for i in jsonObject:
            newResult[getName(i)] = jsonObject[i]
        json.dump(newResult,open(fDir+path+'/simpleForgeriesResultRenamed','w'))

