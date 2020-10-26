from random import shuffle
import pandas as pd


csv_file_1 = ['UNSW-NB15_1.csv']
csv_file_2 = ['UNSW-NB15_2.csv', 'UNSW-NB15_3.csv', 'UNSW-NB15_4.csv', ]

df_ref = pd.read_csv(csv_file_1[0], low_memory=False)
cnt0, cnt1, cnt2, cnt3, cnt4, cnt5, cnt6, cnt7, cnt8, cnt9, cntall = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
threshold_nor = 3700
threshold_attack = 800

threshold = 500
threshold_2 = 1000

df_tr = []
df_ts = []

for file in csv_file_1:
    df_temp = pd.read_csv(file, low_memory=False)
    df_temp.fillna(value=0, inplace=True)
    print(df_temp.head())
    df_temp = df_temp.sample(frac=1)
    print(df_temp.head())

    attack_cat = df_temp['attack_cat'].to_numpy()
    label = df_temp['Label'].to_numpy()


    
    for i, ele in enumerate(label):
        if ele == 0:
            cnt0 = cnt0+1
            if cnt0 > threshold_nor:
                continue
            df_tr.append(list(df_temp.iloc[i, :]))
        
        elif ele == 1:
            cnt1 = cnt1+1
            if cnt1 > threshold_attack:
                continue
            df_tr.append(list(df_temp.iloc[i, :]))
    
    """
    cnt0, cnt1 = 0, 0
    for i, ele in enumerate(label):
        if ele == 0:
            cnt0 = cnt0+1
            if cnt0 > threshold_2_test:
                continue
            elif cnt0 > threshold_test:
                df_ts.append(list(df_temp.iloc[i, :]))

        elif ele == 1:
            cnt1 = cnt1+1
            if cnt1 > threshold_2_test:
                continue
            elif cnt1 > threshold_test:
                df_ts.append(list(df_temp.iloc[i, :]))
    
    for i, ele in enumerate(attack_cat):
        if ele == 0:
            cnt0 = cnt0+1
            if cnt0 > threshold:
                continue
            df_tr.append(list(df_temp.iloc[i, :]))

        elif ele == 'Fuzzers':
            cnt1 = cnt1+1
            if cnt1 > threshold:
                continue
            df_tr.append(list(df_temp.iloc[i, :]))

        elif ele == 'Analysis':
            cnt2 = cnt2+1
            if cnt2 > threshold:
                continue
            df_tr.append(list(df_temp.iloc[i, :]))

        elif ele == 'Backdoors':
            cnt3 = cnt3+1
            if cnt3 > threshold:
                continue
            df_tr.append(list(df_temp.iloc[i, :]))

        elif ele == 'DoS':
            cnt4 = cnt4+1
            if cnt4 > threshold:
                continue
            df_tr.append(list(df_temp.iloc[i, :]))

        elif ele == 'Exploits':
            cnt5 = cnt5+1
            if cnt5 > threshold:
                continue
            df_tr.append(list(df_temp.iloc[i, :]))

        elif ele == 'Generic':
            cnt6 = cnt6+1
            if cnt6 > threshold:
                continue
            df_tr.append(list(df_temp.iloc[i, :]))

        elif ele == 'Reconnaissance':
            cnt7 = cnt7+1
            if cnt7 > threshold:
                continue

            df_tr.append(list(df_temp.iloc[i, :]))

        elif ele == 'Shellcode':
            cnt8 = cnt8+1
            if cnt8 > threshold:
                continue
            df_tr.append(list(df_temp.iloc[i, :]))

        elif ele == 'Worms':
            cnt9 = cnt9+1
            if cnt9 > threshold:
                continue
            df_tr.append(list(df_temp.iloc[i, :]))
            
    cnt0, cnt1, cnt2, cnt3, cnt4, cnt5, cnt6, cnt7, cnt8, cnt9, cntall = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    for i, ele in enumerate(attack_cat):
        cntall = cntall + 1

        if ele == 0:
            cnt0 = cnt0+1
            if (cnt0 > threshold_2):
                continue
            elif cnt0 > threshold:
                df_ts.append(list(df_temp.iloc[i, :]))

        elif ele == 'Fuzzers':
            cnt1 = cnt1+1
            if cnt1 > threshold_2:
                continue
            elif cnt1 > threshold:
                df_ts.append(list(df_temp.iloc[i, :]))

        
        elif ele == 'Analysis':
            cnt2 = cnt2+1
            if cnt2 > threshold_2:
                continue
            elif cnt2 > threshold:
                df_ts.append(list(df_temp.iloc[i, :]))
            

        
        elif ele == 'Backdoors':
            cnt3 = cnt3+1
            if cnt3 > threshold_2:
                continue
            elif cnt3 > threshold:
                df_ts.append(list(df_temp.iloc[i, :]))
            

        elif ele == 'DoS':
            cnt4 = cnt4+1
            if cnt4 > threshold_2:
                continue
            elif cnt4 > threshold:
                df_ts.append(list(df_temp.iloc[i, :]))
            
        

        elif ele == 'Exploits':
            cnt5 = cnt5+1
            if cnt5 > threshold_2:
                continue
            elif cnt5 > threshold:
                df_ts.append(list(df_temp.iloc[i, :]))
            
        
        elif ele == 'Generic':
            cnt6 = cnt6+1
            if cnt6 > threshold_2:
                continue
            elif cnt6 > threshold:
                df_ts.append(list(df_temp.iloc[i, :]))
            

        elif ele == 'Reconnaissance':
            cnt7 = cnt7+1
            if cnt7 > threshold_2:
                continue
            elif cnt7 > threshold:
                df_ts.append(list(df_temp.iloc[i, :]))
            

        elif ele == 'Shellcode':
            cnt8  = cnt8+1
            if cnt8 > threshold_2:
                continue
            elif cnt8 > threshold:
                df_ts.append(list(df_temp.iloc[i, :]))
            
        
        elif ele == 'Worms':
            cnt9 = cnt9+1
            if cnt9 > threshold_2:
                continue
            elif cnt9 > threshold:
                df_ts.append(list(df_temp.iloc[i, :]))
    
    """

    cnt0, cnt1, cnt2, cnt3, cnt4, cnt5, cnt6, cnt7, cnt8, cnt9, cntall = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    for i, ele in enumerate(attack_cat):
        cntall = cntall + 1

        if cntall < threshold_attack:
            continue
        else:
            if ele == 0:
                cnt0 = cnt0+1
                if cnt0 > threshold:
                    continue
                df_ts.append(list(df_temp.iloc[i, :]))
                

            elif ele == 'Fuzzers':
                cnt1 = cnt1+1
                if cnt1 > threshold:
                    continue
                df_ts.append(list(df_temp.iloc[i, :]))
                #print(cntall, " ")

            elif ele == 'Analysis':
                cnt2 = cnt2+1
                if cnt2 > threshold:
                    continue
                df_ts.append(list(df_temp.iloc[i, :]))

            elif ele == 'Backdoors':
                cnt3 = cnt3+1
                if cnt3 > threshold:
                    continue
                df_ts.append(list(df_temp.iloc[i, :]))

            elif ele == 'DoS':
                cnt4 = cnt4+1
                if cnt4 > threshold:
                    continue
                df_ts.append(list(df_temp.iloc[i, :]))

            elif ele == 'Exploits':
                cnt5 = cnt5+1
                if cnt5 > threshold:
                    continue
                df_ts.append(list(df_temp.iloc[i, :]))

            elif ele == 'Generic':
                cnt6 = cnt6+1
                if cnt6 > threshold:
                    continue
                df_ts.append(list(df_temp.iloc[i, :]))

            elif ele == 'Reconnaissance':
                cnt7 = cnt7+1
                if cnt7 > threshold:
                    continue

                df_ts.append(list(df_temp.iloc[i, :]))

            elif ele == 'Shellcode':
                cnt8 = cnt8+1
                if cnt8 > threshold:
                    continue
                df_ts.append(list(df_temp.iloc[i, :]))

            elif ele == 'Worms':
                cnt9 = cnt9+1
                if cnt9 > threshold:
                    continue
                df_ts.append(list(df_temp.iloc[i, :]))
    

df_tr = pd.DataFrame(df_tr, columns=df_ref.keys())
df_ts = pd.DataFrame(df_ts, columns=df_ref.keys())
df_tr.to_csv('train_label_nobalance.csv', index=False)
df_ts.to_csv('test_balance.csv', index=False)

