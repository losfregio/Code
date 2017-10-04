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

cur.executescript('''
DROP TABLE IF EXISTS Demand;
DROP TABLE IF EXISTS Demand_Check;

CREATE TABLE Demand (
    Stores_id     INTEGER,
    Time_id       INTEGER,
               Ele FLOAT,
               Gas FLOAT,
               Ref FLOAT,
    FOREIGN KEY(Stores_id) REFERENCES Stores(id),
    FOREIGN KEY(Time_id) REFERENCES Time(id),
    PRIMARY KEY (Stores_id , Time_id)
   
);


CREATE TABLE Demand_Check(
    Stores_id     INTEGER,
               Ele INTEGER,
               Gas INTEGER,
               Ref INTEGER,
    FOREIGN KEY(Stores_id) REFERENCES Stores(id),
    PRIMARY KEY (Stores_id)
)



''')

                
conn.commit()   


# 
#==============================================================================
