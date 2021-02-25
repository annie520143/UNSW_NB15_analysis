from sklearn.preprocessing import MinMaxScaler
#from sklearn.preprocessing import Imputer
import numpy as np
import pandas as pd
import re

#mutable
oneHotDict = {
'proto' : ['tcp', 'udp', 'arp', 'ospf', 'ip', 'icmp', 'unas'],
'states' : ['FIN', 'CON', 'REQ', 'URH', 'ACC', 'CLO',  'ECO', 'ECR','INT', 'MAS', 'PAR',  'RST', 'TST', 'TXD',  'URN', 'RSTO'],
'service' : ['dns', 'smtp', 'http', 'ftp', 'ftp-data', 'pop3', 'ssh', 'dhcp', 'ssl', 'snmp', 'radius', 'irc']
}

attackCat = [r'[\s]?N(.)*', r'[\s]?F(.)*', r'[\s]?A(.)*', r'[\s]?B(.)*', r'[\s]?D(.)*', r'[\s]?E(.)*', r'[\s]?G(.)*', r'[\s]?R(.)*', r'[\s]?S(.)*', r'[\s]?W(.)*']


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
                    newLabel.append(0)
                else:
                    newAttackCat.append(i)
                    newLabel.append(1)
                
                """
                if(value != 0):
                    newLabel.append(1)
                else:
                    newLabel.append(0)
                    print("hi!! ")
                """
    
    del packets['attack_cat']
    del packets['Label']
    newAttackCat = np.array(newAttackCat)
    newLabel = np.array(newLabel)


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
        

def GetImp(packets,imp_features):
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


def TransDatatype(packets):
    feature_name = packets.keys().tolist()

    #transforming datatype (the default datatype of dataframe is "object", which cannot be used for arithemetic operations in the feature scaling function)
    for f in feature_name:
        packets[f] = pd.to_numeric(packets[f], errors='coerce')
        
    return packets


#normalization
def FeatureScaling(packets):
    sc = MinMaxScaler(feature_range=(0, 1))
    packets = np.nan_to_num(packets)
    packets_scaled = sc.fit_transform(packets)

    return packets_scaled


def NpFillna(packets):
    packets[np.isnan(packets)] = 0
    
    return packets
