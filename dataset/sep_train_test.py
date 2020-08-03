import pandas as pd
import csv
import binascii

file_name = 'NUSW_mix_4.csv'
path = file_name

csv1, csv2, new = [], [], []
i = -1

with open(path,  newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        i = i +1

        if   (i < 60000) :

            if type(row[3]) == type('aa'):
                x = binascii.b2a_hex(row[3].encode('utf-8'))  # 16 base to 10 base
                row[3] = int(x, 16)

            csv1.append(row)

        else :
            if type(row[3]) == type('aa'):
                x = binascii.b2a_hex(row[3].encode('utf-8'))  # 16 base to 10 base
                row[3] = int(x, 16)

            csv2.append(row)
                
    
with open('NUSW20000.csv', newline='') as f:
    packets = pd.read_csv(f)

df1 = pd.DataFrame(csv1, columns=packets.keys())
df2 = pd.DataFrame(csv2, columns=packets.keys())
#df = pd.DataFrame(new, columns=packets.keys())
df1.to_csv('NUSW_mix4_train.csv')
df2.to_csv('NUSW_mix4_test.csv')

