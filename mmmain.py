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

    optional_output = '' 
    optional_output += "########################################################\n"
    optional_output += "################## Simulation results ##################\n"
    optional_output += "########################################################\n"
    optional_output += "#Running time of NO.%d trial %.4fs\n" % (trial, duration)
    optional_output += "#Ending event time stamp %.4f\n" % end_time
    optional_output += "#Blocking probability %.4f\n" % reporter.blocking_prob()
    optional_output += "#Mean time spent in system %.4f\n" % reporter.mean_time_spending_in_system()
    optional_output += "#Mean #pkt in system %.4f\n" % reporter.mean_num_pkt_in_system()
    optional_output += "########################################################\n"
    np.savetxt(file_name, observations, fmt='%i', header=optional_output, comments='#')    
 
    return len(observations)

def main(l):
    global seed, pkt_seq_len, trail
    num_obsrv = 999999
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
    trial = 5
    pkt_seq_len = 5 

    seed = int(time.time())
    main(lambdaA)
    # seed = int(time.time())
    # main(lambdaB)

