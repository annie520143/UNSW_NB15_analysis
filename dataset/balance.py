import pandas as pd

df_based = pd.read_csv('1_0w1_1w1_yshf_notime.csv')
df_extra = pd.read_csv('UNSW-NB15_3.csv')
attack_cat = df_extra['attack_cat']
n = df_based.index+1

for i, ele in enumerate(attack_cat):
    if ele == 'Shellcode' or ele == 'Worms':
        #df_based.loc[n] = df_extra.iloc[i]
        #n=n+1
        df_based = df_based.append(df_extra.iloc[i], ignore_index=True)
        
#print(df_based)

df_based.to_csv('1_0w1_1w1_yshf_notime_balance.csv')