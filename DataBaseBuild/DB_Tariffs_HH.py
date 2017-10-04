# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 19:02:17 2017

@author: nl211
"""


import sqlite3
import pandas as pd
import numpy as np
import datetime
import time

sqlite3.register_adapter(np.float64, float)
sqlite3.register_adapter(np.float32, float)
sqlite3.register_adapter(np.int64, int)
sqlite3.register_adapter(np.int32, int)    

conn = sqlite3.connect('D:\\Database_SSL\\Code\\Sainsburys.sqlite')
cur = conn.cursor()



cur.executescript('''
DROP TABLE IF EXISTS Tariffs_HH;

        
 CREATE TABLE Tariffs_HH (
     id     INTEGER NOT NULL PRIMARY KEY UNIQUE,
     Ele  FLOAT,
     BSUos FLOAT,
     TLM   FLOAT,
     FOREIGN KEY(id) REFERENCES Time(id)
     
 )


''')

#==============================================================================
# Import electricity prices 
#==============================================================================

print('load electricity price:')
df = pd.read_excel('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Utility\\Ele.xlsm''')
 
count=0
for item in range(len(df)) :            
            item_timestamp = df.iloc[item][0]
            item_time=int(  (time.mktime(item_timestamp.timetuple()) + (df.iloc[item][1]-1)*1800)/60/30)
           # this will miss the forward change of hour. BE CAREFFUL!  
           # item_time= int((item_timestamp-datetime.datetime(1970,1,1)).total_seconds()/60/30) wrong 1 hour of difference in some cases!! UTC vs local time?
            item_value  = df.iloc[item][2]; 

            cur.execute('''INSERT OR IGNORE INTO Tariffs_HH (id, Ele) VALUES({Time},{Value})'''.format(Time = item_time, Value=item_value))   
             
            count = count + 1
            if count == 500:
                       count=0   
                       timestamp = datetime.datetime.fromtimestamp(item_time*60*30).strftime('%Y-%m-%d %H:%M:%S')
                       print(' {varitm} \r'.format(varitm=timestamp))
                       #print item_time
                       
conn.commit() 

#==============================================================================
# Import BSUos tariffs
#==============================================================================  
                     
print('load BSUos:')
df = pd.read_excel('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Utility\\BSUos.xlsx''')
 
               
count=0
for item in range(len(df)) :            
            item_timestamp = df.iloc[item][0]
            item_time=int(  (time.mktime(item_timestamp.timetuple()) + (df.iloc[item][1]-1)*1800)/60/30)
           # item_time= int((item_timestamp-datetime.datetime(1970,1,1)).total_seconds()/60/30) wrong 1 hour of difference in some cases!! UTC vs local time?
            item_value  = df.iloc[item][2]; 

            cur.execute('''UPDATE Tariffs_HH SET BSUos={Value} WHERE id={Time}'''.format(Time = item_time, Value=item_value)) 
             
            count = count + 1
            if count == 500:
                       count=0   
                       timestamp = datetime.datetime.fromtimestamp(item_time*60*30).strftime('%Y-%m-%d %H:%M:%S')
                       print (' {varitm} \r'.format(varitm=timestamp))
                       
conn.commit() 

#==============================================================================
# Import TLM tariffs
#==============================================================================  
                     
print('load TLM:')
df = pd.read_excel('''D:\\Database_SSL\\Code\\DataBaseBuild\\RawData\\Utility\\TLM.xlsx''')
 
               
count=0
for item in range(len(df)) :            
            item_timestamp = df.iloc[item][0]
            item_time=int(  (time.mktime(item_timestamp.timetuple()) + (df.iloc[item][1]-1)*1800)/60/30)
           # item_time= int((item_timestamp-datetime.datetime(1970,1,1)).total_seconds()/60/30) wrong 1 hour of difference in some cases!! UTC vs local time?
            item_value  = df.iloc[item][2]; 

            cur.execute('''UPDATE Tariffs_HH SET TLM={Value} WHERE id={Time}'''.format(Time = item_time, Value=item_value)) 
             
            count = count + 1
            if count == 500:
                       count=0   
                       timestamp = datetime.datetime.fromtimestamp(item_time*60*30).strftime('%Y-%m-%d %H:%M:%S')
                       print (' {varitm} \r'.format(varitm=timestamp))
                       
conn.commit() 

