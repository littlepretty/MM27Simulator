#!/usr/bin/python

from mmrng import MMGenerate
from mmsystem import MMSystem
from mmreporter import MMReporter
from mmsimulator import MMSimulator
from mmwelch import MMWelch

import time, math
import numpy as np

def roundup_hundreds(num):
    """To round up ending time of the simulation"""
    return int(math.ceil(num / 100)) * 100

def simulator_driver(trial, l, u, obsrv_int):
    """Reuse this function to get n replication of simulation"""
    # ending time is dependent with arriving rate.
    end_time = 1000

    mm27 = MMSystem(num_srv, num_buffer)

    # arrival interval
    ats = MMGenerate(pkt_seq_len, 1.0 / l, seed)
    # arrival time stamp
    ats = np.cumsum(ats)

    # departure time stamp
    dts_server1 = MMGenerate(pkt_seq_len, u, seed + 1)
    dts_server2 = MMGenerate(pkt_seq_len, u, seed + 2)

    simulator = MMSimulator(mm27, end_time)
    simulator.init_simulation(num_pkt_init)

    t0 = time.time()
    simulator.simulate_core(ats, dts_server1, dts_server2)

    reporter = MMReporter(mm27)

    duration = time.time() - t0
    end_time = int(math.ceil(simulator.clock))
    ots = [obsrv_int for _ in range(0, int(end_time / obsrv_int) + 1)]
    ots = np.cumsum(ots) # obverse time stamp

    file_name = str(trial) + ".txt"
    output_file = open(file_name, 'w+')
    observations = reporter.warm_up_finding(ots)
    output_file.write("########################################################\n")
    output_file.write("################## Simulation results ##################\n")
    output_file.write("########################################################\n")
    output_file.write("#Running time of NO.%d trial %.4fs\n" % (trial, duration))
    output_file.write("#Ending event time stamp %.4f\n" % end_time)
    output_file.write("#Blocking probability %.4f\n" % reporter.blocking_prob())
    output_file.write("#Mean time spent in system %.4f\n" % reporter.mean_time_spending_in_system())
    output_file.write("#Mean #pkt in system %.4f\n" % reporter.mean_num_pkt_in_system())
    output_file.write("########################################################\n")
    np.savetxt(file_name, observations, fmt='%i', delimiter= ',')

    return len(observations)

def main(l):
    global seed, pkt_seq_len, trail
    num_obsrv = 99999
    obsrv_int = min(0.01, 1.0 / l / 10)
    for i in range(trial):
        new_obsrv = simulator_driver(i, l, u, obsrv_int)
        num_obsrv = min(num_obsrv, new_obsrv)
        seed += 10
    welch = MMWelch(trial, obsrv_int, num_obsrv, l)
    welch.average_all_runs()
    # welch = MMWelch(trial, obsrv_int, num_obsrv, l, 'offline')
    welch.plot_avg_run()

if __name__ == '__main__':
    num_srv = 2
    num_buffer = 5
    lambdaA = 2.0
    lambdaB = 10.0
    u = 1.0
    num_pkt_init = 0
    trial = 5000
    pkt_seq_len = 1000

    seed = int(time.time())
    main(lambdaA)
    # seed = int(time.time())
    # main(lambdaB)

