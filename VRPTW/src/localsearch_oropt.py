# -*- coding: utf-8 -*-
"""
Or Opt neighbourhood local search for VRPMTW given route 
Author: Peterson Katagiri Zilli <peterson.zilli@gmail.com>
Date: 2018-01-27

Important Notes:
- Time Windows are sorted while reading the instance. it is important for this localsearch algorithm

"""

import sys

class OrOpt:
    """Or-OPT neighbourhood local search Class for VRPMTW"""
    def __init__(self, instance, solution):
        self.instance = instance
        self.solution = solution

    def eval_delta_dist(self, route, c10, c11, c20, c21, c30, c31):
        """ Evaluate delta distance for an Or-OPT movement """
        d = self.instance.dist
        return d(c10, c21) + d(c30, c11) + d(c20,c31) - d(c10, c11) - d(c20, c21) - d(c30, c31)

    def verify_constraint_tw(self, route, c10, c11, c20, c21, c30, c31):
        """ Verify arival and waiting time from the Or-OPT movement"""

        # the new route after this move is: 0...c10->c21...c30->c11...c20->c31...0

        # verify tw constraints on c21
        aux_arival = c10.arival + c10.waiting_time + c10.service_time + self.instance.dist(c10, c21)
        active_tw = None
        for tw in list(c21.time_windows):
            if aux_arival <= tw[1]:
                active_tw = tuple(tw)
                break
        # if there is no active tw then it is a infeasible insertion  
        if not active_tw:
            return False
        aux_waiting_time = max(active_tw[0], aux_arival) - aux_arival

        # verify tw constraints on the route c21 to c30
        c = c21
        while(c != c30):
            pc = c
            c = c.next_customer
            aux_arival = aux_arival + aux_waiting_time + pc.service_time + self.instance.dist(pc, c)
            active_tw = None
            for tw in list(c.time_windows):
                if aux_arival <= tw[1]:
                    active_tw = tuple(tw)
                    break
            # if there is no active tw then it is a infeasible insertion  
            if not active_tw:
                return False
            aux_waiting_time = max(active_tw[0], aux_arival) - aux_arival

        # the new route after this move is: 0...c10->c21...c30->c11...c20->c31...0
        
        #   0 | 1 | 2 | 3 - 4 - 5 - 6 - 0
        #  c10 c11 c30 c31
        #      c20 c21

        # verify tw constraints on c11
        aux_arival = aux_arival + aux_waiting_time + c30.service_time + self.instance.dist(c30, c11)
        active_tw = None
        for tw in list(c11.time_windows):
            if aux_arival <= tw[1]:
                active_tw = tuple(tw)
                break
        # if there is no active tw then it is a infeasible insertion  
        if not active_tw:
            return False
        aux_waiting_time = max(active_tw[0], aux_arival) - aux_arival

        # verify tw constraints on the route c11 to c20
        c = c11
        while(c != c20):
            pc = c
            c = c.next_customer
            aux_arival = aux_arival + aux_waiting_time + pc.service_time + self.instance.dist(pc, c)
            active_tw = None
            for tw in list(c.time_windows):
                if aux_arival <= tw[1]:
                    active_tw = tuple(tw)
                    break
            # if there is no active tw then it is a infeasible insertion  
            if not active_tw:
                return False
            aux_waiting_time = max(active_tw[0], aux_arival) - aux_arival

        # the new route after this move is: 0...c10->c21...c30->c11...c20->c31...0

        # verify tw constraints on c31
        aux_arival = aux_arival + aux_waiting_time + c20.service_time + self.instance.dist(c20, c31)
        active_tw = None
        for tw in list(c31.time_windows):
            if aux_arival <= tw[1]:
                active_tw = tuple(tw)
                break
        # if there is no active tw then it is a infeasible insertion  
        if not active_tw:
            return False
        aux_waiting_time = max(active_tw[0], aux_arival) - aux_arival

        # verify tw constraints on the route c31 to the end
        c = c31
        while(c != route.last_customer):
            pc = c
            c = c.next_customer
            aux_arival = aux_arival + aux_waiting_time + pc.service_time + self.instance.dist(pc, c)
            active_tw = None
            for tw in list(c.time_windows):
                if aux_arival <= tw[1]:
                    active_tw = tuple(tw)
                    break
            # if there is no active tw then it is a infeasible insertion  
            if not active_tw:
                return False
            aux_waiting_time = max(active_tw[0], aux_arival) - aux_arival

        return True

    def apply_ls(self, route, k=3):
        """
        Apply Or Opt local search
        """

        """
            The algorithm is simple:

            for each group of 1 to k customers in the route:
                take the group of customers out of the route 
                evaluate the cost of reinserting them back in a later position into the route
                if the best cost for reinsertion is negative, reinsert them into the best cost
                else, stop the algorithm
        """


        #   0 | 1 | 2 | 3 - 4 - 5 - 6 - 0
        #  c10 c11 c30 c31
        #      c20 c21
        #   delta = d(c10, c21) + d(c30, c11) + d(c20,c31) - d(c10, c11) - d(c20, c21) - d(c30, c31) 

        if route.number_of_customers < 2:
            return

        best_move_cost = -1
        while best_move_cost < 0:
            best_move_cost = sys.float_info.max
            best_move_c10 = None
            best_move_c20 = None
            best_move_c30 = None

            c10 = route.first_customer

            limit_c30 = route.last_customer         # customer 0 (last) on the example
            limit_c20 = limit_c30.prev_customer     # customer 6 on the example
            limit_c10 = limit_c20.prev_customer     # customer 5 on the example
        
            while c10 != limit_c10:
                c11 = c10.next_customer
                c20 = c11
                counter = k
                while counter > 0 and c20 != limit_c20:
                    counter -= 1
                    c21 = c20.next_customer
                    c30 = c21
                    while c30 != limit_c30:
                        c31 = c30.next_customer
                        #print('c10', c10.number,'c11', c11.number,'c20', c20.number,'c21', c21.number, 'c30', c30.number, 'c31', c31.number)
                        aux_delta_dist = self.eval_delta_dist(route, c10, c11, c20, c21, c30, c31)
                        #print(aux_delta_dist, c10.number, c11.number, c20.number, c21.number, c30.number, c31.number)
                        if aux_delta_dist < -0.000000001 and aux_delta_dist < best_move_cost:
                            if self.verify_constraint_tw(route, c10, c11, c20, c21, c30, c31):
                                best_move_cost = aux_delta_dist
                                best_move_c10 = c10
                                best_move_c20 = c20
                                best_move_c30 = c30
                            #    print('tw ok')
                            #else:
                            #    print('tw problem')
                        c30 = c31
                    c20 = c21
                c10 = c11
            #print('*** best move cost', best_move_cost)
            if best_move_cost < 0:
                #print ('*** Best Move', best_move_cost, best_move_c10.number, best_move_c20.number, best_move_c30.number)
                #print('*** Route %s' % route)
                #route.print_route_light()
                route.execute_oropt(best_move_c10, best_move_c10.next_customer,
                                best_move_c20, best_move_c20.next_customer,
                                best_move_c30, best_move_c30.next_customer)
                #route.print_route_light()