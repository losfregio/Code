
import sqlite3
import Common.classStore as st
import Common.classTech as tc
import Solvers.classCHPProblem as pb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

database_path = ".\\Sainsburys.sqlite"
conn = sqlite3.connect(database_path)
#cur = conn.cursor()

print("my version")

id_store_min = 0
id_store_max = 3000
CHP_cat1, CHP_cat2, CHP_cat3 = ([] for i in range(3))
store1, store2, store3 = ([] for i in range(3))
for id_store in range(id_store_min, id_store_max ):
    goodIO = 0
    cur.execute('''SELECT Ele, Gas FROM Demand_Check Where Stores_id= {vn1}'''.format(vn1=id_store))
    checkIO = cur.fetchall()
    try:
        if checkIO[0][0] == 1:
            if checkIO[0][1] == 1:
                goodIO = 1
    except:
        pass

    if goodIO == 1:
        cur.execute(
            '''SELECT Area FROM Stores Where id= {vn1}'''.format(
                vn1=id_store))
        Index = cur.fetchall()
        if not Index:
            pass
        else:
            Area = np.array([elt[0] for elt in Index])

            if Area <= 25000:
                category = 1

            elif 25000 < Area <= 45000:
                category = 2

            elif Area > 45000:
                category = 3

            else:
                print("Not able to categorise")
            if category == 1:
                pb1 = pb.CHPproblem(id_store)
                solution = pb1.SimpleOpti5NPV()
                CHP_cat1.append(solution[8])
                store1.append(id_store)
            if category == 2:
                pb1 = pb.CHPproblem(id_store)
                solution = pb1.SimpleOpti5NPV()
                CHP_cat2.append(solution[8])
                store2.append(id_store)
            if category == 3:
                pb1 = pb.CHPproblem(id_store)
                solution = pb1.SimpleOpti5NPV()
                CHP_cat3.append(solution[8])
                store3.append(id_store)

print(CHP_cat3)
plt.plot(store1, CHP_cat1, 'ro', label='cat1')
plt.plot(store2, CHP_cat2, 'bo', label='cat2')
plt.plot(store3, CHP_cat3, 'go', label='cat3')
plt.legend()
plt.show()
