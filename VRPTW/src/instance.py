# -*- coding: utf-8 -*-
"""
Instance Representation for VRPMTW
Author: Peterson Katagiri Zilli <peterson.zilli@gmail.com>
Date: 2018-01-25
"""
from math import sqrt
from reader import Reader
from customer import Customer

class Instance:
    """Instance Class for VRPMTW"""
    def __init__(self, file_name=None):
        self.file_name = file_name

        self.reader = Reader(self.file_name)
        self.name, self.number_vehicles, self.capacity, _customers = self.reader.load()
        _customers = [Customer(info) for info in _customers]
        self.customers = tuple(_customers)

    def dist(self, c1, c2):
        """Returns the distance between 2 customers"""
        return sqrt( (c2.xcoord - c1.xcoord)**2 + (c2.ycoord - c1.ycoord)**2 )
        
