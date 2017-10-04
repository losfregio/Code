# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 18:29:51 2017

@author: nl211
"""


import sqlite3
import pandas as pd
import numpy as np
import os
import re
import datetime
import time
import math



sqlite3.register_adapter(np.float64, float)
sqlite3.register_adapter(np.float32, float)
sqlite3.register_adapter(np.int64, int)
sqlite3.register_adapter(np.int32, int)    

conn = sqlite3.connect('D:\\Database_SSL\\Code\\Sainsburys.sqlite')
cur = conn.cursor()

## check and print the data files
print('demand data files:')
for fn in os.listdir('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Demand_new'''):
    #if os.path.isfile(fn):
    print (fn)


print('start creating demand database')
os.chdir('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Demand_new''')



#for fn in os.listdir('D:\AAraw'):
for fn in os.listdir('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Demand_new'''):
#xls = pd.ExcelFile("2.2.xlsx")
    xls = pd.ExcelFile(fn)    
    df1 = xls.parse(parse_cols = 1)
    str1 = df1.iloc[0,0]
    Type = []
    if 'Gas' in str1:
        Type = 'Gas'
    elif 'Electricity' in str1:
        Type = 'Ele'
    elif 'Refrigeration' in str1:
        Type = 'Ref'
    else:
        Type = 'Error'
    m = re.search('(?<=loc/)....', str1)
    id_store = str(int(m.group(0)))
    str2 = df1.iloc[4,1]
    if 'kWh' in str2:
        kWIO = 0
    else:
        kWIO = 1
    Series1 = df1.iloc[5::,0]
    Series2 = df1.iloc[5::,1]
    df2 = df1.iloc[5::,:]
    df2.columns = ['Time','Value']
    
    cur.execute('SELECT {sn} FROM Demand_Check Where Stores_id= {vn1}'.\
                    format(sn = Type, vn1 = id_store))
    dummy_type = cur.fetchone()
    
    if dummy_type is None or dummy_type[0] is not 1:
        
        print('''We don't have this file, let's add it!''')
                 
        print('file: {filename}, store id: {storenum},demand type: {demandtype}'.format(filename=fn,storenum=id_store,demandtype=Type ))    
        print ("")
        
        
        count=0
        Total = np.nan
        TotalDB = np.nan
        for item in range(len(df2)) : 
            t0 = time.time()
            
            item_timestamp = df2.iloc[item][0]
            item_time=int(time.mktime(item_timestamp.timetuple())/60/30)
           # item_time= int((item_timestamp-datetime.datetime(1970,1,1)).total_seconds()/60/30) wrong 1 hour of difference in some cases!! UTC vs local time?
            item_value  = df2.iloc[item][1]/(1+kWIO); 
            
            t1 = time.time()
            
            if math.isnan(item_value) is False:
            
                cur.execute('SELECT {sn} FROM Demand Where Stores_id= {vn1} AND  Time_id= {Time}'.\
                             format(sn = Type, Time = item_time, vn1 = id_store))
                dummy = cur.fetchone()
                    
                if dummy is None: 
                    cur.execute('''INSERT OR IGNORE INTO Demand(Stores_id, Time_id, {sn}) VALUES({vn1},{Time},{Value})'''.format(sn = Type, vn1 = id_store, Time = item_time, Value=item_value))   
                
                else : 
                    cur.execute('''UPDATE Demand SET {sn}={Value} WHERE Stores_id={vn1} AND Time_id = {Time}'''.format(sn = Type, vn1 = id_store, Time = item_time, Value=item_value))  
            
                count = count + 1
                if count == 500:
                       count=0   
                       timestamp = datetime.datetime.fromtimestamp(item_time*60*30).strftime('%Y-%m-%d %H:%M:%S')
                       print ('{store}: {varitm} \r'.format(store = id_store, varitm=timestamp))
                       
                       t2 = time.time()
                       conn.commit() 
                       
                       
                       print(t1-t0)
                       print(t2-t1)

        
        #check for data consistency based on 2016-2017 data.
        default_initial_time = datetime.datetime(2016,1,1)
        default_final_time = datetime.datetime(2017,1,1)
        time_start= int((default_initial_time-datetime.datetime(1970,1,1)).total_seconds()/60/30)
        time_stop= int((default_final_time-datetime.datetime(1970,1,1)).total_seconds()/60/30)
        cur.execute('''SELECT {sn} FROM Demand Where Stores_id= {vn1} AND Time_id > {timeStart} AND Time_id < {timeStop} '''.format(sn = Type, vn1 = id_store, timeStart = time_start-1, timeStop = time_stop))
        RawData = cur.fetchall()
        Total = sum(np.array([elt[0] for elt in RawData]))
        if Type == 'Ele':
            cur.execute('''SELECT ED2016 FROM Stores Where id = ? ''', (id_store,))
            try:
                TotalDB = cur.fetchone()[0]
            except:
                TotalDB = np.nan
                
        if Type == 'Gas':
            cur.execute('''SELECT GD2016 FROM Stores Where id = ? ''', (id_store,))
            try:
                TotalDB = cur.fetchone()[0]
            except:
                TotalDB = np.nan
        
        print('Data:{Total}, DB:{TotalDB}'.format(Total = Total, TotalDB = TotalDB))
        if Total > TotalDB*0.7 and Total < TotalDB*1.3:
            print('gutto des')
            try:
                cur.execute('''INSERT INTO Demand_Check(Stores_id, {sn}) VALUES({vn1},{Value})'''.format(sn = Type, vn1 = id_store, Value=1))
            except:
                cur.execute('''UPDATE Demand_Check SET {sn}={Value} WHERE Stores_id={vn1}'''.format(sn = Type, vn1 = id_store, Value=1))  
        else:
            print('bad des')
            
        

        
    conn.commit()   



# 
#==============================================================================
