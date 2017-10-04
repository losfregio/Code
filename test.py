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


conn = sqlite3.connect('.\\Sainsburys.sqlite')
cur = conn.cursor()   



store_index = 723
problem_id = pb.CHPproblem(store_index)



sol = problem_id.SimpleOpti5NPV()
print(sol)
