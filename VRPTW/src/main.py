#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main script for VRPMTW - Vehicle Routing Problem with Multiple Time Windows
Author: Peterson Katagiri Zilli <peterson.zilli@gmail.com>
Date: 2018-01-25
"""

from instance import Instance
from customer import Customer
from route import Route
from solution import Solution
from construction_simple_1 import ConstructionSimple1
from construction_simple_2 import ConstructionSimple2
from localsearch_oropt import OrOpt
import os
import sys


if __name__ == '__main__':

    print('Instance name,number of vehicles,capacity of vehicles,solution routes,solution distance before or-opt,solution distance after or-opt')
    dir_path = r'..\data\solomon_25'
    for instance in os.listdir(dir_path):
        #instance = 'r101.txt'
        inst = Instance(os.path.join(dir_path,instance))
        
        construct = ConstructionSimple2(inst)
        solution = construct.complete_solution()

        print(inst.name,end=',')
        print(inst.number_vehicles,end=',')
        print(inst.capacity,end=',')
        print(len([r for r in solution.routes if r.total_demand > 0]),end=',')
        print('%5.1f' % solution.total_distance,end=',')

        ls = OrOpt(inst, solution)
        for route in solution.routes:
            if route.number_of_customers < 1:
                continue
            ls.apply_ls(route, 3)

        print('%5.1f' % solution.total_distance)
