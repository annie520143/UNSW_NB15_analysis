import pandas as pd
import numpy as np

file_name = 'NUSW_mix_4.csv'
path = file_name

with open(path,  newline='') as csvfile:
    packets = pd.read_csv(csvfile, low_memory=False)


for i in range (len(packets)):

    if type(packets['is_ftp_login'][i]) != np.float64:
        print(i, type(packets['is_ftp_login'][i]))

print('done')