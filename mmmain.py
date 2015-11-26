#!/usr/bin/python

from random_generator import MMGenerate
from mmsystem import MMSystem
from mmreporter import MMReporter
from mmsimulator import MMSimulator

import time
import numpy as np

def simulator_driver():
    """Reuse this function to get n replication of simulation"""
    num_srv = 2
    num_buffer = 5
    num_pkt_init = 0
    end_time = 1000000
    pkt_seq_len = 50000

    mm27 = MMSystem(num_srv, num_buffer)

    ats = MMGenerate(pkt_seq_len, 0.1, int(time.time()))    # arrival interval
    ats = np.cumsum(ats)                                    # arrival time stamp

    dts = MMGenerate(pkt_seq_len, 1, int(time.time()))      # departure time stamp

    # ats = [round(i, 2) for i in ats]
    # dts = [round(j, 2) for j in dts]

    observe_interval = 0.05
    # ots = [observe_interval for _ in range(0, \
            # int(end_time / observe_interval) + 1)]
    # ots = np.cumsum(ots) # obverse time stamp

    simulator = MMSimulator(mm27, observe_interval, end_time)
    simulator.init_simulation(num_pkt_init)

    t0 = time.time()
    simulator.simulate_core(ats, dts)

    reporter = MMReporter(mm27)

    duration = time.time() - t0

    print "The duration of this trial is %fs" %duration

    print "blocking probability", reporter.blocking_prob()
    print "mean time pkt spending in system", \
            reporter.mean_time_spending_in_system()
    print "mean number of pkt in system", reporter.mean_num_pkt_in_system()

def main():
    simulator_driver()

if __name__ == '__main__':
    main()


