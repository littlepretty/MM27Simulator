#!/usr/bin/python

from random_generator import MMGenerateArrivals, MMGenerateDepartures

class MMEvent(object):
    """Abstraction of packet arrival or departure

    Attributes:
        @pkt_id: which packet this event is about
        @event_type(str): 'arrival' or 'departure'
        @time_stamp: when should we handle this event;
            we need this value to put event into event_list
        @enter_time: the moment it enter the system
        @exit_time: the moment it exit the system
    """
    def __init__(self, pkt_id, name, ts):
        super(MMEvent, self).__init__()
        self.pkt_id = pkt_id
        self.evt_name = name
        self.time_stamp = ts
        self.enter_time = 0
        self.exit_time = 0
        self.depart_srv = None

class MMSystem(object):
    """Various counters for M/M/2/2+5 system

    Attributes:
        @dropped_pkt: number of packet dropped so far
        @waiting: number of packet in the system queue
        @pkt_served: number of packet exited
        @spending_time: how much each packet is spending
            in the system
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

class MMSimulator(object):
    """Simulation core
    """
    def __init__(self, system, end_time):
        super(MMSimulator, self).__init__()
        self.system = system
        self.init_event_list()
        self.end_time = end_time
        self.pkt_seen = 0
        self.clock = 0

    def init_event_list(self):
        """Do necessary initialization
        """
        self.event_list = []

    def last_departure_srv(self, srv_id):
        for event in reversed(self.event_list):
            if event.evt_name == 'departure' and event.depart_srv == srv_id:
                return event

    def schedule_departure(self):
        earliest_ts = None
        self.sort_event_list()
        for s_id in self.system.srv_status.keys():
            evt = self.last_departure_srv(s_id)
            if earliest_ts == None or earliest_ts > evt.ts:
                earliest_ts = evt.ts
                earliest_srv_id = s_id
        return (earliest_ts, earliest_srv_id)

    def sort_event_list(self):
        self.event_list.sort(key=lambda event: event.time_stamp, reverse=False)

    def next_event(self):
        """Sort @event_list and pop up the first event
        """
        self.event_list.sort(key=lambda event: event.time_stamp, reverse=False)
        return self.event_list.pop(0)

    def should_continue(self):
        """If @clock exceed predefined @end_time"""
        return self.clock < self.end_time

    def simulate_core(self, arrive_time_seq, depart_time_seq):
        """Discrete event simulation"""
        N = len(arrive_time_seq)
        while self.system.pkt_served < N and self.should_continue():
            # schedule/add a new pkt arrive event
            new_arrival_ts = arrive_time_seq[self.pkt_seen]
            new_arrive = MMEvent(self.pkt_seen, 'arrival', new_arrival_ts)
            self.event_list.append(new_arrive)
            self.pkt_seen += 1

            # pop up the next event
            evt_x = self.next_event()
            # advance simulation clock
            self.clock = evt_x.time_stamp

            if evt_x.evt_name == 'departure':
                # set the serving server to 'idle'
                # increase @pkt_served counter
                # calculate how long this pkt spend in @system
                self.system.srv_status[evt_x.depart_srv] = 'idle'
                self.system.pkt_served += 1
                evt_x.exit_time = self.clock
                spend = evt_x.exit_time - evt_x.enter_time
                self.system.spending_time[evt_x.pkt_id] = spend
            if evt_x.evt_name == 'arrival':
                if self.system.full():
                    # just drop pkt and increase counter
                    self.system.pkt_dropped += 1
                else:
                    if self.system.available():
                        # put pkt into one available server
                        # calculate when it should exit the server
                        # mark this server as 'busy'
                        new_depart_ts = self.clock + depart_time_seq[evt_x.pkt_id]
                        new_depart_srv = self.system.available_server()
                        self.system.srv_status[new_depart_srv] = 'busy'
                    else:
                        # find the server pkt should go
                        earliest_ts, earliest_srv = self.schedule_departure()
                        new_depart_ts = earliest_ts + depart_time_seq[evt_x.pkt_id]
                        new_depart_srv = earliest_srv
                        self.system.waiting += 1

                    new_depart = MMEvent(evt_x.pkt_id, 'departure', new_depart_ts)
                    new_depart.enter_time = self.clock
                    new_depart.depart_srv = new_depart_srv

                    self.event_list.append(new_depart)


def main():
    ns = 2
    nb = 5
    et = 100000
    mm27 = MMSystem(ns, nb)
    simulator = MMSimulator(mm27, et)
    ats = MMGenerateArrivals()
    dts = MMGenerateDepartures()
    simulator.simulate_core(ats, dts)

if __name__ == '__main__':
    main()


