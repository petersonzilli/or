# -*- coding: utf-8 -*-
"""
Readers for VRPMTW instances
Author: Peterson Katagiri Zilli <peterson.zilli@gmail.com>
Date: 2018-01-25

Important Notes:
- Customer numbers start with 0 (the depot) and must be sequential, in sorted order
"""
import re

class Reader:
    """Reader Class for VRPMTW instances"""
    def __init__(self, filename=None):
        self.filename = filename

    def load(self):
        """Returns instance name, vehicle_number, capacity
        and customers details"""
        with open(self.filename, 'r') as fp:
            # reading instance name
            instance_name = fp.readline().strip()

            # skipping next 3 lines
            for _ in range(3):
                fp.readline()

            # reading number of vehicles and capacity
            aux = fp.readline()
            aux = re.sub(' +', ' ', aux).strip()
            aux = aux.split(' ')
            aux = list(map(int, aux))
            number_vehicles, capacity = aux

            # skipping next 4 lines
            for _ in range(4):
                fp.readline()
            
            # reading customers list.
            # if there is not 7 columns, skips the line
            customers = []
            for line in fp:
                aux = re.sub(' +', ' ', line).strip()
                aux = aux.split()
                if len(aux) != 7:
                    continue
                aux = list(map(int, aux))
                customers.append(aux)
                aux = None

            return instance_name, number_vehicles, capacity, customers
