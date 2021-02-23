import pandas as pd
import csv
import binascii
import random

file_path = 'UNSW-NB15_4.csv'

def seperateLabel():
    with open(file_path,  newline='') as csvfile:
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

    return df0, df1

def seperateTrainTest():
    csv1, csv2, new = [], [], []
    i = -1

    with open(file_path,  newline='') as csvfile:
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

    with open(file_path, newline='') as f:
        packets = pd.read_csv(f)

    df1 = pd.DataFrame(csv1, columns=packets.keys())
    df2 = pd.DataFrame(csv2, columns=packets.keys())

    return df1, df2

def seperateHttpFlow():
    with open(file_path,  newline='') as csvfile:
        packets = pd.read_csv(csvfile)

    http_list = []
    i=0
    for service in packets['service']:
        if service == 'http':
            http_list.append(list(packets.iloc[i, :]))
        i = i+1

    df = pd.DataFrame(http_list, columns=packets.keys())
    return df

def RandomDataAndBalance01():
    sample_n = 10000
    with open(file_path,  newline='', encoding='utf-8') as csvfile:
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

    n0 = len(df0.index)
    n1 = len(df1.index)

    row1 = random.sample(range(n0), sample_n)
    row2 = random.sample(range(n1), sample_n)

    df = pd.DataFrame(columns = packets.keys())

    for index in row1:
        df = df.append(df0.iloc[index], ignore_index=True)

    for index in row2:
        df = df.append(df1.iloc[index], ignore_index=True)

    return df

