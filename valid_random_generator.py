#!/usr/bin/python

import numpy as np
from time import time
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def rg_fitness():
    mu, sigma = 100, 15
    x = mu + sigma * np.random.randn(10000)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # the histogram of the data
    n, bins, patches = ax.hist(x, 50, normed=1, facecolor='green', \
                               alpha=0.75, label="Normalized Histogram")

    # hist uses np.histogram under the hood to create 'n' and 'bins'.
    # np.histogram returns the bin edges, so there will be 50 probability
    # density values in n, 51 bin edges in bins and 50 patches.  To get
    # everything lined up, we'll compute the bin centers
    bincenters = 0.5*(bins[1:]+bins[:-1])
    # add a 'best fit' line for the normal PDF
    y = mlab.normpdf( bincenters, mu, sigma)
    ax.plot(bincenters, y, 'r--', linewidth=1, label='PDF of Normal Distribution')

    ax.set_xlabel('Random Values')
    ax.set_ylabel('Probability')

    ax.set_xlim(40, 160)
    ax.set_ylim(0, 0.035)
    ax.grid(True)
    plt.legend()
    plt.savefig('rg_fitness.eps', format='eps')

def rg_histogram():
    #1.1 Does your RNG generate random numbers?
    randgen_1 = np.random.RandomState(1)
    list_random = []
    number = 10000
    for i in range(0, number):
        list_random.append(randgen_1.rand())

    print "1.1 Does your RNG generate random numbers?"
    print "Plot the histogram of generated random numbers"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n, bins, patches = ax.hist(list_random, bins=100, normed=1, facecolor='green', \
                               alpha=0.75, label='Normalized Histogram')
    fit = [1 for x in bins]
    ax.plot(bins, fit, 'r--', linewidth=1, label='PDF of Uniform Distribution')
    ax.set_xlabel("Generated Random Value")
    ax.set_ylabel("Count in Each Bin")
    ax.grid(True)
    plt.legend()
    plt.savefig('rg_histogram.eps', format='eps')

def rg_seed():
    """How do you initialize the seed of your RNG?"""
    current_time = time()
    np.random.RandomState(int(current_time))
    print "1.2 How do you initialize the seed of your RNG?"
    print "Use current time as int type: %s\n" % int(current_time)

def rg_diff():
    """Generate two sequences of 1000000 numbers each
    for every sequence use a different seed.
    """
    randgen1 = np.random.RandomState(1)
    randgen2 = np.random.RandomState(2)

    listA = randgen1.uniform(low=0.0, high=1.0, size=1000000)
    listB = randgen2.uniform(low=0.0, high=1.0, size=1000000)

    A, B = stats.mstats.ttest_ind(listA, listB)
    print "The p-value is %s, the t-statistics is %s" % (B, A)

    overall = np.append(listA,listB)

    # Using set operation to differentiate 2 different lists
    # We know that for set, every element is identical.
    # So we can find the length of the set after we combine 2 lists.
    # Method 1
    temp3 = tuple(set(listA) - set(listB))
    print len(temp3)
    # Method 2
    set_overall = set(overall)
    print len(set_overall)

if __name__ == "__main__":
    rg_histogram()
    rg_fitness()
    rg_seed()
    rg_diff()
