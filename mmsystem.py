#!/usr/bin/python

class MMSystem(object):
    """Various counters for M/M/2/2+5 system

    Attributes:
        dropped_pkt: number of packet dropped so far
        waiting: number of packet in the system queue
        pkt_served: number of packet exited
        spending_time: how much each packet is spending in the system
    """
    def __init__(self, num_srv, capacity):
        super(MMSystem, self).__init__()
        self.pkt_dropped = 0
        self.waiting = 0
        self.pkt_served = 0
        self.spending_time = {}
        self.num_srv = num_srv
        self.capacity = capacity
        self.srv_status = {}
        for i in range(0, self.num_servers):
            self.srv_status[i] = 'idle'

    def full(self):
        """Test if the queue is full"""
        return self.waiting >= self.capacity

    def available(self):
        """Test if any server is idle"""
        return 'idle' in self.srv_status.values()

    def available_server(self):
        """Find any 'idle' server in system"""
        for key, value in self.srv_status.items():
            if value == 'idle':
                return key

