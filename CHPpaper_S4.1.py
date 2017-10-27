# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 11:52:00 2017

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



store_index = 693
p_id = pb.CHPproblem(store_index)

mod = [1,1,1,1]

p_id.hidden_costs = 333000
p_id.putTech(21)
sol = p_id.SimpleOptiControl()
print("BAU:", sum(sol[0]))

h_d = p_id.store.d_gas*0.87*2
h_e = p_id.store.d_ele*2
f1 = plt.figure()
plt.xlabel('HH')
plt.ylabel('Demand, [kWh]')
plt.axis([0, 48*7, 0, 1000])

plt.plot(h_d,  label = 'Electricity')   
plt.plot(h_e,  label = 'heating') 
legend = plt.legend(loc='lower right')








#ax = f.add_subplot(111)
#ax.yaxis.tick_right()
#ax.tick_params(labelleft=True, labelright=True)




#print(problem_id.SimpleOpti5NPV(tech_range = [21], mod = mod, table_string =  'Utility_Prices_Aitor_NoGasCCL', ECA_value = 0.26))
#problem_id.hidden_costs = 400000
#print(problem_id.SimpleOpti5NPV(tech_range = [17], mod = mod))
#print(problem_id.SimpleOpti5NPV(tech_range = [17], mod = mod, table_string =  'Utility_Prices_Aitor_NoGasCCL', ECA_value = 0.26))




##
#f = plt.figure()
#plt.xlabel('years')
#plt.ylabel('Cash flow, [k£]')
#plt.axis([0, 20, -2000, 5000])
#ax = f.add_subplot(111)
#ax.yaxis.tick_right()
#ax.tick_params(labelleft=True, labelright=True)
#
#xs = np.linspace(0,20,num = 21)
#horiz_line_data = np.array([0 for i in range(len(xs))])
#plt.plot(xs, horiz_line_data, 'k--') 
#
#plt.plot(RP_FC,  label = 'Fuel Cell')   
#plt.plot(RP_CHP,  label = 'Combustion Engine')  
#
#legend = plt.legend(loc='lower right')
