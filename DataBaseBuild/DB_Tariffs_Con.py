# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 19:19:46 2017

@author: nl211
"""


import sqlite3
import pandas as pd
import numpy as np
import itertools as it

sqlite3.register_adapter(np.float64, float)
sqlite3.register_adapter(np.float32, float)
sqlite3.register_adapter(np.int64, int)
sqlite3.register_adapter(np.int32, int)    

conn = sqlite3.connect('D:\\Database_SSL\\Code\\Sainsburys.sqlite')
cur = conn.cursor()

# Values provided by Saisnburys.... USELESS
#Triad_intensity = 0.54 #kW triad/kVA
#Triad_Utilisation_factor = 4730 #kWh/year/kVA

cur.executescript('''
DROP TABLE IF EXISTS DNO_Tariffs;


CREATE TABLE DNO_Tariffs (
    DNO     INTEGER NOT NULL,
    year   INTEGER  NOT NULL,
    Month INTEGER NOT NULL,
    DayType INTEGER  NOT NULL,
    HH    INTEGER  NOT NULL,
    Voltage STRING,
    TNUos FLOAT,
    DUOs_cap FLOAT,
    DUOs_com FLOAT,
    OR_tariff FLOAT,
    CCL FLOAT,
    FiT FLOAT,
    AAHEDC FLOAT,
    CfD FLOAT,
    CM FLOAT,
    Man_fee FLOAT,
    LLF,
    Gas,
    CCL_Gas,
    PRIMARY KEY (DNO,year, Month, DayType,HH,Voltage) 
)


''')



# TNUos
print('load TNUos:')
df = pd.read_excel('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Utility\\TNUos.xlsx''')

count=0
for item in range(len(df)) :            
            year = df.iloc[item][0]
            Region = df.iloc[item][1]
            item_value  = df.iloc[item][2]; 
            
            for Month_item in range(12):
                for DayType_item in range(2):
                    for HH_item in range(48):
                        for Voltage_item in range(3):
    
                #cur.execute('''UPDATE DNO_Tariffs SET NSUos={Value} WHERE DNO = {dno}'''.format( Value=item_value, dno = Region)) 
                         cur.execute('''INSERT INTO DNO_Tariffs(DNO, year, Month, DayType, HH, Voltage, TNUos) VALUES({dno},{year},{Month},{Daytype},{HH},{Voltage},{Value})'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month = Month_item, Value=item_value))   
                         
conn.commit() 


# DUos capactiy
print('load DUos_cap:')
df = pd.read_excel('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Utility\\DUos_cap.xlsx''')

count=0
for raw in range(len(df)) :  
    year = df.iloc[raw,0]
    Voltage_item = df.iloc[raw,1]
    for col in range(len(df.axes[1])-2):
            Region = col+1          
            item_value  = df.iloc[raw, Region+1];   
            for Month_item in range(12):
                for DayType_item in range(2):
                    for HH_item in range(48):
    
                #cur.execute('''UPDATE DNO_Tariffs SET NSUos={Value} WHERE DNO = {dno}'''.format( Value=item_value, dno = Region)) 
                         try:
                             cur.execute('''INSERT INTO DNO_Tariffs(DNO, year, Month, DayType, HH, Voltage, DUos_cap) VALUES({dno},{year},{Month},{Daytype},{HH},{Voltage},{Value})'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month = Month_item, Value=item_value))   
                         except:
                             cur.execute('''UPDATE DNO_Tariffs SET DUos_cap={Value} WHERE DNO={dno} AND year={year} AND Month = {Month} AND HH={HH} AND Voltage={Voltage}'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month = Month_item, Value=item_value))   
                   

conn.commit() 


# DUos commodity
print('load DUos_com:')
df = pd.read_excel('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Utility\\DUos_com.xlsx''', sheetname = 'Sheet1')
df2 = pd.read_excel('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Utility\\DUos_com.xlsx''', sheetname = 'Sheet2')

count=0
for item in range(len(df)) :            
    year = df.iloc[item][0]
    Region = df.iloc[item][1]
    Voltage_item = df.iloc[item][2]
    for DayType_item in range(2):
        for HH_item in range(48):
            time_band = df2[HH_item].iloc[int((Region-1)*2+DayType_item)]
            item_value = df.iloc[item][3 + time_band] 
            for Month_item in range(12):
                    try:
                         cur.execute('''INSERT INTO DNO_Tariffs(DNO, year, Month, DayType, HH, Voltage, DUos_com) VALUES({dno},{year},{Month},{Daytype},{HH},{Voltage},{Value})'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month= Month_item, Value=item_value))   
                    except:
                         cur.execute('''UPDATE DNO_Tariffs SET DUos_com={Value} WHERE DNO={dno} AND year={year} AND Month = {Month} AND DayType = {Daytype} AND HH={HH} AND Voltage={Voltage}'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month = Month_item, Value=item_value))  
           
      

conn.commit() 



# Constant components
print('Constant components:')
df = pd.read_excel('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Utility\\Constant.xlsx''')

for item in range(len(df)) :            
    year = df.iloc[item][0]
    OR_tariff = df.iloc[item][1]
    CCL = df.iloc[item][2]
    FiT = df.iloc[item][3]
    AAHEDC = df.iloc[item][4]
    CfD = df.iloc[item][5]
    CM = df.iloc[item][6]
    Man_fee = df.iloc[item][7]
    for Region_item in range(14):
        Region = Region_item + 1
        for Month_item in range(12):
            for Voltage_item in range(3):
                for DayType_item in range(2):
                    for HH_item in range(48):
                        try:
                             cur.execute('''INSERT INTO DNO_Tariffs(DNO, year, Month, DayType, HH, Voltage, OR_tariff, CCL, FiT, AAHEDC, CfD, CM, Man_fee) VALUES({dno},{year}, {Month}, {Daytype},{HH},{Voltage},{ValueOR},{ValueCCL}, {ValueFiT}, {ValueAAHEDC}, {ValueCfD}, {ValueCM}, {ValueMan_fee})'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month=Month_item, ValueOR=OR_tariff, ValueCCL=CCL, ValueFiT = FiT, ValueAAHEDC = AAHEDC, ValueCfD = CfD, ValueCM = CM, ValueMan_fee = Man_fee))   
                        except:
                             cur.execute('''UPDATE DNO_Tariffs SET OR_tariff={ValueOR}, CCL = {ValueCCL}, FiT = {ValueFiT}, AAHEDC = {ValueAAHEDC}, CfD = {ValueCfD}, CM = {ValueCM}, Man_fee = {ValueMan_fee}  WHERE DNO={dno} AND year={year} AND Month={Month} AND DayType = {Daytype} AND HH={HH} AND Voltage={Voltage}'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month=Month_item, ValueOR=OR_tariff, ValueCCL=CCL, ValueFiT = FiT, ValueAAHEDC = AAHEDC, ValueCfD = CfD, ValueCM = CM, ValueMan_fee = Man_fee))   

conn.commit() 



## wierd had to separate... maybe string too long
for item in range(len(df)):
    year = df.iloc[item][0]
    Gas = df.iloc[item][8]
    CCL_Gas = df.iloc[item][9]
    for Region_item in range(14):
        Region = Region_item + 1
        for Month_item in range(12):
            for Voltage_item in range(3):
                for DayType_item in range(2):
                    for HH_item in range(48):
                        try:
                             cur.execute('''INSERT INTO DNO_Tariffs(DNO, year, Month, DayType, HH, Voltage, Gas, CCL_Gas) VALUES({dno},{year}, {Month}, {Daytype},{HH},{Voltage},{ValueGas},{ValueCCL_Gas})'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month=Month_item, ValueGas=Gas, ValueCCL_Gas=CCL_Gas))   
                        except:
                             cur.execute('''UPDATE DNO_Tariffs SET Gas={ValueGas}, CCL_Gas = {ValueCCL_Gas} WHERE DNO={dno} AND year={year} AND Month={Month} AND DayType = {Daytype} AND HH={HH} AND Voltage={Voltage}'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month=Month_item, ValueGas=Gas, ValueCCL_Gas=CCL_Gas))  

conn.commit()     



# LLF
print('load LLF:')
df = pd.read_excel('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Utility\\LLF.xlsx''', sheetname = 'Sheet1')
df2 = pd.read_excel('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Utility\\LLF.xlsx''', sheetname = 'Sheet2')

for item in range(len(df)) :            
    year = df.iloc[item][1]
    Region = df.iloc[item][0]
    Period = df.iloc[item][2]
    for Voltage_item in range(3):
            item_value = df.iloc[item][3+Voltage_item]
            if Period == 0:
                for Month_item in range(12):
                    for DayType_item in range(2):
                        for HH_item in range(48):
                            try:
                                cur.execute('''INSERT INTO DNO_Tariffs(DNO, year, Month, DayType, HH, Voltage, LLF) VALUES({dno},{year},{Month},{Daytype},{HH},{Voltage},{Value})'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month = Month_item, Value=item_value))   
                            except:
                                cur.execute('''UPDATE DNO_Tariffs SET LLF={Value} WHERE DNO={dno} AND year={year} AND Month = {Month} AND DayType = {Daytype} AND HH={HH} AND Voltage={Voltage}'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month = Month_item, Value=item_value))  
            else:            
                subset = df2[df2['DNO']==Region]
                subset = subset[subset['Period']== Period]
                for i in range(len(subset)):
                        M1 = subset.iloc[i,2]-1
                        M2 = subset.iloc[i,3]-1
                        if M1 > M2:
                            M4 = M2+1
                            M2 = 11
                            M3 = 0
                        else:    
                            M3 = 0
                            M4 = 0                        
                        for Month_item in it.chain(range(M1, M2+1), range(M3, M4)):
                            for DayType_item in range(2):
                                HH1 = subset.iloc[i,4+2*DayType_item]*2
                                HH2 = subset.iloc[i,5+2*DayType_item]*2
                                for HH_item in range(int(HH1),int(HH2)):
                                        try:
                                            cur.execute('''INSERT INTO DNO_Tariffs(DNO, year, Month, DayType, HH, Voltage, LLF) VALUES({dno},{year},{Month},{Daytype},{HH},{Voltage},{Value})'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month = Month_item, Value=item_value))   
                                        except:
                                            cur.execute('''UPDATE DNO_Tariffs SET LLF={Value} WHERE DNO={dno} AND year={year} AND Month = {Month} AND DayType = {Daytype} AND HH={HH} AND Voltage={Voltage}'''.format(dno = Region, Daytype = DayType_item, HH=HH_item, Voltage=Voltage_item, year= year, Month = Month_item, Value=item_value))  

    
conn.commit() 



