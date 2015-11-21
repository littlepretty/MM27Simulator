__author__ = 'Ping'
import numpy as np

def MMGenerate(length, miu, seed):
    randgen = np.random.RandomState(seed)
    return randgen.exponential(scale = miu, size = length)
