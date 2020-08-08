import scapy.all as sp
import numpy as np
import pandas as pd
import statistics

def get_pcap_layers(packet):
    counter = 0
    while True:
        layer = packet.getlayer(counter)
        if layer is None:
            break

        yield layer
        counter += 1


def id_eq_http(flow, pkt):
    
    if ((flow['srcip'] == pkt['id_orig_h']) & (flow['dstip'] == pkt['id_resp_h']) 
    & (flow['sport'] == pkt['id_orig_p']) & (flow['dsport'] == pkt['id_resp_p'])):
        return True
    
    if  ((flow['dstip'] == pkt['id_orig_h']) & (flow['srcip'] == pkt['id_resp_h']) 
    & (flow['dsport'] == pkt['id_orig_p']) & (flow['sport'] == pkt['id_resp_p'])):
        return True
    
    return False
        
def get_flow_index(zeek, pcaps):

    n = len(zeek.index)
    index = np.empty((n, 0)).tolist()
    direction = [-1 for i in range (len(pcaps))]

    for i in range(n):
        row = zeek.iloc[i, :]
        srcip, dstip, sport, dsport = row['srcip'], row['dstip'], row['sport'], row['dsport']

        for j, pcap in enumerate(pcaps):

            layers = []
            for layer in get_pcap_layers(pcap):
                layers.append(layer.name)

            try:
                ip = layers[1]
                trans = layers[2]

                #packets from src to dst
                if ((srcip == pcap.getlayer(ip).src) & (dstip == pcap.getlayer(ip).dst) & 
                    (sport == pcap.getlayer(trans).sport) & (dsport == pcap.getlayer(trans).dport)):
                    index[i].append(j)
                    direction[j] = 0

                #packets from dst to src
                elif ((srcip == pcap.getlayer(ip).dst) & (dstip == pcap.getlayer(ip).src) & 
                    (sport == pcap.getlayer(trans).dport) & (dsport == pcap.getlayer(trans).sport)):
                    index[i].append(j)
                    direction[j] = 1

            except:continue

    return index, direction


def preprossing(zeek):

    srcip_bytes = zeek['orig_ip_bytes'].tolist()
    dstip_bytes = zeek['resp_ip_bytes'].tolist()

    #if the log file hasn't been filtered in linux
    del zeek['uid']
    del zeek['local_orig']
    del zeek['local_resp']
    del zeek['missed_bytes']
    del zeek['history']
    del zeek['orig_ip_bytes']
    del zeek['resp_ip_bytes']
    del zeek['tunnel_parents']

    #change the key name to the same as NUSW dataset
    zeek.columns = ['Stime', 'srcip', 'sport', 'dstip', 'dsport', 'proto', 'service', 'dur', 'sbytes', 'dbytes', 'state', 'Spkts', 'Dpkts']

    return zeek, srcip_bytes, dstip_bytes

def fill_tcp_feature(zeek, pcaps, index, direction):

    swin, dwin, stcpb, dtcpb =[], [], [], []

    #print(index)

    for i, idx in enumerate(index):

        if idx == []:
            swin.append(np.nan)
            dwin.append(0)
            stcpb.append(0)
            dtcpb.append(0)
            continue

        flow = zeek.iloc[i, :]
        swin_avg, dwin_avg = [], []
        flag_s=0
        flag_d=0
        syn=0
        syn_ack=0
        ack=0
        
        first_pck = pcaps[idx[0]]

        if first_pck.haslayer('TCP') == False: 
            swin.append(0)
            dwin.append(0)
            stcpb.append(0)
            dtcpb.append(0)
            continue

        for value in idx:

            #first packet in each direction : can get base sequence number and window size
            if (direction[value] == 0) & (flag_s==0):
                flag_s=1
                stcpb.append(pcaps[value].getlayer('TCP').seq)
                swin_avg.append(pcaps[value].getlayer('TCP').window)

            elif (direction[value] == 1) & (flag_d==0):
                flag_d=1
                dtcpb.append(pcaps[value].getlayer('TCP').seq)
                dwin_avg.append(pcaps[value].getlayer('TCP').window)
                
            elif direction[value] == 0:
                swin_avg.append(pcaps[value].getlayer('TCP').window)
            
            elif direction[value] == 1:
                dwin_avg.append(pcaps[value].getlayer('TCP').window)

        

        if flag_d == 0:
            dtcpb.append(0)
        
        #calculate average window size for each flow
        try:
            swin.append(int(statistics.mean(swin_avg)))
        except:
            swin.append(0)

        try:
            dwin.append(int(statistics.mean(dwin_avg)))
        except:
            dwin.append(0)

            
    zeek = zeek.assign(swin = pd.Series(swin).values, dwin = pd.Series(dwin).values)
    zeek = zeek.assign(stcpb = pd.Series(stcpb).values, dtcpb = pd.Series(dtcpb).values)

    return zeek
    

