import pandas as pd

file_name = 'UNSW-NB15_1.csv'
path = file_name

with open(path,  newline='') as csvfile:
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

df0.to_csv('NUSW40000-label0.csv')
df1.to_csv('NUSW40000-label1.csv')

