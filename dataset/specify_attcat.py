import pandas as pd

csv_file_1 = ['UNSW-NB15_4.csv']
csv_file = ['UNSW-NB15_1.csv', 'UNSW-NB15_2.csv', 'UNSW-NB15_3.csv']

df_ref = pd.read_csv('UNSW-NB15_1.csv')
df = pd.DataFrame(columns = df_ref.keys())
cnt5, cnt6, cnt7, cnt8 = 0,0,0,0
threshold = 100

for file in csv_file_1:
    
    df_ref = pd.read_csv(file, low_memory=False)
    attack_cat = df_ref['attack_cat']
    print('Processing: ', file)
    for i, ele in enumerate(attack_cat):
        
        if ele == 'Exploits':
            cnt5  = cnt5+1
            if cnt5 > threshold:
                continue
            df = df.append(df_ref.iloc[i], ignore_index=True)

        elif ele == 'Generic':
            cnt6  = cnt6+1
            if cnt6 > threshold:
                continue
            df = df.append(df_ref.iloc[i], ignore_index=True)

        elif ele == 'Reconnaissance':
            cnt7  = cnt7+1
            if cnt7 > threshold:
                continue
            df = df.append(df_ref.iloc[i], ignore_index=True)
        
        elif ele == 'Shellcode':
            cnt8  = cnt8+1
            if cnt8 > threshold:
                continue
            df = df.append(df_ref.iloc[i], ignore_index=True)


"""for file in csv_file_1:
    df_ref = pd.read_csv(file, low_memory=False)
    attack_cat = df_ref['attack_cat']

    for i, ele in enumerate(attack_cat):

        if ele == 'Reconnaissance':
            cnt  = cnt+1
            if cnt > 200:
                break
            df = df.append(df_ref.iloc[i], ignore_index=False)

        
            
    #print(df_based)"""

df.to_csv('label5,6,7,8_test.csv')