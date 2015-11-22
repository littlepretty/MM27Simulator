#!/usr/bin/python

class MMEvent(object):
    """Abstraction of packet arrival or departure"""
    def __init__(self, pkt_id, name, ts):
        """Create MMEvent object

        Attributes:
            pkt_id: which packet this event is about
            event_type(str): 'arrival' or 'departure'
            time_stamp: when should we handle this event;
                we need this value to put event into event_list
            enter_time: the moment it enter the system
            exit_time: the moment it exit the system
        """
        super(MMEvent, self).__init__()
        self.pkt_id = pkt_id
        self.evt_name = name
        self.time_stamp = ts
        self.enter_time = 0
        self.exit_time = 0
        self.depart_srv = None

