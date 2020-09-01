import pandas as pd

#csv_file_1 = ['UNSW-NB15_1.csv']
csv_file = ['UNSW-NB15_1.csv', 'UNSW-NB15_2.csv', 'UNSW-NB15_4.csv']

df_ref = pd.read_csv('UNSW-NB15_1_random(2w).csv', low_memory=False)
cnt0, cnt1, cnt2, cnt3, cnt4, cnt5, cnt6, cnt7, cnt8, cnt9 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
threshold = 500



df = []

for file in csv_file:
    df_temp = pd.read_csv(file, low_memory=False)
    attack_cat = df_temp['attack_cat'].to_numpy()
    label = df_temp['Label'].to_numpy()

    for i, ele in enumerate(label):
        if ele == 0:
            cnt0 = cnt0+1
            if cnt0 > threshold:
                continue
            df.append(list(df_temp.iloc[i, :]))

    for i, ele in enumerate(attack_cat):

        if ele == 'Fuzzers':
            cnt1 = cnt1+1
            if cnt1 > threshold:
                continue
            df.append(list(df_temp.iloc[i, :]))

        elif ele == 'Analysis':
            cnt2 = cnt2+1
            if cnt2 > threshold:
                continue
            df.append(list(df_temp.iloc[i, :]))

        elif ele == 'Backdoors':
            cnt3 = cnt3+1
            if cnt3 > threshold:
                continue
            df.append(list(df_temp.iloc[i, :]))

        elif ele == 'DoS':
            cnt4 = cnt4+1
            if cnt4 > threshold:
                continue
            df.append(list(df_temp.iloc[i, :]))

        elif ele == 'Exploits':
            cnt5 = cnt5+1
            if cnt5 > threshold:
                continue
            df.append(list(df_temp.iloc[i, :]))

        elif ele == 'Generic':
            cnt6 = cnt6+1
            if cnt6 > threshold:
                continue
            df.append(list(df_temp.iloc[i, :]))

        elif ele == 'Reconnaissance':
            cnt7 = cnt7+1
            if cnt7 > threshold:
                continue
            df.append(list(df_temp.iloc[i, :]))

        elif ele == 'Shellcode':
            cnt8  = cnt8+1
            if cnt8 > threshold:
                continue
            df.append(list(df_temp.iloc[i, :]))
        
        elif ele == 'Worms':
            cnt9 = cnt9+1
            if cnt9 > threshold:
                continue
            df.append(list(df_temp.iloc[i, :]))

df = pd.DataFrame(df, columns=df_ref.keys())
df.to_csv('UNSW-NB15_1_attack(balances).csv', index=False)
