# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 17:59:34 2017

@author: nl211
"""

import sqlite3
import numpy as np
import math



sqlite3.register_adapter(np.float64, float)
sqlite3.register_adapter(np.float32, float)
sqlite3.register_adapter(np.int64, int)
sqlite3.register_adapter(np.int32, int)    

conn = sqlite3.connect('D:\\Database_SSL\\Code\\Sainsburys.sqlite')
cur = conn.cursor()


cur.executescript('''
DROP TABLE IF EXISTS Utility_Prices_Aitor;

        
 CREATE TABLE Utility_Prices_Aitor (
     id     INTEGER NOT NULL,
     DNO INTEGER,
     Voltage INTEGER,
     Ele  FLOAT,
     Gas FLOAT,
     Ele_exp FLOAT,
     PRIMARY KEY(id,DNO,Voltage),
     FOREIGN KEY(id) REFERENCES Time(id)
     
 )


''')

year_start = 2015
year_stop = 2017


for DNO in range(1,15):
    for Voltage in range(3):
        
        print("currently producing prices for (DNO, Voltage):", DNO,Voltage)
        cur.execute('''SELECT * FROM Time WHERE year BETWEEN {year_start} AND {year_stop}'''.format(year_start= year_start, year_stop = year_stop))  
        fetch = cur.fetchall()
        time_id = tuple([elt[0] for elt in fetch])
        year_id = tuple([elt[2] for elt in fetch])
        Month_id = tuple([elt[3] for elt in fetch])
        Day_id = tuple([elt[4] for elt in fetch])
        HH_id = tuple([elt[5] for elt in fetch])
        DayType_id = tuple([elt[6] for elt in fetch])
        
        for count in range(len(time_id)):
            time_count = time_id[count]
            year = year_id[count]
            Month = Month_id[count]
            Day = Day_id[count]
            HH = HH_id[count]   
            DayType = DayType_id[count]
        
        
        
            cur.execute('''SELECT Ele FROM Tariffs_HH WHERE id = {time}'''.format(time=time_count)) 
            try:
                comm = cur.fetchone()[0]/10
            except:
                comm = float("NaN")
            cur.execute('''SELECT BSUos FROM Tariffs_HH WHERE id = {time}'''.format(time=time_count)) 
            try:
                BSUos = cur.fetchone()[0]/10
            except:
                BSUos = float("NaN")
            cur.execute('''SELECT TLM FROM Tariffs_HH WHERE id = {time}'''.format(time=time_count)) 
            try:
                TLM= cur.fetchone()[0]
            except:
                TLM = float("NaN")          
        
        
            ## TNUos
            Days_NovFeb = 120
            daysperWeek = 5.0/7
            Triad_hours = 1.5
            prob = np.zeros((12,48))
            prob[0][34]=3.20; prob[0][35]= 0.53; prob[0][36]= 0.27; prob[1][34]= 1.92; prob[1][35]= 0.32; prob[1][36]= 0.16; prob[10][34]= 1.92; prob[10][35]= 0.32; prob[10][36]= 0.16; prob[11][34]= 2.56; prob[11][35]= 0.43; prob[11][36]= 0.21
            cur.execute('''SELECT TNUos FROM DNO_Tariffs WHERE DNO ={dno} AND year={year} AND Month = {Month} AND DayType = {Daytype} AND HH={HH} AND Voltage={Voltage}'''.format(dno = DNO, Daytype = DayType, HH=HH, Voltage=Voltage, year= year, Month=Month))  
            TNUosRaw = cur.fetchone()
            TNUos = TNUosRaw [0]/Days_NovFeb/daysperWeek/Triad_hours*100 
            TNUos = TNUos*prob[Month][HH-1] 
            
            
            
            ## DUOs capacity
            ## its is based on the connection not on the usage, therefrore we shuldnt consider it in our model!
            Utilisation_factor = 3735
            cur.execute('''SELECT DUos_cap FROM DNO_Tariffs WHERE DNO ={dno} AND year={year} AND Month = {Month}  AND DayType = {Daytype} AND HH={HH} AND Voltage={Voltage}'''.format(dno = DNO, Daytype = DayType, HH=HH, Voltage=Voltage, year= year, Month=Month)) 
            DUOs_capRaw  = cur.fetchone()
            DUOs_cap = DUOs_capRaw[0]*365/Utilisation_factor 
            
            
            ## DUOs commodity
            cur.execute('''SELECT DUos_com FROM DNO_Tariffs WHERE DNO ={dno} AND year={year} AND Month = {Month}  AND DayType = {Daytype} AND HH={HH} AND Voltage={Voltage}'''.format(dno = DNO, Daytype = DayType, HH=HH, Voltage=Voltage, year= year, Month=Month))  
            DUOs_comRaw  = cur.fetchone()
            DUOs_com = DUOs_comRaw[0]
            
            
            ## Constant Tariffs
            cur.execute('''SELECT OR_tariff, CCL, FiT, AAHEDC, CfD, CM, Man_fee FROM DNO_Tariffs WHERE DNO ={dno} AND year={year} AND Month = {Month}  AND DayType = {Daytype} AND HH={HH} AND Voltage={Voltage}'''.format(dno = DNO, Daytype = DayType, HH=HH, Voltage=Voltage, year= year, Month=Month)) 
            ConstantRaw  = cur.fetchone()
            OR_tariff = ConstantRaw [0]
            CCL = ConstantRaw[1]
            FiT = ConstantRaw[2]
            AAHEDC = ConstantRaw[3]
            CfD = ConstantRaw[4]
            CM = ConstantRaw[5]
            Man_fee = ConstantRaw[6]
            
            
            ## LLF
            cur.execute('''SELECT LLF FROM DNO_Tariffs WHERE DNO ={dno} AND year={year} AND Month = {Month}  AND DayType = {Daytype} AND HH={HH} AND Voltage={Voltage}'''.format(dno = DNO, Daytype = DayType, HH=HH, Voltage=Voltage, year= year, Month=Month))  
            LLFRaw  = cur.fetchone()
            LLF = LLFRaw[0]
            
            
            
            cur.execute('''SELECT Gas, CCL_Gas FROM DNO_Tariffs WHERE DNO ={dno} AND year={year} AND Month = {Month}  AND DayType = {Daytype} AND HH={HH} AND Voltage={Voltage}'''.format(dno = DNO, Daytype = DayType, HH=HH, Voltage=Voltage, year= year, Month=Month)) 
            ConstantRaw  = cur.fetchone()
            Gas = ConstantRaw [0]
            Gas_CCL = ConstantRaw[1]
            
            final_ele = comm*LLF*TLM + BSUos*LLF*TLM + TNUos*LLF + DUOs_com + DUOs_cap + OR_tariff + CCL + AAHEDC + CfD + CM +  Man_fee
            final_ele_exp = final_ele*2/5
            final_gas = Gas + Gas_CCL
            
            if not math.isnan(final_ele):
                cur.execute('''INSERT INTO Utility_Prices_Aitor(id, DNO, Voltage, Ele, Gas, Ele_exp) VALUES({time_id}, {dno},{Voltage},{Value},{Value_Gas},{Value_exp})'''.format(time_id = time_count, dno = DNO, Voltage = Voltage, Value = final_ele, Value_Gas = final_gas, Value_exp = final_ele_exp))   
            



    conn.commit() 
    
