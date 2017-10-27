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



RP_FC = np.array([])
RP_CHP = np.array([])


store_index = 693
problem_id = pb.CHPproblem(store_index)


mod = [1,1,1,1]
mod_gas = 1
mod_ele = 1

discount_rate = 0.0

cash_flow = -1170
RP_FC  = np.append(RP_FC, cash_flow) 
ncount = 0
for year_item in range(0,20):
    sol = problem_id.SimpleOptiControl(tech_id = 21, mod = mod, table_string =  'Utility_Prices_Aitor_NoGasCCL')
    opex_savings = (sum(sol[0])-sum(sol[1]))/((1+discount_rate )**(year_item+1))
    print(opex_savings)
    cash_flow = cash_flow +  opex_savings/1000
    RP_FC  = np.append(RP_FC, cash_flow)
    mod_gas = mod_gas*1.02
    mod_ele = mod_ele*1.04
    if year_item == 10:
        ncount = 0
    mod_fuel = (1+0.009)**ncount
    mod = [mod_ele, mod_gas, mod_fuel, 1]
    ncount = ncount + 1

print("CHP")
mod = [1,1,1,1]
mod_gas = 1
mod_ele = 1
mod_fuel = 1
ncount = 0

cash_flow = -820
RP_CHP  = np.append(RP_CHP, cash_flow) 
for year_item in range(0,20):
    sol = problem_id.SimpleOptiControl(tech_id = 17, mod = mod)#, table_string =  'Utility_Prices_Aitor_NoGasCCL')
    opex_savings = (sum(sol[0])-sum(sol[1]))/((1+discount_rate )**(year_item+1))
    print(opex_savings)
    cash_flow = cash_flow +  opex_savings/1000
    RP_CHP  = np.append(RP_CHP, cash_flow)
    mod_gas = mod_gas*1.02
    mod_ele = mod_ele*1.04
    if year_item == 10:
        ncount = 0
    mod_fuel = (1+0.009)**ncount
    mod = [mod_ele, mod_gas, mod_fuel, 1]
    ncount = ncount + 1
    
mod = [1,1,1,1]
#problem_id.hidden_costs = 333000
#print(problem_id.SimpleOpti5NPV(tech_range = [21], mod = mod, table_string =  'Utility_Prices_Aitor_NoGasCCL', ECA_value = 0.26))
#problem_id.hidden_costs = 400000
#print(problem_id.SimpleOpti5NPV(tech_range = [17], mod = mod))
#print(problem_id.SimpleOpti5NPV(tech_range = [17], mod = mod, table_string =  'Utility_Prices_Aitor_NoGasCCL', ECA_value = 0.26))

#
f = plt.figure()
plt.xlabel('years')
plt.ylabel('Cash flow, [k£]')
plt.axis([0, 20, -2000, 5000])
ax = f.add_subplot(111)
ax.yaxis.tick_right()
ax.tick_params(labelleft=True, labelright=True)

xs = np.linspace(0,20,num = 21)
horiz_line_data = np.array([0 for i in range(len(xs))])
plt.plot(xs, horiz_line_data, 'k--') 

plt.plot(RP_FC,  label = 'Fuel Cell')   
plt.plot(RP_CHP,  label = 'Combustion Engine')  

legend = plt.legend(loc='lower right')

#
#plt.xlabel('Case #')
#plt.ylabel('Cumulative Discounted Cash Flow, [£]')
#plt.axis([500, 800, -300000, 500000])
#plt.plot(RP_case,  RP_FC_cash, 'ro', label = 'Fuel Cell: discounted CCF')   
#plt.plot(RP_case,  RP_CHP_cash, 'bo' , label = 'CHP: discounted CCF') 
#
#
#legend = plt.legend(loc='lower left')