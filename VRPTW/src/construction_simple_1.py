# -*- coding: utf-8 -*-
"""
Complete a full solution for VRPTW given a partial solution 
Author: Peterson Katagiri Zilli <peterson.zilli@gmail.com>
Date: 2018-01-25

Important Notes:
- Time Windows are sorted while reading the instance. it is important for simple construction algorithm

"""
from solution import Solution
import random
import sys

class ConstructionSimple:
    """Instance Class for VRPTW"""
    def __init__(self, instance, solution=None):
        self.instance = instance
        if not solution:
            solution = Solution(self.instance)
        self.solution = solution

        # preprocessing instance for the algo
        for c in self.instance.customers:
            c.time_windows = sorted(c.time_windows)

    def complete_solution(self, random_seed=0):
        """
        Builds a solution loosely based on Solomon (1987) and Russell (1995) sequential construction heuristics
        """

        #print('Phase 1: determining seed customers between the not used customers')
        random.seed(random_seed)
        seed_customers = [c.number for c in self.instance.customers if c.route == None]
        random.shuffle(seed_customers)
        #print(seed_customers)

        #print('Phase 2: inserting each customer to the route which yields the least incurred cost')
        
        """
            The algorithm is simple:

            for the next customer of seed_customers - ordered and not already used
                for each route:
                    for each one of the possible positions in the route:
                        calculate the aditional cost of adding the customer 'c'
                        if it is better than the best, update the best
            perform the best insertion (and update route and solution costs)
            remove the best insertion customer from the seed customers
        """
        while len(seed_customers) > 0:
            # reset best move
            best_insertion_cost = sys.float_info.max
            best_insertion_customer = None
            best_insertion_previous_customer = None
        
            c = seed_customers[0]
            tbic = self.instance.customers[c]

            for r in self.solution.routes:
                previous_customer = r.first_customer

                # verify if capacity constraint is ok
                if not self.verify_constraint_demand(tbic, r):
                    continue

                while previous_customer.next_customer != None:
                    pc = previous_customer
                    nc = pc.next_customer

                    delta_cost = self.instance.dist(pc, tbic) + self.instance.dist(tbic, nc) - self.instance.dist(pc, nc)
                    
                    if delta_cost < best_insertion_cost and self.verify_constraint_tw(tbic, pc):
                        best_insertion_cost = delta_cost
                        best_insertion_customer = tbic
                        best_insertion_previous_customer = pc
                    previous_customer = nc
            
            #print('best_insertion cost:          ', best_insertion_cost)
            #print('best_insertion customer:      ', best_insertion_customer.number)
            #print('best_insertion prev customer: ', best_insertion_previous_customer.number)
            #print('best_insertion route:         ', best_insertion_previous_customer.route)
            
            best_insertion_previous_customer.route.insert(best_insertion_customer, best_insertion_previous_customer)        
            seed_customers.remove(best_insertion_customer.number)
            #self.solution.print_solution()
            #input('waiting...')
        return self.solution


    def verify_constraint_demand(self, tbic, r):
        """Verify demand constraints for the route"""
        return self.instance.capacity >= r.total_demand + tbic.demand

    def verify_constraint_tw(self, tbic, pc):
        """ Verify arival and waiting time from the inserted cutomer to the end"""

        # verify tw constraints on tbic
        aux_arival = pc.arival + pc.waiting_time + pc.service_time + self.instance.dist(pc, tbic)
        active_tw = None
        for tw in list(tbic.time_windows):
            if aux_arival <= tw[1]:
                active_tw = tuple(tw)
                break
        # if there is no active tw then it is a infeasible insertion  
        if not active_tw:
            return False
        aux_waiting_time = max(active_tw[0], aux_arival) - aux_arival
    
        # verify tw constraints on pc.next "[...] and beyond!" - Buzz Lightyer
        c = pc.next_customer
        pc = tbic

        while c:
            aux_arival = aux_arival + aux_waiting_time + pc.service_time + self.instance.dist(pc, c)
            active_tw = None
            for tw in c.time_windows:
                if aux_arival <= tw[1]:
                    active_tw = tuple(tw)
                    break
            # if there is no active tw then it is a infeasible insertion  
            if not active_tw:
                return False
            aux_waiting_time = max(active_tw[0], aux_arival) - aux_arival
            
            # update customer to be tested
            pc = c
            c = pc.next_customer
        
        return True
