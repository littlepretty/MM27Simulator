__author__ = 'Ping'
import numpy as np

def MMGenerate(length, mu, seed):
    """Generate exponential random sequence with seed"""
    randgen = np.random.RandomState(seed)
    return randgen.exponential(scale=mu, size=length)

def MMGenerateSingle(mu, seed):
    """Generate one exponential random value with seed"""
    randgen = np.random.RandomState(seed)
    random_values = randgen.exponential(scale=mu, size=1)
    return random_values[0]
