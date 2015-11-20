#!/usr/bin/python

from enum import Enum
from random_generator import MMGenerateArrivals, MMGenerateDepartures

class MMEventType(Enum):
    arrival = 1
    departure = 2

class MMEvent(object):
    """Abstraction of packet arrival or departure

    Attributes:
        @pkt_id: which packet this event is about
        @event_type: a kind of MMEventType
        @time_stamp: when should we handle this event;
            we need this value to put event into event_list
        @enter_time: the moment it enter the system
        @exit_time: the moment it exit the system
    """
    def __init__(self, pkt_id, event_type, ts):
        super(MMEvent, self).__init__()
        self.pkt_id = pkt_id
        self.event_type = event_type
        self.time_stamp = ts
        self.enter_time = 0
        self.exit_time = 0
        self.depart_server = None

class MMSystem(object):
    """Various counters for M/M/2/2+5 system

    Attributes:
        @dropped_pkt: number of packet dropped so far
        @waiting: number of packet in the system queue
        @pkt_served: number of packet exited
        @spending_time: how much each packet is spending
            in the system
    """
    def __init__(self, num_servers, capacity):
        super(MMSystem, self).__init__()
        self.pkt_dropped = 0
        self.waiting = 0
        self.pkt_served = 0
        self.spending_time = {}
        self.num_servers = num_servers
        self.capacity = capacity
        self.server_status = {}
        for i in range(0, self.num_servers):
            self.server_status[i] = True

    def full(self):
        return self.waiting >= self.capacity

    def available(self):
        return True in self.server_status.values()

    def available_server(self):
        for key, value in self.server_status.items():
            if value == True:
                return key


def MMSimulateInit(system):
    """Do necessary initialization
    """
    event_list = []
    return event_list

def MMLastDeparture(event_list):
    for event in reversed(event_list):
        if event.event_type == MMEventType.departure:
            return event

def MMSimulateCore(system, event_list, arrive_time_seq, depart_time_seq, end_time):
    pkt_seen = 0
    N = len(arrive_time_seq)
    global_clock= 0
    while system.pkt_served < N and global_clock < end_time:
        new_arrival_ts = arrive_time_seq[pkt_seen]
        new_arrive = MMEvent(pkt_seen, MMEventType.arrival, new_arrival_ts)
        event_list.append(new_arrive)
        pkt_seen += 1

        event_list.sort(key=lambda event: event.time_stamp, reverse=False)
        evt_x = event_list.pop(0)
        global_clock = evt_x.time_stamp

        if evt_x.event_type == MMEventType.departure:
            system.available += 1
            system.pkt_served += 1
            evt_x.exit_time = global_clock
            spend = evt_x.exit_time - evt_x.enter
            system.spending_time[evt_x.pkt_id] = spend
        else: # evt_x.event_type == MMEventType.arrival:
            if system.full():
                system.pkt_dropped += 1
            else:
                if system.available():
                    new_depart_ts = global_clock + depart_time_seq[evt_x.pkt_id]
                    new_depart_server = system.available_server()
                else:
                    earliest_ts = None
                    for s_id in system.server_status.keys():
                        evt = MMLastDeparture(event_list, s_id)
                        if earliest_ts == None or earliest_ts > evt.ts:
                            earliest_ts = evt.ts
                            earliest_server = evt.server_id
                    new_depart_ts = earliest_ts + depart_time_seq[evt_x.pkt_id]
                    new_depart_server = earliest_server
                    system.waiting += 1

                new_depart = MMEvent(evt_x.pkt_id, MMEventType.departure, new_depart_ts, new_depart_server)
                new_depart.enter_time = global_clock
                new_depart.depart_server = new_depart_server

                event_list.append(new_depart)


def main():
    ns = 2
    nb = 5
    et = 100000
    mm27 = MMSystem(ns, nb)
    el = MMSimulateInit(mm27)
    ats = MMGenerateArrivals()
    dts = MMGenerateDepartures()
    MMSimulateCore(mm27, el, ats, dts, et)

if __name__ == '__main__':
    main()


