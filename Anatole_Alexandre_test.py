# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 16:37:48 2017

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


id_store_min = 500
id_store_max =510

time_start = 806448
time_stop = 824016

Res_cat1 = []

for store_index in range(id_store_min, id_store_max ): 
        
#store_index = 505
        
        goodIO = 0
        cur.execute('''SELECT Ele, Gas FROM Demand_Check Where Stores_id= {vn1}'''.format(vn1 = store_index))
        checkIO = cur.fetchall()
        try:
           if checkIO[0][0] == 1:
               if checkIO[0][1] == 1:
                   goodIO  = 1
        except:
            pass
               
        
        if goodIO == 1:            
            #categorise the store
            cur.execute('''SELECT DNO FROM Stores Where id= {vn1}'''.format(vn1 = store_index))
            DNO = cur.fetchall()[0][0] 
            if DNO < 18:
               category = 1
               
               
               
               
            #get demand    
            cur.execute('''SELECT Gas FROM Demand Where Stores_id= ? AND Time_id > ? AND Time_id < ? ''', (store_index, time_start-1, time_stop))
            Raw_data = cur.fetchall()
            Ele = np.array([elt[0] for elt in Raw_data])
            
            
        if category == 1:
            Res_cat1.append(Ele)

               
            

## calcualte averages across categories
#pd.average(Resutls_ele, )
cat1 = np.array(Res_cat1)
cat1_avg = np.average(cat1, axis = 0)

plt.xlabel('')
plt.ylabel('Ele demand')
plt.axis([0, 100, 0, 200])
plt.plot(Ele, 'ro', label = 'cat1')   



legend = plt.legend(loc='lower left')
            
     