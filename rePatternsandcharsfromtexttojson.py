# coding: utf-8

with open('BHSig260FIX/Hindi/hindi.pairs.xor_forforCharVec') as f:
    lines = f.readlines()
    
lines
lines[0]
lines[0][1]
lines[0][:20]
lines[0][:21]
lines[0][:22]
lines[0][:22].split('/')
lines[0].split('/')
test = lines[0].split('/')
test
test[4]
test[3]
test[3].split(' ')
test[3].match()
test[3].search('-H')
import re
re.search('-H-',test[3])
a = re.search('-H-',test[3])
a
a[0]
a[1]
a.group(0)
a.group(1)
a.group()
re.findall('-H',test[3])
re.findall('-all',test[3])
a = re.compile('-H')
a.search(test[3])
a.search(test[3])?
b = a.search(test[3])
get_ipython().run_line_magic('pinfo', 'b')
b.pos()
b.pos
b.start
b.group(0)
b.string
b.end
b
b.groups
b.re
b.endpos
b.regs
b.span
b.start(0)
b.end(0)
test[3]
b.start(0)+1
test[3][11]
test[3][11:]
test[3][11:].split('_')
import os
os.path.exists('BHSig260FIX/Hindi/')
test
os.path.exists('BHSig260FIX/Hindi/'+test[2]+'/'+test[3][11:].split('_')[0]+'.tif')

rePattern = re.compile('-H')
for line in lines: 
    fileToCheck = line.split('/')       
    b = rePattern(fileToCheck[3])
    os.path.exists('BHSig260FIX/Hindi/'+fileToCheck[2]+'/'+fileToCheck[3][b.start(0)+1:].split('_')[0]+'.tif')
    

rePattern = re.compile('-H')
for line in lines: 
    fileToCheck = line.split('/')       
    b = rePattern.search(fileToCheck[3])
    os.path.exists('BHSig260FIX/Hindi/'+fileToCheck[2]+'/'+fileToCheck[3][b.start(0)+1:].split('_')[0]+'.tif')
    

rePattern = re.compile('-H')
for line in lines: 
    fileToCheck = line.split('/')       
    b = rePattern.search(fileToCheck[3])
    if(!os.path.exists('BHSig260FIX/Hindi/'+fileToCheck[2]+'/'+fileToCheck[3][b.start(0)+1:].split('_')[0]+'.tif')):
        print('no existe')

    

rePattern = re.compile('-H')
for line in lines: 
    fileToCheck = line.split('/')       
    b = rePattern.search(fileToCheck[3])
    if(os.path.exists('BHSig260FIX/Hindi/'+fileToCheck[2]+'/'+fileToCheck[3][b.start(0)+1:].split('_')[0]+'.tif')==False ):
        print('no existe')

    

rePattern = re.compile('-H')
count = 0
for line in lines: 
    fileToCheck = line.split('/')       
    b = rePattern.search(fileToCheck[3])
    if(os.path.exists('BHSig260FIX/Hindi/'+fileToCheck[2]+'/'+fileToCheck[3][b.start(0)+1:].split('_')[0]+'.tif')==False ):
        print('no existe')

    else:
        count += 1
        print('existe ', count)
        
open('BHSig260FIX/Hindi/list.forgery.thinnedCharVec') as f2:

   
   


   
f2 = open('BHSig260FIX/Hindi/list.forgery.thinnedCharVec')


    
    


    
f2
f2 = f2.readlines()
f2
f3 = list(map(lambda x:x[21:],f2 ))
f3
f3 = list(map(lambda x:x[22:],f2 ))
f3
pat = re.compile('.tif')
pat.search(f3[0])
f3[0][:17]
for line in f3:
    aux = pat.search(line)
    print(line[:aux.end(0)])
    
for line in f3:
    aux = pat.search(line)
    print(line[:aux.end(0)]+ '/' + line[aux.end(0):-1] )
    
    
for line in f3:
    aux = pat.search(line)
    print(line[:aux.end(0)]+ '/' + line[aux.end(0):-1].strip() )
    
    
    
for line in f3:
    aux = pat.search(line)
    print(line[:aux.end(0)]+ ' ' + line[aux.end(0):-1].strip() )
    
    
    
    
charDict = {}
for line in f3:
    aux = pat.search(line)
    print(line[:aux.end(0)]+ '/' + line[aux.end(0):-1].strip() )
    
    
    
