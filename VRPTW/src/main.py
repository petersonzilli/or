#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main script for VRPTW
Author: Peterson Katagiri Zilli <peterson.zilli@gmail.com>
Date: 2018-01-25
"""

from instance import Instance
from customer import Customer
from route import Route
from solution import Solution
from construction_simple_1 import ConstructionSimple
import os


if __name__ == '__main__':

    print('Instance name,number of vehicles,capacity of vehicles,solution routes,solution distance')
    dir_path = r'..\data\solomon_100'
    for instance in os.listdir(dir_path):
        
        inst = Instance(os.path.join(dir_path,instance))
        
        construct = ConstructionSimple(inst)
        solution = construct.complete_solution()

        print(inst.name,end=',')
        print(inst.number_vehicles,end=',')
        print(inst.capacity,end=',')
        print(len([r for r in solution.routes if r.total_demand > 0]),end=',')
        print('%5.1f' % solution.total_distance)

        #solution.print_solution()
