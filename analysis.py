import pandas as pd
import matplotlib.pyplot as plt

keys = ['Fuzzers', 'Exploits', 'Reconnaissance', 'DoS', 'Generic', 'Analysis', 'Backdoors', 'Worms', 'Shellcode', 'Normal']

features = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm']

file_name = '1_0w1_1w1_yshf_notime'
path = file_name+'.csv'
Dict = {}

with open(path,  newline='') as csvfile:
    df = pd.read_csv(csvfile, low_memory=False)

for feature in features:
    D = {}
    for key in keys:
        D[key] = []
    Dict[feature] = D

n = len(df.index)
for i in range(n):
    row = df.iloc[i, :]
    attack = row['attack_cat']

    if(type(attack) != type('a')): 
        attack = 'Normal'

    for feature in features:
        value = row[feature]
        
        Dict[feature][attack].append(value)

for feature in features:
    print(feature)
    print('------------------------------------')
    for key in keys:
        values = Dict[feature][key]
        try :
            mininum = min(values)
        except:
            mininum = 0
        try:
            maxinum = max(values)
        except:
            maxinum = 0
        print("{:<12s}{:<12s}{:>12f}{:<12s}{:>12f}".format(key,':\t', mininum,'\t', maxinum))

    print('==================================')

target = 'Dpkts'

plt.figure()
plt.title(target)

for i,key in enumerate(keys):
    values = Dict[target][key]
    cnt = pd.value_counts(values)
    cnt = cnt.sort_index()

    R = cnt.max()-cnt.min()
    scale = R/20
    bins =  [x*scale+cnt.min() for x in range(0,21) ]
    ax = plt.subplot(2,5,i+1)
    ax.title.set_text(key)
    plt.hist(cnt, bins=bins)

plt.show()







