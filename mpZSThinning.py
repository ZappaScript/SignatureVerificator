import multiprocessing as mp
import libTest as zs
import argparse
route = 'BHSig260FIX/Hindi/'

counter = None
resFilePath = None

def init(args):
    global counter
    global resFilePath
    counter = args[0]
    resFilePath = args[1]


def thinningWrapper(args):
    
    writtenImage=zs.zhThinning(args)
    global counter
    with counter.get_lock():
        counter.value += 1
        i = int (counter.value)
        print (( i / 4800) * 100)
    print(args)
    resFilePath.append(str(writtenImage +'\n'))
    ##print(counter.value, 'say whaaat')
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("file")
    args = parser.parse_args()
    
    with open(args.path + args.file) as f:
        routes = f.readlines()
        routes = list(map((lambda x: x.strip() ),routes))
        routes = list(map((lambda x: args.path + x ), routes))
        counter = mp.Value('i', 0)
        resFilePath = mp.Manager().list()

        with mp.Pool(processes = 4, initializer = init, initargs = ([counter,resFilePath], )) as p:
            
            p.map(thinningWrapper,routes)
    with open(args.path + args.file + '.thinned','w') as resFile:
        for line in resFilePath:
            resFile.write(line)
    