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
p_id = pb.CHPproblem(store_index)


mod = [1,1,1,1]
mod_gas = 1
mod_ele = 1


sol = p_id.SimpleOptiControl(tech_id = 21, mod = mod, table_string =  'Utility_Prices_Aitor_NoGasCCL')
#sol = p_id.SimpleOptiControl(tech_id = 17, mod = mod)#, table_string =  'Utility_Prices_Aitor_NoGasCCL') 
 
part_load = sol[2]
[tech_data, utility_data] = p_id.calculate_data()
[Boiler_eff, a_fuel, b_fuel, a_el, b_el, a_th,  b_th, psi_min, parasitic_load, mant_costs]  = tech_data  
[el_price, el_price_exp, gas_price, th_demand, el_demand] = utility_data


mask000 = part_load > 0.01

el_utilisation = (a_el*part_load+b_el)*mask000
el_tot_utilisation = np.sum(el_utilisation)
fuel_utilisation = (a_fuel*part_load+b_fuel)*mask000 
fuel_tot_utilisation = np.sum(fuel_utilisation)
th_utilisation = np.minimum((a_th*part_load+b_th)*mask000, th_demand)
boilers_topup = th_demand - (a_th*part_load+b_th)*mask000
boilers_topup[boilers_topup<0] = 0
heat_boilers = sum(boilers_topup)
el_exp = el_utilisation - el_demand
el_exp[el_exp<0] = 0
tot_el_exp = sum(el_exp)

th_tot_utilisation = np.sum(th_utilisation)
el_efficiency_tot = el_tot_utilisation/fuel_tot_utilisation 
th_efficiency_tot =th_tot_utilisation/fuel_tot_utilisation
CHPQI = el_efficiency_tot*238+th_efficiency_tot*120


heat_gen = sum((a_th*part_load+b_th)*mask000)



print("heat generated:", heat_gen)
print("heat utilised:", sum(th_utilisation))
print("heat boilers:", heat_boilers)
print("gas consumption:", sum(fuel_utilisation))
print("gas boilers:", heat_boilers/0.87)
print("el generation:", sum(el_utilisation))
print("el generation:", sum(el_utilisation) - tot_el_exp)
print("el export:", tot_el_exp)
print("mant cost £:", sum(el_utilisation)*mant_costs)
print("savings £:", sum(sol[0])-sum(sol[1]))
np.average(p_id.store.p_gas)

#sol = problem_id.SimpleOptiControl(tech_id = 17, mod = mod)#, table_string =  'Utility_Prices_Aitor_NoGasCCL')
