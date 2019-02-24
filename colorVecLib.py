import ctypes
import os
from numpy.ctypeslib import ndpointer

def colorVector(path):
    route = path.encode('UTF-8')
    route = ctypes.create_string_buffer(route)
    a = ctypes.cdll.LoadLibrary('./libcvector.so')
    a.foo.restype = ndpointer(dtype=ctypes.c_float, shape=(10,))
    returnVector = a.foo(route)
    return returnVector