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

def simulator_driver(trial, l, u, num_pkt_init, num_pkts, obsrv_int, seed, prefix):
    """Reuse this function to get many replicas of simulation"""
    # ending time is dependent with arriving rate.
    end_time = 1000

    mm27 = MMSystem(num_srv, num_buffer)

    # arrival interval
    ats = MMGenerate(num_pkts, 1.0 / l, seed)
    # arrival time stamp
    ats = np.cumsum(ats)
    # insert init pkt events
    init_ats = np.array([0] * num_pkt_init)
    ats = np.insert(ats, 0, init_ats)

    # departure time stamp
    dts_server1 = MMGenerate(num_pkts + num_pkt_init, u, seed + 1)
    dts_server2 = MMGenerate(num_pkts + num_pkt_init, u, seed + 2)

    simulator = MMSimulator(mm27, end_time)
    simulator.init_simulation(num_pkt_init)

    t0 = time.time()
    simulator.simulate_core(ats, dts_server1, dts_server2)

    reporter = MMReporter(mm27)

    duration = time.time() - t0
    end_time = int(math.ceil(simulator.clock))
    ots = [obsrv_int for _ in range(0, int(end_time / obsrv_int) + 1)]
    ots = np.cumsum(ots) # obverse time stamp

    # output results to this file
    file_name = prefix + 'Run%d.txt' % trial
    # align results to observation intervals
    observations = reporter.warm_up_finding(ots)
    # output statistic results as header
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
    # for main to get min common simulation length
    return len(observations)

def eliminate_warmup_period(l, u, num_pkt_init, seed):
    num_obsrv = 999999
    num_trials = 5000
    num_pkts = 1000
    obsrv_int = min(0.01, 1.0 / l / 10)
    prefix = 'Lmda%dInit%d' % (l, num_pkt_init)
    for i in range(num_trials):
        new_obsrv = simulator_driver(i, l, u, num_pkt_init, num_pkts, obsrv_int, seed, prefix)
        num_obsrv = min(num_obsrv, new_obsrv)
        seed += 10
    welch = MMWelch(num_trials, obsrv_int, num_obsrv, prefix)
    welch.average_all_runs()
    # welch = MMWelch(trial, obsrv_int, num_obsrv, l, 'offline')
    welch.plot_avg_run()

def run_system(l, u, num_pkt_init):
    seed = int(time.time())
    eliminate_warmup_period(l, u, num_pkt_init, seed)

def main():
    run_system(lambdaA, u, 0)
    run_system(lambdaA, u, 7)
    run_system(lambdaB, u, 0)
    run_system(lambdaB, u, 4)

if __name__ == '__main__':
    num_srv = 2
    num_buffer = 5
    lambdaA = 2.0
    lambdaB = 10.0
    u = 1.0

    main()
