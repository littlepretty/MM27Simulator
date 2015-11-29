#!/usr/bin/python

from mmevent import MMEvent

class MMSimulator(object):
    """Simulator for M/M/2/7 system"""
    def __init__(self, system, end_time):
        super(MMSimulator, self).__init__()
        self.system = system
        self.end_time = end_time
        self.clock = 0
        self.initialized = False

    def init_simulation(self, num_pkt_init):
        """Initialize simulator before its core"""
        self.init_system_status(num_pkt_init)
        self.init_event_list()
        self.initialized = True

    def init_system_status(self, num_pkt_init):
        """Set system initial status"""
        self.system.log_time.append(0)
        self.system.log_num_pkt_inside.append(num_pkt_init)
        # initial number of pkt may large than system capacity
        num_busy_srv = num_pkt_init - self.system.capacity
        if num_busy_srv > 0 and num_busy_srv <= self.system.num_srv:
            for i in range(0, num_busy_srv):
                self.system.srv_status[i] = 'busy'

    def init_event_list(self):
        """Do necessary initialization"""
        self.event_list = []

    def sort_event_list(self):
        """Sort event list on time stamp of every events"""
        self.event_list.sort(key=lambda event: event.time_stamp, reverse=False)

    def last_departure_srv(self, srv_id):
        """Search in event list the last depart event
        with specified depart server id"""
        self.sort_event_list()
        for event in reversed(self.event_list):
            if event.evt_name == 'departure' and event.depart_srv == srv_id:
                return event

    def schedule_departure(self):
        """Find server for new depart event with the depart time stamp"""
        earliest_ts = None
        self.sort_event_list()
        for s_id in self.system.srv_status.keys():
            evt = self.last_departure_srv(s_id)
            if earliest_ts == None or earliest_ts > evt.time_stamp:
                earliest_ts = evt.time_stamp
                earliest_srv_id = s_id
        return (earliest_ts, earliest_srv_id)

    def next_event(self):
        """Pop up the earliest event"""
        self.sort_event_list()
        return self.event_list.pop(0)

    def should_continue(self):
        """Test if @clock exceed predefined @end_time"""
        return self.clock < self.end_time

    def simulate_core(self, arrive_time_seq, depart_time_seq_server1, depart_time_seq_server2):
        """Discrete event simulation"""
        if not self.initialized:
            print "Simulator is not explicitly initialized"

        N = len(arrive_time_seq)
        flag_server1 = 0
        flag_server2 = 0

        while self.system.pkt_served + self.system.pkt_dropped < N and self.should_continue():
            # schedule/add a new pkt arrive event
            if self.system.pkt_seen < N:
                new_arrival_ts = arrive_time_seq[self.system.pkt_seen]
                new_arrive = MMEvent(self.system.pkt_seen, 'arrival', new_arrival_ts)
                self.event_list.append(new_arrive)
                self.system.pkt_seen += 1

            # pop up the next event
            evt_x = self.next_event()
            # advance simulation clock
            self.clock = evt_x.time_stamp

            if evt_x.evt_name == 'departure':
                # set the serving server to 'idle'
                # increase @pkt_served counter
                # calculate how long this pkt spend in @system
                if self.system.pkt_waiting == 0:
                    self.system.srv_status[evt_x.depart_srv] = 'idle'
                else:
                    self.system.pkt_waiting -= 1

                evt_x.exit_time = self.clock
                # either server became idle or waiting pkt decreased
                # log num_pkt_inside the system
                self.system.dump_num_pkt_inside(self.clock)
                # calculate the spending time of this packet
                self.system.dump_pkt_spending_time(evt_x)
                self.system.pkt_served += 1

            if evt_x.evt_name == 'arrival':
                if self.system.full():
                    # just drop pkt and increase counter
                    self.system.pkt_dropped += 1
                    # no departure event for this pkt is created
                    # but need to count its spending time/ not to count
                    evt_x.exit_time = evt_x.enter_time = 0
                    # self.system.dump_pkt_spending_time(evt_x)
                else:
                    if self.system.available():
                        # put pkt into one available server
                        # calculate when it should exit the server
                        # mark this server as 'busy'
                        new_depart_srv = self.system.available_server()
                        if new_depart_srv == 0:
                            new_depart_ts = self.clock + depart_time_seq_server1[flag_server1]
                            flag_server1 += 1
                        else:
                            new_depart_ts = self.clock + depart_time_seq_server2[flag_server2]
                            flag_server2 += 1

                        self.system.srv_status[new_depart_srv] = 'busy'
                    else:
                        # find the server pkt should go
                        earliest_ts, earliest_srv = self.schedule_departure()
                        if earliest_srv == 0:
                            new_depart_ts = earliest_ts + depart_time_seq_server1[flag_server1]
                            flag_server1 += 1
                        else:
                            new_depart_ts = earliest_ts + depart_time_seq_server2[flag_server2]
                            flag_server2 += 1

                        new_depart_srv = earliest_srv
                        self.system.pkt_waiting += 1

                    # either server became busy or waiting packet increases
                    # log num_pkt_inside the system
                    self.system.dump_num_pkt_inside(self.clock)
                    # actually insert new departure event
                    new_depart = MMEvent(evt_x.pkt_id, 'departure', new_depart_ts)
                    new_depart.enter_time = self.clock
                    new_depart.depart_srv = new_depart_srv
                    self.event_list.append(new_depart)

