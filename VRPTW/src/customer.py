# -*- coding: utf-8 -*-
"""
Customer Representation for VRPTW instances

Author: Peterson Katagiri Zilli <peterson.zilli@gmail.com>
Date: 2018-01-25
"""

class Customer:
    """Customer Class for VRPTW"""
    def __init__(self, customer_info=None):
        self.prev_customer = None
        self.next_customer = None
        self.route = None
        self.arival = None
        self.waiting_time = None

        if isinstance(customer_info, list) and len(customer_info) == 7:
            self.number = customer_info[0]
            self.xcoord = customer_info[1]
            self.ycoord = customer_info[2]
            self.demand = customer_info[3]
            self.time_windows = [(customer_info[4], customer_info[5])]
            self.service_time = customer_info[6]
        
        elif isinstance(customer_info, Customer):
            c = customer_info
            self.number = c.number
            self.xcoord = c.xcoord
            self.ycoord = c.ycoord
            self.demand = c.demand
            self.time_windows = [tuple(x) for x in c.time_windows]
            self.service_time = c.service_time
        
        else:
            raise NotImplementedError('Custsomer initialization not implemented for data that is not a list with customer info or another customer object')