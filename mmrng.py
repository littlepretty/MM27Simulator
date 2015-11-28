__author__ = 'Ping'
import numpy as np

def MMGenerate(length, mu, seed):
    randgen = np.random.RandomState(seed)
    return randgen.exponential(scale=mu, size=length)
