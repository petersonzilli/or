# -*- coding: utf-8 -*-
"""
Route Representation for VRPMTW solution
Author: Peterson Katagiri Zilli <peterson.zilli@gmail.com>
Date: 2018-01-25
"""

from customer import Customer

class Route:
    """Route Class for VRPMTW"""
    def __init__(self, instance, solution):
        # setup route
        self.instance = instance
        self.solution = solution
        self.total_distance = 0.0
        self.total_demand = 0
        self.number_of_customers = 0

        # create customers
        self.first_customer = Customer(instance.customers[0])
        self.last_customer = Customer(instance.customers[0])

        # setup customers
        f = self.first_customer
        l = self.last_customer

        f.prev_customer = None
        f.next_customer = l
        f.route = self
        f.arival = 0.0
        f.waiting_time = 0.0

        l.prev_customer = f
        l.next_customer = None
        l.route = self
        l.arival = 0.0
        l.waiting_time = 0.0

    def insert(self, to_be_inserted_customer, previous_customer):
        """Inserts the 'to_be_inserted_customer' into the route, after 'previous_customer' and updates the route"""
        # saving previous and next customers
        pc = previous_customer
        nc = pc.next_customer

        # updating customers
        tbic = to_be_inserted_customer
        tbic.route = self

        tbic.prev_customer = pc
        tbic.next_customer = nc

        pc.next_customer = tbic
        nc.prev_customer = tbic
    
        # updating arival and waiting time from the inserted cutomer to the end
        self.update_arival_and_begin_times(tbic)
    
        #print('inserting customer', tbic.number)
        #print('into route', self)
        #print('between', pc.number, 'and', nc.number)

        # updating route and solution costs
        delta_cost = self.instance.dist(pc, tbic) + self.instance.dist(tbic, nc) - self.instance.dist(pc, nc)
        self.total_distance += delta_cost
        self.solution.total_distance = sum([r.total_distance for r in self.solution.routes])

        # updating route capacity
        self.total_demand += tbic.demand

        # updating total customers count
        self.number_of_customers += 1

    def execute_oropt(self, c10, c11, c20, c21, c30, c31):
        """ Performe a Or-Opt movement and update the customers arival and begin service times """
        # the new route after this move is: 0...c10->c21...c30->c11...c20->c31...0
        
        c10.next_customer = c21
        c21.prev_customer = c10

        c30.next_customer = c11
        c11.prev_customer = c30

        c20.next_customer = c31
        c31.prev_customer = c20

        # update distances for the route and solution
        d = self.instance.dist
        self.total_distance += d(c10, c21) + d(c30, c11) + d(c20,c31) - d(c10, c11) - d(c20, c21) - d(c30, c31)
        self.solution.total_distance = sum([r.total_distance for r in self.solution.routes])

        # update arival and beghin times for the route, after c21 (inclusive)
        self.update_arival_and_begin_times(c=c21)


    def update_arival_and_begin_times(self, c=None):
        if c == None:
            c = self.first_customer.next_customer
        
        while c:
            # update arival time
            c.arival = c.prev_customer.arival + c.prev_customer.waiting_time + c.prev_customer.service_time + self.instance.dist(c.prev_customer, c)
            
            # find the right tw for updating waiting_time
            active_tw = None
            for tw in c.time_windows:
                if c.arival <= tw[1]:
                    active_tw = tw
                    break
            #print('*** c', c.number, c.arival, c.time_windows, active_tw)
            c.waiting_time = max(active_tw[0], c.arival) - c.arival
            
            c = c.next_customer

    def print_route_light(self):
        """Prints the Route"""
        c = self.first_customer
        print('distance: %7.2f\t' % self.total_distance, end='')
        print('demand: %5d\troute: ' % self.total_demand, end='')

        route_text = " "
        while c:
            route_text += "%d (%f)" % (c.number, c.arival)
            c = c.next_customer
            if c:
                route_text += ' - '
        print(route_text)


    def print_route(self):
        """Prints the Route"""
        c = self.first_customer
        print('distance: %7.2f\t' % self.total_distance, end='')
        print('demand: %5d\n*** Route:\n' % self.total_demand, end='')

        route_text = " "
        while c:
            route_text += "\t\tcustomer %3d arival: <%5.2f> tw: <%d,%d> \n" % (c.number, c.arival, c.time_windows[0][0], c.time_windows[0][1])
            c = c.next_customer
            if c:
                route_text += ' - '
        print(route_text)
        