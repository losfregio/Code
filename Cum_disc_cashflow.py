
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
cur = conn.cursor()

id_store_min = 0
id_store_max = 3000
store1, store2, store3 = ([] for i in range(3))
financials1, financials2, financials3 = ([] for i in range(3))
carbon1, carbon2, carbon3 = ([] for i in range(3))
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
                solution = pb.CHPproblem(id_store).SimpleOpti5NPV()
                financials1.append(solution[4][4])
                carbon1.append(solution[5][2])
                store1.append(id_store)
            if category == 2:
                solution = pb.CHPproblem(id_store).SimpleOpti5NPV()
                financials2.append(solution[4][4])
                carbon2.append(solution[5][2])
                store2.append(id_store)
            if category == 3:
                solution = pb.CHPproblem(id_store).SimpleOpti5NPV()
                financials3.append(solution[4][4])
                carbon3.append(solution[5][2])
                store3.append(id_store)

'''plt.figure(1)
plt.plot(store1, financials1, 'ro', label='cat1')
plt.plot(store2, financials2, 'bo', label='cat2')
plt.plot(store3, financials3, 'go', label='cat3')
plt.legend()
plt.show()

plt.figure(2)

plt.plot(store1, carbon1, 'ro', label='cat1')
plt.plot(store2, carbon2, 'bo', label='cat2')
plt.plot(store3, carbon3, 'go', label='cat3')
plt.legend()
plt.show()'''

MAC = [-np.average(financials1)/abs(np.average(carbon1)),
       -np.average(financials2)/abs(np.average(carbon2)),
       -np.average(financials3)/abs(np.average(carbon3))]

average1 = np.average(carbon1)
average2 = np.average(carbon2)
average3 = np.average(carbon3)
print(average1, average2, average3)

width = [average1, average2, average3]
cum_width = np.cumsum(width)
ind = [width[0]/2, (cum_width[1]-cum_width[0])/2+cum_width[0], (cum_width[2]-cum_width[1])/2+cum_width[1]]

plt.figure(3)
p1 = plt.bar(ind, MAC, width, linewidth=1, edgecolor='black')
plt.xlabel('$tCO_2e$ savings')
plt.ylabel('$£/tCO_2e$')
plt.title('MAC curves for each store category and CHP implementation 2016-17')
plt.show()

rects = p1.patches
labels = ['Category 1', 'Category 2', 'Category 3']
for rect, label in zip(rects, labels):
    height = rect.get_height()
    p1.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')
plt.show()
