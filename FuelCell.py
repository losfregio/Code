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

mod = [1,1,1,1]
id_store_min =500
id_store_max = 1000#785

tech_range = range(1,21)

RP_FC = np.array([])
RP_FC_cash = np.array([])
RP_CHP = np.array([])
RP_CHP_cash = np.array([])
RP_store = np.array([])
RP_CHPQI = np.array([])
RP_CHP_G = np.array([])
RP_case = np.array([])
count_case = 1

for store_index in range(id_store_min, id_store_max ): 
        
        
        goodIO = 0
        cur.execute('''SELECT Ele, Gas FROM Demand_Check Where Stores_id= {vn1}'''.format(vn1 = store_index))
        checkIO = cur.fetchall()
        try:
           if checkIO[0][0] == 1:
               if checkIO[0][1] == 1:
                   goodIO  = 1
        except:
            pass
               
        
        id_tech_opti = -1
        if goodIO == 1:
            problem_id = pb.CHPproblem(store_index)
            problem_id.hidden_costs = 330000
            results = problem_id.SimpleOpti5NPV(method = 1, tech_range = [21], mod = [1,1,1,1], table_string = 'Utility_Prices_Aitor_NoGasCCL', ECA_value = 0.26)
            problem_id.hidden_costs = 400000
            results2 = problem_id.SimpleOpti5NPV(method = 1, tech_range = [17], mod =  mod)
            CHPQI = results2[2]
            if CHPQI > 109.5:
                results2 = problem_id.SimpleOpti5NPV(method = 1, tech_range = [17], table_string = 'Utility_Prices_Aitor_NoGasCCL',  ECA_value = 0.26, mod =  mod)
            
#            diff = results[3] - results2[3]
            
#            id_tech_opti = results[0]
#            id_tech_opti_name = results[1]
#            savings = results[2]
            print("store number:", store_index)
#            print(results[3])
#            print(results2[3])
#            print(diff)
            if results[5] < 10:
                RP_case = np.append(RP_case,store_index)
                RP_FC  = np.append(RP_FC, results[5])
                #RP_FC_cash  = np.append(RP_FC_cash, results[5])
                if CHPQI > 109.5:
                    RP_CHP_G = np.append(RP_CHP_G, results2[5])
                    RP_CHP  = np.append(RP_CHP,[np.nan])
                else:
                    RP_CHP  = np.append(RP_CHP, results2[5])
                    RP_CHP_G = np.append(RP_CHP_G, [np.nan])
                #RP_CHP_cash  = np.append(RP_CHP_cash, results2[5])    
                RP_store = np.append(RP_store, store_index)
                RP_CHPQI = np.append(RP_CHPQI, CHPQI)
                count_case = count_case + 1



plt.xlabel('Case #')
plt.ylabel('Payback Time, [years]')
plt.axis([500, 800, 0, 10])
plt.plot(RP_case, RP_FC, 'ro', label = 'Fuel Cell (good CHPQI)')   
plt.plot(RP_case, RP_CHP, 'bo' , label = 'CHP bad CHPQI') 
plt.plot(RP_case, RP_CHP_G, 'go' , label = 'CHP good CHPQI') 

legend = plt.legend(loc='lower left')

#plt.xlabel('Case #')
#plt.ylabel('Cumulative Discounted Cash Flow, [£]')
#plt.axis([500, 800, -300000, 500000])
#plt.plot(RP_case,  RP_FC_cash, 'ro', label = 'Fuel Cell: discounted CCF')   
#plt.plot(RP_case,  RP_CHP_cash, 'bo' , label = 'CHP: discounted CCF') 


legend = plt.legend(loc='lower left')