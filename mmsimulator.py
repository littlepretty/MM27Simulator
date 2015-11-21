#!/usr/bin/python

from mmevent import MMEvent
from random_generator import MMGenerate
from mmsystem import MMSystem
import time
import numpy as np

class MMSimulator(object):
    """Simulator for M/M/2/7 system"""
    def __init__(self, system, end_time):
        super(MMSimulator, self).__init__()
        self.system = system
        self.init_event_list()
        self.end_time = end_time
        self.pkt_seen = 0
        self.clock = 0

    def init_event_list(self):
        """Do necessary initialization"""
        self.event_list = []

    def last_departure_srv(self, srv_id):
        """Search in event list the last departure event
        with specified depart server id"""
        for event in reversed(self.event_list):
            if event.evt_name == 'departure' and event.depart_srv == srv_id:
                return event

    def schedule_departure(self):
        """Find a server for new departure event, with
        the departure time stamp"""
        earliest_ts = None
        self.sort_event_list()
        for s_id in self.system.srv_status.keys():
            evt = self.last_departure_srv(s_id)
            if earliest_ts == None or earliest_ts > evt.time_stamp:
                earliest_ts = evt.time_stamp
                earliest_srv_id = s_id
        return (earliest_ts, earliest_srv_id)

    def sort_event_list(self):
        """Sort event list on time stamp of every events"""
        self.event_list.sort(key=lambda event: event.time_stamp, reverse=False)

    def next_event(self):
        """Sort @event_list and pop up the first event
        """
        self.event_list.sort(key=lambda event: event.time_stamp, reverse=False)
        return self.event_list.pop(0)

    def should_continue(self):
        """Test if @clock exceed predefined @end_time"""
        return self.clock < self.end_time

    def simulate_core(self, arrive_time_seq, depart_time_seq):
        """Discrete event simulation"""
        N = len(arrive_time_seq)
        while self.system.pkt_served + self.system.pkt_dropped < N and self.should_continue():
            # schedule/add a new pkt arrive event
            if self.pkt_seen < N:
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
                if self.system.waiting == 0:
                    self.system.srv_status[evt_x.depart_srv] = 'idle'
                else:
                    self.system.waiting -= 1
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

        print [round(x, 2) for x in self.system.spending_time.values()]


def main():
    ns = 2
    nb = 5
    et = 100000
    mm27 = MMSystem(ns, nb)
    simulator = MMSimulator(mm27, et)
    ats = MMGenerate(10, 0.5, int(time.time()))
    dts = MMGenerate(10, 1, int(time.time()))
    ats = np.cumsum(ats)
    ats = [round(i, 2) for i in ats]
    dts = [round(j, 2) for j in dts]
    #print ats
    #print dts
    #time.sleep(10)
    ats = [6.09, 6.65, 7.66, 8.41, 9.0]
    dts = [7.32, 1.13, 2.0, 1.51, 1.17]
    simulator.simulate_core(ats, dts)

if __name__ == '__main__':
    main()


