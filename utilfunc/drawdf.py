import pandas as pd
import json
import numpy as np

def drawslots(tt,m,n):

    d = []
    for i in range(n):
        x = []
        for j in range (m):
            x.append("")
        d.append(x)

    T = pd.DataFrame(data=d,dtype='str')

    for slot in tt['slots']:
        for coord in slot['coord']:
            T[coord[1]][coord[0]] = T.iat[coord[0],coord[1]] + slot['slot']

    print(T)
    table = T.to_csv()

    with open(tt['name']+'.csv','w',newline='') as ff:
        ff.write(table)

