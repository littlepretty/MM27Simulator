#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt
import math

class MMWelch(object):
    """Welch graphic method to eliminate warm-up period"""
    def __init__(self, num_replicas, interval, run_length, l):
        super(MMWelch, self).__init__()
        self.num_replicas = float(num_replicas)
        self.run_length = run_length
        self.interval = float(interval)
        self.l = float(l)
        self.avg_run = [0] * self.run_length
        self.time_seq = [self.interval * i for i in range(0, self.run_length)]

    def average_all_runs(self):
        for i in range(0, int(self.num_replicas)):
            # truncate only the common part of each runs
            replica = np.loadtxt('%d.txt' % i, dtype=int)
            # print "run length = ", len(replica)
            replica = replica[:self.run_length]
            self.avg_run = np.add(replica, self.avg_run)
        # average and save
        self.avg_run = [float(x) / self.num_replicas for x in self.avg_run]
        np.savetxt('avg_run.txt', self.avg_run)

    def plot_avg_run(self):
        y_max = math.ceil(max(self.avg_run))
        x_max = math.ceil(self.time_seq[-1] / 10) * 10
        figure_name = 'Lambda%dAvg%dRuns.eps' % (self.l, self.num_replicas)

        plt.figure()
        plt.plot(self.time_seq, self.avg_run)
        plt.xticks(np.arange(0, x_max, x_max / 10.0))
        plt.yticks(np.arange(0, y_max, y_max / 10.0))
        plt.xlim(self.time_seq[0], self.time_seq[-1])
        plt.ylim(0, y_max)
        plt.grid()
        plt.savefig(figure_name, format='eps')

