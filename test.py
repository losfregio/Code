# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 10:50:55 2017

@author: nl211
"""

import sqlite3
import Common.classStore as st
import Solvers.classCHPProblem as pb
import numpy as np
import matplotlib.pyplot as plt


store_index = 693
problem_id = pb.CHPproblem(store_index)

mod = [1,2,1,1]

sol = problem_id.SimpleOptiControl(tech_id = 15, mod = mod)

op_cost = sum(sol[0])
op_cost_new = sum(sol[1])
print(op_cost)
print(op_cost_new)

print(sol[5])
print(sum(sol[4]))

##new line test github