import pandas as pd
import csv
import binascii

file_name = 'UNSW-NB15_1.csv'
path = file_name

label0, label1, new = [], [], []
i, j = 0, 0

with open(path,  newline='') as csvfile:
    rows = csv.reader(csvfile)
    
    for row in rows:
            
        n = len(row)
        label = row[n-1]
        #print (label)

        if type(row[3]) == type('aa'):
            x = binascii.b2a_hex(row[3].encode('utf-8'))  # 字符串转16进制
            row[3] = int(x, 16)

        if (label == '0') & (i < 10000):
            label0.append(row)
            new.append(row)
            i = i+1
        
        elif (label == '1') & (j < 10000):
            label1.append(row)
            new.append(row)
            j = j+1
    
with open('NUSW20000.csv', newline='') as f:
    packets = pd.read_csv(f)

df0 = pd.DataFrame(label0, columns=packets.keys())
df1 = pd.DataFrame(label1, columns=packets.keys())
df = pd.DataFrame(new, columns=packets.keys())

df0.to_csv('NUSW10000-0.csv')
df1.to_csv('NUSW10000-1.csv')
df.to_csv('NUSW_mix.csv')

