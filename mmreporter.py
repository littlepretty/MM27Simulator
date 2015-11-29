#!/usr/bin/python

import bisect

class MMReporter(object):
    """Calculate system measurements"""
    def __init__(self, system):
        super(MMReporter, self).__init__()
        self.system = system

    def blocking_prob(self):
        """Blocking probability"""
        return float(self.system.pkt_dropped) / float(self.system.pkt_seen)

    def mean_time_spending_in_system(self):
        """Mean time pkt spending in the system"""
        dur_sum = 0.0
        spending_time_seq = self.system.spending_time.values()
        start = int(len(spending_time_seq) / 3.0)
        end = len(spending_time_seq)
        for i in range(start, end):
            dur_sum += spending_time_seq[i]
        return dur_sum / (end - start)

    def mean_num_pkt_in_system(self):
        """Mean number of pkt in the system"""
        num_pkt_duration = {}
        entire_duration = 0.0
        product_sum = 0.0

        start = int(len(self.system.log_time) / 3.0) - 1
        end = len(self.system.log_time) - 1
        for i in range(start, end):
            dur = self.system.log_time[i+1] - self.system.log_time[i]
            num_pkt = self.system.log_num_pkt_inside[i]
            if num_pkt in num_pkt_duration:
                num_pkt_duration[num_pkt] += dur
            else:
                num_pkt_duration[num_pkt] = dur
            entire_duration += dur

        for num_pkt, dur in num_pkt_duration.items():
            product_sum += num_pkt * dur
        return product_sum / entire_duration

    def warm_up_finding(self, interval_sequence):

        #print interval_sequence
        output = []

        for i in interval_sequence:
            index = bisect.bisect_left(self.system.log_time, i)
            index = index - 1
            output.append(self.system.log_num_pkt_inside[index])

        return output

