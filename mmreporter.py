#!/usr/bin/python

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
        n = float(len(self.system.spending_time.values()))

        for dur in self.system.spending_time.values():
            dur_sum += dur
        return dur_sum / n

    def mean_num_pkt_in_system(self):
        """Mean number of pkt in the system"""
        num_pkt_duration = {}
        entire_duration = 0.0

        for i in range(0, len(self.system.log_time) - 1):
            dur = self.system.log_time[i+1] - self.system.log_time[i]
            num_pkt = self.system.log_num_pkt_inside[i]
            if num_pkt in num_pkt_duration:
                num_pkt_duration[num_pkt] += dur
            else:
                num_pkt_duration[num_pkt] = dur

            entire_duration += dur

        product_sum = 0.0
        for num_pkt, dur in num_pkt_duration.items():
            product_sum += num_pkt * dur
        return product_sum / entire_duration


