#!/usr/bin/python

from random_generator import MMGenerate
from mmsystem import MMSystem
from mmreporter import MMReporter
from mmsimulator import MMSimulator

import time
import numpy as np

def simulator_driver(trial_index):

    """Reuse this function to get n replication of simulation"""
    trail = trial_index
    num_srv = 2
    num_buffer = 5
    num_pkt_init = 0
    # ending time is dependent with arriving rate.
    end_time = 1000
    pkt_seq_len = 5000



    mm27 = MMSystem(num_srv, num_buffer)

    ats = MMGenerate(pkt_seq_len, 0.1, int(time.time()))    # arrival interval
    ats = np.cumsum(ats)                                    # arrival time stamp
    print "last arrival event time stamp:", ats[-1]

    dts_server1 = MMGenerate(pkt_seq_len, 1, int(time.time()))      # departure time stamp
    dts_server2 = MMGenerate(pkt_seq_len, 1, int(time.time()+1))
    # ats = [round(i, 2) for i in ats]
    # dts = [round(j, 2) for j in dts]
    observe_interval = 0.1

    ots = [observe_interval for _ in range(0, \
            int(end_time / observe_interval) + 1)]
    ots = np.cumsum(ots) # obverse time stamp

    #print len(ots)

    simulator = MMSimulator(mm27, observe_interval, end_time)
    simulator.init_simulation(num_pkt_init)

    t0 = time.time()
    simulator.simulate_core(ats, dts_server1, dts_server2)

    reporter = MMReporter(mm27)

    duration = time.time() - t0

    file_name = str(trail) + ".txt"
    np.savetxt(file_name, reporter.warm_up_finding(ots),fmt='%i',delimiter= ',')


    print "The duration of this trial is %fs" %duration

    print "blocking probability", reporter.blocking_prob()
    print "mean time pkt spending in system", \
            reporter.mean_time_spending_in_system()
    print "mean number of pkt in system", reporter.mean_num_pkt_in_system()
    print "#" * 75

def main():

    trial = 2
    for i in range(trial):

        simulator_driver(i)

if __name__ == '__main__':
    main()


