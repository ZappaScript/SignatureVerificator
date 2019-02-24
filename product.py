import itertools
import argparse
import re

def getUserFromString(x):
    return( int(re.search('(.+?)/',x).group(1)))
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('fileGen')
    parser.add_argument('fileForg')
    args = parser.parse_args()
    
    with open(args.path+args.fileForg) as f:
        a = f.readlines()
        a = list(map(lambda x : x.strip(),a))
    
    with open(args.path+args.fileGen) as f:
        b = f.readlines()
        b = list(map(lambda x : x.strip(),b))
    
    c = []
    for x in range(1, len(b)//24 + 1 ): c.append( itertools.product ([i for i in a if getUserFromString(i)==x] , [i for i in b if getUserFromString(i)==x] ))

    ##for i in range(len(c)):
      ##  c[i] = itertools.permutations(c[i],2)
    ##for i in range(len(c)):
      ##  c[i] = list(c[i])


    with open(args.path+'pairs.forgery_genuine','w+') as f:
        for x in range(len(c)):
            for i in c[x]:
                f.write(i[0]+' '+i[1]+' '+str(1)+'\n')
