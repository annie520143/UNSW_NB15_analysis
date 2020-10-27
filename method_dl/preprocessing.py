from sklearn.preprocessing import MinMaxScaler
#from sklearn.preprocessing import Imputer
import numpy as np
import pandas as pd
import re

# all feature, except srcip dstip
all_features = ['sport', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'service', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime','Sintpkt', 'Dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attackCat', 'Label']

imp_features = ['sport', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'service', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime',
                'Sintpkt', 'Dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attackCat', 'Label']

#mutable
oneHotDict = {
'proto' : ['tcp', 'udp', 'arp', 'ospf', 'ip', 'icmp', 'unas'],
'states' : ['FIN', 'CON', 'REQ', 'URH', 'ACC', 'CLO',  'ECO', 'ECR','INT', 'MAS', 'PAR',  'RST', 'TST', 'TXD',  'URN', 'RSTO'],
'service' : ['dns', 'smtp', 'http', 'ftp', 'ftp-data', 'pop3', 'ssh', 'dhcp', 'ssl', 'snmp', 'radius', 'irc']
}

attackCat = ['[\s]?A(.)*', '[\s]?B(.)*', '[\s]?D(.)*', '[\s]?E(.)*', '[\s]?G(.)*', '[\s]?R(.)*', '[\s]?S(.)*', '[\s]?W(.)*']


def SeperateAttackLabel(packets):
    dataAttackCat = packets['attack_cat'].to_numpy()
    newAttackCat = []
    newLabel = []

    re_match = 0
    for value in dataAttackCat:
        flag = 1
        for i, cat in enumerate(attackCat):
            try:
                re_match = re.match(cat, value)
            except: pass

            if ((((re_match!= None) | (value == 0)) & (flag))):
                flag = 0
                if value == 0:
                    newAttackCat.append(0)
                else:
                    newAttackCat.append(i+1)

                if(i != 0):
                    newLabel.append(1)
                else:
                    newLabel.append(0)

    del packets['attack_cat']
    del packets['Label']

    return packets, newAttackCat, newLabel


#one hot encoding
def FeatureOneHot(packets):

    for feature in oneHotDict.keys():
        try:
            data = packets[feature]
            for element in oneHotDict[feature]:
                tempList = []
                for d in data:
                    if (d == element):
                        tempList.append(1)
                    else:
                        tempList.append(0)
                packets[element] = tempList

        except:
            pass

    return packets
        

def GetImp(packets):
    imp_features_n = len(imp_features) 

    packets_imp = packets.copy()
    for col in (packets_imp.columns):
        for i in range(imp_features_n):
            tar = imp_features[i]
            #important features, check the next column
            if (col == tar):
                break

            #no important features match, and last feature has been checked
            elif ((col != tar) & (i == imp_features_n-1)):
                del packets_imp[col]

    return packets_imp


#normalization
def FeatureScaling(packets):
    sc = MinMaxScaler(feature_range=(0, 1))
    packets = np.nan_to_num(packets)
    packets_scaled = sc.fit_transform(packets)

    return packets_scaled


def TransDatatype(packets):
    feature_name = packets.keys().tolist()

    #transforming datatype (the default datatype of dataframe is "object", which cannot be used for arithemetic operations in the feature scaling function)
    for f in feature_name:
        packets[f] = pd.to_numeric(packets[f], errors='coerce')
        
    return packets


def NpFillna(packets):
    df = pd.DataFrame(packets)
    
    df.fillna(0, inplace= True)
    
    packets = df.values
    return packets
