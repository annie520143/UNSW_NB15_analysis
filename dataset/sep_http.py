import pandas as pd

file_name = 'NUSW20000.csv'
path = 'dataset/'+file_name

with open(path,  newline='') as csvfile:
    packets = pd.read_csv(csvfile)

http_list = []
i=0

for service in packets['service']:
    if service == 'http':
        http_list.append(list(packets.iloc[i, :]))

    i = i+1

df = pd.DataFrame(http_list, columns=packets.keys())

df.to_csv('dataset/NUSW20000-http.csv')

