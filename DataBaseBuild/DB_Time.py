# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 18:37:26 2017

@author: nl211
"""


import sqlite3
import pandas as pd
import numpy as np
import datetime
import calendar


sqlite3.register_adapter(np.float64, float)
sqlite3.register_adapter(np.float32, float)
sqlite3.register_adapter(np.int64, int)
sqlite3.register_adapter(np.int32, int)    

conn = sqlite3.connect('D:\\Database_SSL\\Code\\Sainsburys.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Time;
       
 CREATE TABLE Time (
     id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
     timestamp  TEXT,
     year INTEGER,
     Month INTEGER,
     Day,
     HH INTEGER,
     DayType INTEGER
 )


''')
 
 
#==============================================================================
# CREATE TIME DATABASE
#==============================================================================
#==============================================================================
timeSeries= pd.date_range("2012-01-01 00:00", "2018-01-01 00:00", freq="30min")


initial_time = datetime.datetime(2012,1,1)
final_time = datetime.datetime(2018,1,1)
start= int((initial_time-datetime.datetime(1970,1,1)).total_seconds()/60/30)
stop= int((final_time-datetime.datetime(1970,1,1)).total_seconds()/60/30)

for num in range(start,stop): 
     
    timestamp = datetime.datetime.fromtimestamp(num*60*30).strftime('%Y-%m-%d %H:%M:%S')
    year = datetime.datetime.fromtimestamp(num*60*30).year 
    Month = datetime.datetime.fromtimestamp(num*60*30).month -1
    Day = datetime.datetime.fromtimestamp(num*60*30).day
    HH = int(datetime.datetime.fromtimestamp(num*60*30).hour*2+datetime.datetime.fromtimestamp(num*60*30).minute/30)
     
     
      
    Cal =calendar.Calendar(calendar.SUNDAY).yeardays2calendar(year,1)
    NewCal = [[] for x in range(12)]
    count_month = 0
    for month in Cal:
        for week in month[0]:              
            for day in week:
                if day[0] is not 0:
                    NewCal[count_month].append(day)
        count_month = count_month + 1
        
    WeekDay = NewCal[Month][Day-1][1]
    if WeekDay == 5 or WeekDay == 6:
        WeekDayType = 1
    else:
        WeekDayType = 0
 
     #new_entry = pd.Timestamp(entry)
    cur.execute('''INSERT OR IGNORE INTO Time (id, timestamp, year, Month, Day, HH, DayType) VALUES (?, ?,?,?,?,?,? )''', (num, str(timestamp), year, Month, Day, HH, WeekDayType)) 

conn.commit()  