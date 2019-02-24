import ctypes
import os

def zhThinning(img):
    #route = path.encode('UTF-8')
    #route = ctypes.create_string_buffer(route)
    a = os.getcwd()+'/zst.so'
    a = ctypes.cdll.LoadLibrary(a)
    return a.zhThinning(img)
    #return path        