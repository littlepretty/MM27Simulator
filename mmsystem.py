#!/usr/bin/python

class MMSystem(object):
    """Various system states and counters for M/M/2/2+5 system

    Attributes:
        num_srv: number of servers in this system
        capacity: queue size of the system, excluding buffer on server
        pkt_seen: number of packets arrived so far
        pkt_dropped: number of packets dropped so far
        pkt_waiting: number of packets in the system queue
        pkt_served: number of packets exited
        spending_time: how much each packet is spending in the system
        log_time: starting time stamp that pkt in system is changed
        log_num_pkt_inside: history of number of packets in system
        stable: if we passed warm-up period
        srv_status: idle or busy for a particular server
    """
    def __init__(self, num_srv, capacity):
        super(MMSystem, self).__init__()
        # immutable properties
        self.num_srv = num_srv
        self.capacity = capacity

        # couters
        self.pkt_dropped = 0    # dropped due to buffer full
        self.pkt_seen = 0       # total arrived pkt
        self.pkt_waiting = 0    # pkt in buffer
        self.pkt_served = 0     # pkt departed from servers

        # result log info
        self.spending_time = {}
        self.log_time = []
        self.log_num_pkt_inside = []

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
        """Return number of available servers"""
        counter = 0
        for key, value in self.srv_status.items():
            if value == 'idle':
                counter += 1
        return counter

    def available_server(self):
        """Find any 'idle' server in system"""
        for key, value in self.srv_status.items():
            if value == 'idle':
                return key

    def dump_num_pkt_inside(self, time):
        """Update pkt inside system and log it with current time stamp"""
        self.log_time.append(time)
        if self.pkt_waiting > 0:
            num_pkt_inside = self.pkt_waiting + 2
        else:
            num_pkt_inside = 2 - self.num_available_servers()

        self.log_num_pkt_inside.append(num_pkt_inside)

    def dump_pkt_spending_time(self, evt):
        """Calculate the duration a pkt spent in the system"""
        self.spending_time[evt.pkt_id] = evt.exit_time - evt.enter_time


