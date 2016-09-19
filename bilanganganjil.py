# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 01:58:46 2016

@author: febi
"""
import math

row = 25
i = row
    
while(i>=0):
    if i != row // 2:
        print(" " * ((row-( int( math.sqrt(( row - (row-i)*2 ) ** 2))))//2) +  "*" * ( int( math.sqrt(( row - (row-i)*2 ) ** 2))) + " " * ((row-( int( math.sqrt(( row - (row-i)*2 ) ** 2))))//2) )
    i=i-1