f3[0]
pattern2 = re.compile('\(\w+\)')
pattern2.search(f3[0])
a= pattern2.search(f3[0])
a
pattern2 = re.compile('[w+]')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('w+')
a= pattern2.search(f3[0])
a
pattern2 = re.compile(' ')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\w+')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\(\w+')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\w+.,\s\w+.,]\)')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\w+.,\s\w+.,]')
a= pattern2.search(f3[0])
a
f3[0][18:]
pattern2 = re.compile('\([\w+.\s\w+.]')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\w+.\w+,]')
a= pattern2.search(f3[0])
a
a.groups
a.groups(0)
a.groups(1)
a.group(1)
a.group(0)
pattern2 = re.compile('\([\w+.\w+]')
a= pattern2.search(f3[0])
a
a
pattern2 = re.compile('\([\d+.\d+]')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('[\d+.\d+]')
a= pattern2.search(f3[0])
a
a.group(0)
a.group(2)
a.group(1)
a= pattern2.match(f3[0])
a
pattern2 = re.compile('[\d+.\d+]')
a
a= pattern2.match(f3[0])
a
pattern2 = re.compile('[\d+.\d+]')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('[\d+.\d+]+')
a= pattern2.search(f3[0])
a
f3[0][4:]
pattern2 = re.compile('\([\d+.\d+]+')
a= pattern2.search(f3[0])
a
f3[0][18:]
f3[0][18:36]
pattern2 = re.compile('\([\d+.\d+]+\s')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d+.\d+]+ \s')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d+.\d+]')
a= pattern2.search(f3[0])
a
f3[0][18:20]
pattern2 = re.compile('\([\d+\.\d+]')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d+.]+')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d+.]')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d+]')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d+]\.[d+]')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d+]+\.[d+]+')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d+.]')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d+.][\d+]')
a= pattern2.search(f3[0])
a
f3[0][18:21]
pattern2 = re.compile('\([\d]+[\d+]')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d]+')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d]+\.[\d]+')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d]+\.[\d]+\s[\d]+\.[\d]+')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d]+\.[\d]+\,\s[\d]+\.[\d]+')
a= pattern2.search(f3[0])
a
pattern2 = re.compile('\([\d]+\.[\d]+\,\s[\d]+\.[\d]+\)')
a= pattern2.search(f3[0])
a
a= pattern2.search(f3[1])
a
if a : 
    print(True)
    
pattern2 = re.compile('\([\d]+\.[\d]+\,\s[\d]+\.[\d]+\sfsdfs)')
pattern2 = re.compile('\([\d]+\.[\d]+\,\s[\d]+\.[\d]+asdsdfa\)')
a= pattern2.search(f3[1])
a
if a : 
    print(True)
    
pattern2 = re.compile('\([\d]+\.[\d]+\,\s[\d]+\.[\d]+\)')
anotherCount = 0
for line in f3:
    if (pattern2.search(line)):
        anotherCount += 1
        
anotherCount
x = pattern2.search(f3[0])
x
f3[x.start(0):x.end(0)]
f3[0][x.start(0):x.end(0)]
f3[0][x.start(0):x.end(0)].strip()
f3[0][x.start(0):x.end(0)].replace(' '.'')
f3[0][x.start(0):x.end(0)].replace(' ','')
import ast
ast.literal_eval(f3[0][x.start(0):x.end(0)].replace(' ',''))
ast.literal_eval(f3[0][x.start(0):x.end(0)])
ast.literal_eval('['+f3[0][x.start(0):x.end(0)]+','+f3[0][x.end(0):-1].strip().replace(' ',',')+']')
btr = ast.literal_eval('['+f3[0][x.start(0):x.end(0)]+','+f3[0][x.end(0):-1].strip().replace(' ',',')+']')
btr
btr[0]
btr[0][0]
btr[0][0]**2
for line in f3:ast.literal_eval('['+line[x.start(0):x.end(0)]+','+line[x.end(0):-1].strip().replace(' ',',')+']')
for line in f3:ast.literal_eval('['+line[x.start(0):x.end(0)]+','+line[x.end(0):-1].strip().replace(' ',',')+']')
for line in f3: ast.literal_eval('['+line[x.start(0):x.end(0)]+','+line[x.end(0):-1].strip().replace(' ',',')+']')
for line in f3: x = pattern2.search(line) ast.literal_eval('['+line[x.start(0):x.end(0)]+','+line[x.end(0):-1].strip().replace(' ',',')+']')
for line in f3:
     x = pattern2.search(line) 
     ast.literal_eval('['+line[x.start(0):x.end(0)]+','+line[x.end(0):-1].strip().replace(' ',',')+']')
     
for line in f3:
     x = pattern2.search(line) 
     result = ast.literal_eval('['+line[x.start(0):x.end(0)]+','+line[x.end(0):-1].strip().replace(' ',',')+']')
     print(result)
     
dictTest = {}
for line in f3:
     x = pattern2.search(line)
     dictTest[line[:x.end(0)]] =  ast.literal_eval('['+line[x.start(0):x.end(0)]+','+line[x.end(0):-1].strip().replace(' ',',')+']')
     print(result)
     
dictTest
dictTest = {}
dictTest
for line in f3:
     x = pattern2.search(line)
     dictTest[line[:x.start(0)]] =  ast.literal_eval('['+line[x.start(0):x.end(0)]+','+line[x.end(0):-1].strip().replace(' ',',')+']')
     print(result)
     
