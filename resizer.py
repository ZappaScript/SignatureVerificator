import cv2
import argparse
import multiprocessing as mp

def resizeImages(path):
    print(path)
    img = cv2.imread(path,1)
    img = cv2.resize(img,(512,288),interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(path[:-4]+'s.tif',img)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("file")
    args = parser.parse_args()
    with open(args.path+args.file) as f:
        a = f.readlines()

    b = list(map((lambda x: args.path + x.strip()[:-4]+'_t.tif'),a))

    with mp.Pool(4) as p:
        p.map(resizeImages,b)

