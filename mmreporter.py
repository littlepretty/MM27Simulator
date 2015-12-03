#!/usr/bin/python

import bisect

class MMReporter(object):
    """Calculate system measurements"""
    def __init__(self, system, ats):
        super(MMReporter, self).__init__()
        self.system = system
        self.ats = ats
        self.obsrv_pkt = []

    def blocking_prob(self):
        """Blocking probability"""
        num_dropped = 0
        num_seen = 0

        for i in range(self.system.pkt_seen):
            if self.ats[i] > (self.system.log_time[-1] / 3.0):
                if i in self.system.pkt_dropped_id:
                    num_dropped += 1
                num_seen += 1

        return num_dropped/float(num_seen)
        #return float(self.system.pkt_dropped) / float(self.system.pkt_seen)

    def mean_time_spending_in_system(self):
        """Mean time pkt spending in the system"""
        dur_sum = 0.0
        spending_time_seq = self.system.spending_time.values()
        start = int(len(spending_time_seq) / 2.0)
        end = int(len(spending_time_seq) / 3.0 * 2)
        for i in range(start, end):
            dur_sum += spending_time_seq[i]
        return dur_sum / (end - start)

    def mean_num_pkt_in_system(self):
        """Mean number of pkt in the system"""
        num_pkt_duration = {}
        entire_duration = 0.0
        product_sum = 0.0

        start = int(len(self.system.log_time) / 2.0) - 1
        end = int(len(self.system.log_time) / 3.0 * 2) - 1
        for i in range(start, end):
            dur = self.system.log_time[i+1] - self.system.log_time[i]
            num_pkt = self.system.log_num_pkt_inside[i]
            if num_pkt in num_pkt_duration.keys():
                num_pkt_duration[num_pkt] += dur
            else:
                num_pkt_duration[num_pkt] = dur
            entire_duration += dur

        for num_pkt, dur in num_pkt_duration.items():
            product_sum += num_pkt * dur
        return product_sum / entire_duration

    def warm_up_finding(self, interval_sequence):
        """Find #pkt for all moment in interval sequence"""

        for i in interval_sequence:
            index = bisect.bisect_left(self.system.log_time, i)
            index = index - 1
            self.obsrv_pkt.append(self.system.log_num_pkt_inside[index])

        return self.obsrv_pkt

