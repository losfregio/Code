# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 15:33:00 2017

@author: nl211
"""


import sqlite3
import Common.classStore as st
import Common.classTech as tc
import Solvers.classCHPProblem as pb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


database_path = ".\\Sainsburys.sqlite"
conn = sqlite3.connect(database_path)
cur = conn.cursor()



id_store = 693
pb_id = pb.CHPproblem(id_store)


solution = pb_id.SimpleOptiControl(tech_id = 15)
print("BAU:", sum(solution[0]))
print("OPEX:", sum(solution[1]))
#
#solution = pb_id.SimpleOpti5NPV()
#print(solution[1])
#print(solution[8])