dictTest
import json
json.dump(dictTest,file('asdfsdf.json','w'))
json.dump(dictTest,open('asdfsdf.json','w'))
werw = json.load('asdfsdf.json')
werw = json.load(open('asdfsdf.json'))
werw
werw == dictTest
werw[0] == dictTest[0]
werw['H-S-40-F-20_t.tif'] == dictTest['H-S-40-F-20_t.tif']
werw['H-S-40-F-20_t.tif '] == dictTest['H-S-40-F-20_t.tif ']
werw['H-S-40-F-20_t.tif '] 
dictTest['H-S-40-F-20_t.tif ']
f2
f
f1
f1 = f.readlines()
werw['H-S-40-F-20_t.tif '] 
dictTest = {}
for line in f3:
     x = pattern2.search(line)
     dictTest[line[:x.start(0)].strip()] =  ast.literal_eval('['+line[x.start(0):x.end(0)]+','+line[x.end(0):-1].strip().replace(' ',',')+']')
     print(result)
     
json.dump(dictTest,open('asdfsdf.json','w'))
werw = json.load(open('asdfsdf.json'))
werw['H-S-40-F-20_t.tif'] 
json.dump(werw,open('genuine.characteristics_vector','w'))
f1
f3
f3[0][5:]
f3[0][4:]
f3[0]
f2[0]
f2[0][17:20]
f2[0][18:21]
f2[2][18:21]
f2[4800][18:21]
f2[4000][18:21]
f2 = list(sorted(f2,key= int( str[18:21]  )))
f2 = list(sorted(f2,key= lambda line: int( line[18:21]  )))
f2
f4 = list(map(f2,lambda line: line[22:] ))
f4 = list(map(f2, lambda x: x[22:] ))
f4 = list(map(f lambda x: x[22:],f2 ))
f4 = list(map(lambda x: x[22:],f2 ))
f4
dictTest = {}
for line in f4:
     x = pattern2.search(line)
     dictTest[line[:x.start(0)].strip()] =  ast.literal_eval('['+line[x.start(0):x.end(0)]+','+line[x.end(0):-1].strip().replace(' ',',')+']')
     print(result)

          
json.dump(dictTest,open('forgery.characteristics_vector','w'))
g5 = open('BHSig260FIX/Hindi/list.genuine.thinnedCharVec)
g5 = open('BHSig260FIX/Hindi/list.genuine.thinnedCharVec')
g5 = list(map(lambda x: x[22:],g5 ))
g5
g5 = open('BHSig260FIX/Hindi/list.genuine.thinnedCharVec')
g5 = list(sorted(g5,key= lambda line: int( line[18:21]  )))
g5 = list(map(lambda x: x[22:],g5 ))
g5
dictTest = {}
for line in g5:
     x = pattern2.search(line)
     dictTest[line[:x.start(0)].strip()] =  ast.literal_eval('['+line[x.start(0):x.end(0)]+','+line[x.end(0):-1].strip().replace(' ',',')+']')
     print(result)
     

          
dictTest
json.dump(dictTest,open('genuine.characteristics_vector','w'))
for key,value in dictTest:
    print(key,value)
    
for key in dictTest:
    print(key,value)
    
    
for key in dictTest:
    print(key,dictTest[key])
    
    
    
for key in dictTest:
    print(key)
    
    
    
    
for key in dictTest:
    print(key+'s')
    
    
    
    
    
pattern3 = re.compile('H-S-[\d]-G')

    
    
    
dict[0]
dictTest[0]
dictTest[1]
g5
pattern3.search(g5[0])
g5[0][0:7]
pattern3.search(g5[2000])
bg = pattern3.search(g5[2000])
bg
pattern3 = re.compile('H-S-[\d]+-G')


    
    
    
bg = pattern3.search(g5[2000])
bg
bg = pattern3.split(g5[2000])
bg
g5[3:-40]
g5[0][3:-40]
g5[0][4:-80]
bg = pattern3.search(g5[2000])
bg.end(0)
g5[2000][bg.start(0):bg.end(0)-2]
g5[2000][bg.start(0)+4:bg.end(0)-2]
bg = pattern3.search(g5[3456])
g5[3456][bg.start(0)+4:bg.end(0)-2]
g5[3999][bg.start(0)+4:bg.end(0)-2]
g5[3839][bg.start(0)+4:bg.end(0)-2]
g5[3840][bg.start(0)+4:bg.end(0)-2]
g5[3839][bg.start(0)+4:bg.end(0)-2]
g5[2][bg.start(0)+4:bg.end(0)-2]
g5[200][bg.start(0)+4:bg.end(0)-2]
bg = pattern3.search(g5[200])
g5[200][bg.start(0)+4:bg.end(0)-2]
int(g5[200][bg.start(0)+4:bg.end(0)-2])
int(g5[200][bg.start(0)+4:bg.end(0)-2])**3
dictTest['asdfasf']
get_ipython().run_line_magic('save', 'rePatternsandcharsfromtexttojson 0-335')