def fill_general_feature(zeek, index, srcip_bytes, dstip_bytes):
    
    smeansz, dmeansz = [], [], []
    for i, idx in enumerate(index):

        if idx == []:
            smeansz.append(0)
            dmeansz.append(0)

            continue

        flow = zeek.iloc[i,:]

        try:
            smeansz.append(int(int(srcip_bytes[i])/int(flow['Spkts'])))
        except ZeroDivisionError:
            smeansz.append(int(srcip_bytes[i]))

        try:
            dmeansz.append(int(int(dstip_bytes[i])/int(flow['Dpkts'])))
        except ZeroDivisionError:
            dmeansz.append(int(dstip_bytes[i]))

    zeek = zeek.assign(smeansz = pd.Series(smeansz).values, dmeansz = pd.Series(dmeansz).values)

    return zeek

def fill_ip_feature(zeek, pcaps, index, direction):

    sttl, dttl = [],[]

    for i, idx in enumerate(index):

        if idx == []:
            sttl.append(0)
            dttl.append(0)
            continue
        
        flag_s = 0
        flag_d = 0

        for value in idx:

            if(pcaps[value].haslayer('IP') == False):
                sttl.append(0)
                dttl.append(0)
                flag_d = 1
                flag_s = 1
                break
               
            if (flag_s == 0) & (direction[value] == 0):
                sttl.append(pcaps[value].getlayer('IP').ttl)
                flag_s = 1
            
            elif (flag_d == 0) & (direction[value] == 1):
                dttl.append(pcaps[value].getlayer('IP').ttl)
                flag_d = 1

            if flag_d & flag_s:
                break

        if flag_d == 0:
            dttl.append(0)

    zeek = zeek.assign(sttl = pd.Series(sttl).values, dttl = pd.Series(dttl).values)

    return zeek

def fill_http_feature(zeek, pcaps, index):

    trans_depth, res_len ,ct_flw_http_mthd = [], [], []

    #if http.log don't exist
    try : 

        #############################
        #   place http.log file     #
        #############################

        http = pd.read_csv('./openvas/http.log.csv')
    except : 
        for i in range (len(zeek.index)):
            trans_depth.append(0)
            res_len.append(0)
            ct_flw_http_mthd.append(0)

        zeek = zeek.assign(trans_depth = pd.Series(trans_depth).values, res_len = pd.Series(res_len).values,
                        ct_flw_http_mthd = pd.Series(ct_flw_http_mthd).values)

        return zeek

        

    for i in range (len(zeek.index)):

        flow = zeek.iloc[i,:]
        if flow['service'] != 'http':
            ct_flw_http_mthd.append(0)
            trans_depth.append(0)
            res_len.append(0)
            continue

        len_avg = []
        depth_tmp = 0
        mthd_n = 0

        for j in range(len(http.index)):
            
            pkt = http.iloc[j,:]
            if id_eq_http(flow, pkt):
                
                depth_tmp = int(pkt['trans_depth'])
                len_avg.append(int(pkt['response_body_len']))
                mthd_n = mthd_n+1

        
        trans_depth.append(depth_tmp)
        ct_flw_http_mthd.append(mthd_n)

        try:
            res_len.append(int(statistics.mean(len_avg)))
        except:
            res_len.append(0)

    zeek = zeek.assign(trans_depth = pd.Series(trans_depth).values, res_len = pd.Series(res_len).values,
                        ct_flw_http_mthd = pd.Series(ct_flw_http_mthd).values)

    return zeek

