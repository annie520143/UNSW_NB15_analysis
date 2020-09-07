from sklearn.preprocessing import MinMaxScaler
#from sklearn.preprocessing import Imputer
import numpy as np
import pandas as pd

all_features = ['sport', 'dsport', 'dur', 'proto','state','sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss',  'service','Sload', 'Dload', 'Spkts', 'Dpkts', 'swin', 'dwin', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Sintpkt', 'Dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports', 'ct_state_ttl','ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attack_cat', 'Label']

#全部feature 不含srcip dstip
imp_features = ['sport', 'dsport', 'proto',  'state', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'service', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attack_cat', 'Label']

sd_features = ['sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload',
'Spkts', 'Dpkts', 'swin', 'dwin', 'smeansz', 'dmeansz', 'Sjit', 'Djit', 'Sintpkt', 'Dintpkt']

http_features = ['srcip', 'sport', 'dstip', 'dsport', 'proto', 'dur', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'Label', 'attack_cat']
proto = ['tcp', 'udp', 'arp', 'ospf', 'ip', 'icmp', 'unas']
states = ['FIN', 'CON', 'REQ', 'URH', 'ACC', 'CLO',  'ECO', 'ECR',
'INT', 'MAS', 'PAR',  'RST', 'TST', 'TXD',  'URN', 'RSTO', ]
#states = 

service = ['dns', 'smtp', 'http', 'ftp', 'ftp-data', 'pop3', 'ssh', 'dhcp', 'ssl', 'snmp', 'radius', 'irc']


def seperate_att_lab_catagory(packets):

    attack_cat = packets['attack_cat'].to_numpy()
    
    # Fuzzers, Analysis, Backdoors, DoS, Exploits, Generic, Reconnaissance, Shellcode and Worms
    for i,value in enumerate(attack_cat):

        if value == 'Fuzzers':
            attack_cat[i] = 1
        elif value == 'Analysis':
            attack_cat[i]  = 2
        elif value == 'Backdoors':
            attack_cat[i]  = 3
        elif value == 'DoS':
            attack_cat[i]  = 4
        elif value == 'Exploits':
            attack_cat[i]  = 5
        elif value == 'Generic':
            attack_cat[i]  = 6
        elif value == 'Reconnaissance':
            attack_cat[i]  = 7
        elif value == 'Shellcode':
            attack_cat[i]  = 8
        elif value == 'Worms':
            attack_cat[i]  = 9
        else:
            attack_cat[i]  = 0

    #label = packets['Label'].to_numpy()
    packets['attack_cat'] = attack_cat

    return packets, attack_cat

def seperate_att_lab_label(packets):
    
    label = packets['Label'].to_numpy()
    return packets, label


def proto_to_value(packets):
    """ proto = []
    for p in packets['proto']:
        if(p not in proto):
            proto.append(p)
    """

    for element in proto:   

        proto_list = []
        for protocol in packets['proto']:

            if(protocol == element):
                proto_list.append(1)
            else:
                proto_list.append(0)

        packets[element] = proto_list

    del packets['proto']


    return packets



def state_to_value(packets):

    for element in states:
        state_list = []
        for state in packets['state']:

            if(state == element):
                state_list.append(1)
            else:
                state_list.append(0)

        packets[element] = state_list

    del packets['state']

    return packets
    


def service_to_value(packets):
    """ service = []
    for s in packets['service']:
        if(s not in service):
            service.append(s)   """
    
    #print(service)

    for element in service:
        service_list = []
        for serv in packets['service']:

            if(serv == element):
                service_list.append(1)
            else:
                service_list.append(0)

        packets[element] = service_list

    del packets['service']

    return packets
    


def ip_to_value(packets):
    #ip is stored as string
    #print(type(packets.loc[1]['srcip']))

    n = len(packets)

    srcip = packets['srcip']
    dstip = packets['dstip']

    srcip1, srcip2, dstip1, dstip2 = [], [], [], []

    for i in range(n):

        srcip_split = srcip[i].split(".")
        dstip_split = dstip[i].split(".")

        srcip1.append(int(srcip_split[0], base=10))
        srcip2.append(int(srcip_split[1], base=10))

        dstip1.append(int(dstip_split[0], base=10))
        dstip2.append(int(dstip_split[1], base=10))

    packets['srcip1'], packets['srcip2'] = srcip1, srcip2
    packets['dstip1'], packets['dstip2'] = dstip1, dstip2

    del packets['srcip'], packets['dstip']
    srcip_list = srcip.tolist()
    dstip_list = dstip.tolist()

    return packets, srcip_list, dstip_list
    

#important features
def get_http(packets):
    http_features_n = len(http_features)
    #cnt = 0

    packets_http = packets.copy()
    for col in (packets_http.columns):
        for i in range(http_features_n):

            #important features, check the next column
            if (col == http_features[i]):
                break

            #no important features match, and last feature has been checked
            elif ((col != http_features[i]) & (i == http_features_n-1)):
                del packets_http[col]

    return packets_http


def get_imp(packets):
    imp_features_n = len(all_features) 
    cnt = 0

    packets_imp = packets.copy()
    for col in (packets_imp.columns):
        for i in range(imp_features_n):
            tar = all_features[i]
            #important features, check the next column
            if (col == tar):
                break

            #no important features match, and last feature has been checked
            elif ((col != tar) & (i == imp_features_n-1)):
                del packets_imp[col]

    return packets_imp

def add_sd_feature(packets):
    sd_features_n = int(len(sd_features) / 2)

    packets_sd = packets.copy()
    for i in range(sd_features_n):
        s_tar = sd_features[2*i]
        d_tar = sd_features[2*i+1]

        tar = 'avg_' + s_tar[1:]

        packets_sd[tar] = (packets_sd[s_tar] + packets_sd[d_tar]) / 2
        del packets_sd[s_tar]
        del packets_sd[d_tar]
                
    return packets_sd

#normalization
def feature_scaling(packets):
    sc = MinMaxScaler(feature_range=(0, 1))
    packets = np.nan_to_num(packets)
    packets_scaled = sc.fit_transform(packets)

    return packets_scaled


def normalization(packets, features):
    for f in features:       
        packets[f] = (packets[f] - packets[f].min()) /\
            (packets[f].max() - packets[f].min())
        
    return packets

def trans_datatype(packets):
    feature_name = packets.keys().tolist()

    #transforming datatype (the default datatype of dataframe is "object", which cannot be used for arithemetic operations in the feature scaling function)
    for f in feature_name:
        packets[f] = pd.to_numeric(packets[f], errors='coerce')
        
    return packets


def np_fillna(packets):
    df = pd.DataFrame(packets)
    #print("is nan? ", df.isnull().any())
    df.fillna(0, inplace= True)
    #print("is nan? again??? ", df.isnull().any())
    #print(df.isnull().any())
    packets = df.values
    return packets
