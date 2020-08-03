import pandas as pd
import random

file_name = 'UNSW-NB15_1_nodup.csv'
path = file_name

with open(path,  newline='', encoding='utf-8') as csvfile:
    packets = pd.read_csv(csvfile)


label0, label1 = [], []
i=0

for label in packets['Label']:
    if label == 0:
        label0.append(list(packets.iloc[i, :]))
    elif label == 1:
        label1.append(list(packets.iloc[i, :]))
    i = i+1

df0 = pd.DataFrame(label0, columns=packets.keys())
df1 = pd.DataFrame(label1, columns=packets.keys())

"""df0.to_csv('NUSW40000-label0.csv')
df1.to_csv('NUSW40000-label1.csv')
"""

n0 = len(df0.index)
n1 = len(df1.index)


row1 = random.sample(range(n0), 10000)
row2 = random.sample(range(n1), 10000)

df = pd.DataFrame(columns = packets.keys())

for index in row1:
    df = df.append(df0.iloc[index], ignore_index=True)

for index in row2:
    df = df.append(df1.iloc[index], ignore_index=True)

df.to_csv('UNSW-NB15_1_random(2w)_nodup.csv')