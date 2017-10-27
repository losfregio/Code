# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:58:31 2017

@author: nl211
"""

import sqlite3
import Common.classStore as st
import Common.classTech as tc
import Solvers.classCHPProblem as pb
import numpy as np
import matplotlib.pyplot as plt

#
conn = sqlite3.connect('D:\\Database_SSL\\Code\\Sainsburys.sqlite')
cur = conn.cursor()   



store_index = 2010
p_id = pb.CHPproblem(store_index)

sol = p_id.SimpleOpti5NPV()
print(sol[1])
print(sol[8])