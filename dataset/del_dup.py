import pandas as pd
import csv

file_name = 'UNSW-NB15_4'
path = file_name+'.csv'
new_df = []
dul_df = []

with open(path,  newline='') as csvfile:
    df = pd.read_csv(csvfile, low_memory=False)

for i in range(len(df)):

    if (i > 0):    
        if ((df['Sload'][i] != df['Sload'][i-1]) & (df['Dload'][i] != df['Dload'][i-1])):
            new_df.append(list(df.iloc[i, :]))
        else:
            dul_df.append(list(df.iloc[i, :]))

            
""" new = pd.DataFrame(new_df, columns=df.keys())
new.to_csv(file_name+'_nodup.csv', index = False) """

dul = pd.DataFrame(dul_df, columns=df.keys())
dul.to_csv(file_name+'_dupdata.csv', index=False)
