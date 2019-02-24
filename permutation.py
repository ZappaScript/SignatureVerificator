import itertools
import argparse
import re 
def getUserFromString(x):
    return( int(re.search('(.+?)/',x).group(1)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('file')
    args = parser.parse_args()

    
    with open(args.path+args.file) as f:
        a = f.readlines()
        a = list(map(lambda x : x.strip(),a))
    
    b = []
    for x in range(1,len(a)//24 +1 ): b.append( [i for i in a if getUserFromString(i)==x])

    for i in range(len(b)):
        b[i] = itertools.permutations(b[i],2)
    for i in range(len(b)):
        b[i] = list(b[i])


    with open(args.path+'pairs.'+args.file,'w+') as f:
        for x in range(len(b)):
            for i in b[x]:
                f.write(i[0]+' '+i[1]+' '+str(1)+'\n')
