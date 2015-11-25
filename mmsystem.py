#!/usr/bin/python

class MMSystem(object):
    """Various system states and counters for M/M/2/2+5 system

    Attributes:
        dropped_pkt: number of packet dropped so far
        pkt_waiting: number of packet in the system queue
        pkt_served: number of packet exited
        spending_time: how much each packet is spending in the system
    """
    def __init__(self, num_srv, capacity, num_pkt_inside):
        super(MMSystem, self).__init__()
        # immutable properties
        self.num_srv = num_srv
        self.capacity = capacity

        # couters
        self.pkt_dropped = 0
        self.pkt_seen = 0
        self.pkt_waiting = 0
        self.pkt_served = 0

        # result log info
        self.spending_time = {}
        self.log_time = []
        self.log_time.append(0)
        self.log_num_pkt_inside = []
        self.log_num_pkt_inside.append(num_pkt_inside)

        # state variables
        self.stable = False
        self.srv_status = {}
        for i in range(0, self.num_srv):
            self.srv_status[i] = 'idle'

    def full(self):
        """Test if the queue is full"""
        return self.pkt_waiting >= self.capacity

    def available(self):
        """Test if any server is idle"""
        return 'idle' in self.srv_status.values()

    def num_available_servers(self):
        counter = 0
        for key, value in self.srv_status.items():
            if value == 'idle':
                counter += 1
        return counter

    def dump_num_pkt_inside(self, time):
        self.log_time.append(time)
        num_pkt_inside = self.pkt_waiting + self.num_available_servers()
        self.log_num_pkt_inside.append(num_pkt_inside)

    def dump_pkt_spending_time(self, evt):
        self.spending_time[evt.pkt_id] = evt.exit_time - evt.enter_time

    def available_server(self):
        """Find any 'idle' server in system"""
        for key, value in self.srv_status.items():
            if value == 'idle':
                return key

