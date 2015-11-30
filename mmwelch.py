#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt
import math

class MMWelch(object):
    """Welch graphic method to eliminate warm-up period"""
    def __init__(self, num_replicas, interval, run_length, prefix, mode='online'):
        """Create object with

        Attributes:
            num_replicas: to average these number of replicas
            run_length: the min length over all replications
            interval & time_seq: to draw simulation time
            prefix: name for output .txt and .eps files
        """
        super(MMWelch, self).__init__()
        self.num_replicas = float(num_replicas)
        self.run_length = run_length
        self.interval = float(interval)
        self.time_seq = [self.interval * i for i in range(0, self.run_length)]
        print "Use min length %d as common length " % self.run_length
        self.prefix = prefix
        self.mode = mode
        if self.mode == 'online':
            self.avg_run = [0] * self.run_length

    def average_all_runs(self):
        """Average all replica runs, store in self.avg_run"""
        for i in range(0, int(self.num_replicas)):
            # truncate only the common part of each runs
            replica = np.loadtxt('%sRuns%d.txt' % (self.prefix, i), dtype=int, comments='#')
            replica = replica[:self.run_length]
            self.avg_run = np.add(replica, self.avg_run)
        # average and save
        self.avg_run = [float(x) / self.num_replicas for x in self.avg_run]
        file_name = self.prefix + 'Avg%d.txt' % self.num_replicas
        np.savetxt(file_name, self.avg_run)

    def plot_avg_run(self):
        """Draw a figure, output to file"""
        if self.mode == 'offline':
            self.avg_run = np.loadtxt('%sAvg%d.txt' % (self.prefix, self.num_replicas))
            self.run_length = len(self.avg_run)
            self.time_seq = [self.interval * i for i in range(0, self.run_length)]

        y_max = math.ceil(max(self.avg_run)) + 0.5
        x_max = math.ceil(self.time_seq[-1] / 10) * 10

        figure_name = self.prefix + 'Avg%d.eps' % self.num_replicas
        plt.figure()
        plt.plot(self.time_seq, self.avg_run)
        plt.xlabel('Wall clock time / second')
        plt.ylabel('Number packet in system')
        plt.xticks(np.arange(0, x_max, x_max / 10.0))
        plt.yticks(np.arange(0, y_max, y_max / 10.0))
        plt.xlim(self.time_seq[0], self.time_seq[-1])
        plt.ylim(0, y_max)
        plt.grid()
        plt.savefig(figure_name, format='eps')