def same_ip_port(zeek):
    is_sm_ips_ports = []
    for i in range(len(zeek.index)):
        flow = zeek.iloc[i,:]
        if (flow['srcip'] == flow['dstip']) & (flow['sport'] == flow['dsport']):
            is_sm_ips_ports.append(1)
        else:
            is_sm_ips_ports.append(0)

    zeek = zeek.assign(is_sm_ips_ports = pd.Series(is_sm_ips_ports).values)
    return zeek

def cnt_100_2(zeek, target):

    n = 100
    col = []
    t1 = target[0]
    t2 = target[1]

    for i in range (len(zeek.index)):
         
        cnt = 0
        if i < n:
            for j in range(i):
                if (zeek.iloc[i,:][t1] == zeek.iloc[j,:][t1]) & (zeek.iloc[i,:][t2] == zeek.iloc[j,:][t2]):
                    cnt = cnt+1

        else:
            for j in range(i-1, i-101, -1):
                if (zeek.iloc[i,:][t1] == zeek.iloc[j,:][t1]) & (zeek.iloc[i,:][t2] == zeek.iloc[j,:][t2]):
                     cnt = cnt+1

        col.append(cnt)
        
    return col

def cnt_100_1(zeek, target):

    n = 100
    col = []
    t1 = target[0]

    for i in range (len(zeek.index)):
         
        cnt = 0
        if i < n:
            for j in range(i):
                if (zeek.iloc[i,:][t1] == zeek.iloc[j,:][t1]):
                    cnt = cnt+1

        else:
            for j in range(i-1, i-101, -1):
                if (zeek.iloc[i,:][t1] == zeek.iloc[j,:][t1]):
                     cnt = cnt+1

        col.append(cnt)
        
    return col

def statis(zeek):

    zeek = same_ip_port(zeek)

    target = ['service', 'srcip']
    col = cnt_100_2(zeek, target)
    zeek = zeek.assign(ct_srv_src = pd.Series(col).values)

    target = ['service', 'dstip']
    col = cnt_100_2(zeek, target)
    zeek = zeek.assign(ct_srv_dst = pd.Series(col).values)

    target = ['srcip', 'dsport']
    col = cnt_100_2(zeek, target)
    zeek = zeek.assign(ct_src_dport_ltm = pd.Series(col).values)

    target = ['dstip', 'sport']
    col = cnt_100_2(zeek, target)
    zeek = zeek.assign(ct_dst_sport_ltm = pd.Series(col).values)

    target = ['srcip', 'dstip']
    col = cnt_100_2(zeek, target)
    zeek = zeek.assign(ct_dst_src_ltm = pd.Series(col).values)

    target = ['dstip']
    col = cnt_100_1(zeek, target)
    zeek = zeek.assign(ct_dst_ltm = pd.Series(col).values)

    target = ['srcip']
    col = cnt_100_1(zeek, target)
    zeek = zeek.assign(ct_src_ltm = pd.Series(col).values)

    return zeek
                

if __name__ == '__main__':
    
    #########################
    #   place pcap file     #
    #########################

    pcaps = sp.rdpcap('./openvas/openvas.pcapng')
    n = len(pcaps)

    #############################
    #   place conn.log file     #
    #############################

    zeek = pd.read_csv('./openvas/conn.log.csv', low_memory=False)
    zeek, srcip_bytes, dstip_bytes = preprossing(zeek)
    #print(srcip_bytes)

    #in each flow, get the index of the original packets
    index, direction = get_flow_index(zeek, pcaps)

    zeek = statis(zeek)
    zeek = fill_ip_feature(zeek, pcaps, index, direction)
    zeek = fill_http_feature(zeek, pcaps, index)
    zeek = fill_general_feature(zeek, index, srcip_bytes, dstip_bytes)
    zeek = fill_tcp_feature(zeek, pcaps, index, direction)

       
    zeek.to_csv('./openvas/openvas.csv', index=False)
