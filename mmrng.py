#!/usr/bin/python

import numpy as np

def generate_exp(length, mu, seed):
    """Generate exponential random sequence with seed"""
    randgen = np.random.RandomState(seed)
    return randgen.exponential(scale=mu, size=length)

def generate_exp_single(mu, seed):
    """Generate one exponential random value with seed"""
    randgen = np.random.RandomState(seed)
    random_values = randgen.exponential(scale=mu, size=1)
    return random_values[0]
