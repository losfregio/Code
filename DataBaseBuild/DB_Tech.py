# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 18:50:26 2017

@author: nl211
"""



import sqlite3
import pandas as pd
import numpy as np


sqlite3.register_adapter(np.float64, float)
sqlite3.register_adapter(np.float32, float)
sqlite3.register_adapter(np.int64, int)
sqlite3.register_adapter(np.int32, int)    

conn = sqlite3.connect('D:\\Database_SSL\\Code\\Sainsburys.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Technologies;

CREATE TABLE Technologies (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT,
    price INTEGER NOT NULL, 
    a_fuel INTEGER NOT NULL, 
    b_fuel INTEGER NOT NULL, 
    a_ele INTEGER NOT NULL,
    b_ele INTEGER NOT NULL,
    a_th INTEGER NOT NULL,
    b_th INTEGER NOT NULL,
    psi_min INTEGER NOT NULL,
    parasitic_load INTEGER NOT NULL,
    mant_costs INTEGER NOT NULL
)

''')


bla1 = pd.read_csv('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Tech.csv''')
bla = bla1.iloc[0::,:]
for entry in range(len(bla)) :    
     entry_name  = bla.iloc[entry][0]; 
     entry_price = bla.iloc[entry][1];
     entry_a_fuel  = bla.iloc[entry][2];
     entry_b_fuel  = bla.iloc[entry][3];
     entry_a_ele  = bla.iloc[entry][4];
     entry_b_ele  = bla.iloc[entry][5];
     entry_a_th  = bla.iloc[entry][6];
     entry_b_th  = bla.iloc[entry][7];
     entry_psi_min  = bla.iloc[entry][8];
     entry_parasitic_load  = bla.iloc[entry][9];
     ## These have changed with respect to the previous version of the model. now the mantiancne costs is applied as a tax of 0.02/kWh on the gas.
     entry_mant_costs  = bla.iloc[entry][10];
     #print entry_id
     cur.execute('''INSERT OR IGNORE INTO Technologies (name, price, a_fuel, b_fuel, a_ele, b_ele, a_th, b_th, psi_min, parasitic_load,mant_costs) 
         VALUES ( ?,?,?,?,?,?,?,?,?,?,? )''', (entry_name, entry_price, entry_a_fuel, entry_b_fuel, entry_a_ele, entry_b_ele, entry_a_th, entry_b_th, entry_psi_min, entry_parasitic_load,entry_mant_costs ) )   
conn.commit()    
     
