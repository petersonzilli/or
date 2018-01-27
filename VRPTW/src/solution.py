# -*- coding: utf-8 -*-
"""
Solution Representation for VRPMTW
Author: Peterson Katagiri Zilli <peterson.zilli@gmail.com>
Date: 2018-01-25
"""

from route import Route

class Solution:
    """Instance Class for VRPMTW"""
    def __init__(self, instance, routes=None):
        self.instance = instance
        if not routes:
            routes = tuple([Route(self.instance, self) for r in range(self.instance.number_vehicles)])
        self.routes = routes
        self.total_distance = sum([r.total_distance for r in routes])
        
        # Marks customer 0 as 'already used' (once copies of it are already in all routes)
        self.instance.customers[0].route = -1   

    def print_solution(self):
        """Prints the solution"""
        print('Solution for Instance name: ', self.instance.name)
        print('Total Distance:', self.total_distance)
        print('Routes:')
        for index in range(len(self.routes)):
            if self.routes[index].total_demand > 0:
                print('(R%3d) \t' % (index+1) ,end='')
                self.routes[index].print_route_light()