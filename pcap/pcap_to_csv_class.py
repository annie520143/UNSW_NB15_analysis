import os
import scapy.all as sp
import numpy as np
import pandas as pd
import statistics

log_path = './NASHUA/'
filename = 'NASHUA'

def get_pcap_layers(packet):
    counter = 0
    while True:
        layer = packet.getlayer(counter)
        if layer is None:
            break

        yield layer
        counter += 1

class preprocessor():

    #class have object: pcap, conn.log, http.log
    def __init__(self, log_path):

        self.pcaps = sp.rdpcap(os.path.join(log_path, filename+'.pcapng'))
        self.zeek = pd.read_csv(os.path.join(log_path, 'conn.log.csv'), low_memory=False)
        self.srcip_bytes, self.dstip_bytes = [], []
        """self.index = np.empty((self.zeek.index, 0)).tolist()
        self.direction = [-1 for i in range (len(pcaps))]"""
        self.n = len(self.zeek.index)

        try:
            self.https = pd.read_csv(os.path.join(log_path, 'http.log.csv'), low_memory=False)
        except:
            self.https = -1

    def preprossing_zeek(self):

        self.srcip_bytes = self.zeek['orig_ip_bytes'].tolist()
        self.dstip_bytes = self.zeek['resp_ip_bytes'].tolist()

        #if the log file hasn't been filtered in linux
        del self.zeek['uid']
        del self.zeek['local_orig']
        del self.zeek['local_resp']
        del self.zeek['missed_bytes']
        del self.zeek['history']
        del self.zeek['orig_ip_bytes']
        del self.zeek['resp_ip_bytes']
        del self.zeek['tunnel_parents']

        #change the key name to the same as NUSW dataset
        self.zeek.columns = ['Stime', 'srcip', 'sport', 'dstip', 'dsport', 'proto', 'service', 'dur', 'sbytes', 'dbytes', 'state', 'Spkts', 'Dpkts']

    def get_flow_index(self):
    
        n = len(self.zeek.index)
        self.index = np.empty((n, 0)).tolist()
        self.direction = [-1 for i in range (len(self.pcaps))]

        for i in range(n):
            row = self.zeek.iloc[i, :]
            srcip, dstip, sport, dsport = row['srcip'], row['dstip'], row['sport'], row['dsport']

            for j, pcap in enumerate(self.pcaps):

                layers = []
                for layer in get_pcap_layers(pcap):
                    layers.append(layer.name)

                try:
                    ip = layers[1]
                    trans = layers[2]

                    #packets from src to dst
                    if ((srcip == pcap.getlayer(ip).src) & (dstip == pcap.getlayer(ip).dst) & 
                        (sport == pcap.getlayer(trans).sport) & (dsport == pcap.getlayer(trans).dport)):
                        self.index[i].append(j)
                        self.direction[j] = 0

                    #packets from dst to src
                    elif ((srcip == pcap.getlayer(ip).dst) & (dstip == pcap.getlayer(ip).src) & 
                        (sport == pcap.getlayer(trans).dport) & (dsport == pcap.getlayer(trans).sport)):
                        self.index[i].append(j)
                        self.direction[j] = 1

                except:continue

    def cnt_100_2(self, target):
    
        n = 100
        col = []
        t1 = target[0]
        t2 = target[1]

        for i in range (self.n):
            
            cnt = 0
            if i < n:
                for j in range(i):
                    if (self.zeek.iloc[i,:][t1] == self.zeek.iloc[j,:][t1]) & (self.zeek.iloc[i,:][t2] == self.zeek.iloc[j,:][t2]):
                        cnt = cnt+1

            else:
                for j in range(i-1, i-101, -1):
                    if (self.zeek.iloc[i,:][t1] == self.zeek.iloc[j,:][t1]) & (self.zeek.iloc[i,:][t2] == self.zeek.iloc[j,:][t2]):
                        cnt = cnt+1

            col.append(cnt)
            
        return col

    def cnt_100_1(self, target):

        n = 100
        col = []
        t1 = target[0]

        for i in range (self.n):
            
            cnt = 0
            if i < n:
                for j in range(i):
                    if (self.zeek.iloc[i,:][t1] == self.zeek.iloc[j,:][t1]):
                        cnt = cnt+1

            else:
                for j in range(i-1, i-101, -1):
                    if (self.zeek.iloc[i,:][t1] == self.zeek.iloc[j,:][t1]):
                        cnt = cnt+1

            col.append(cnt)
            
        return col

    def same_ip_port(self):

        is_sm_ips_ports = []
        for i in range(self.n):
            flow = self.zeek.iloc[i,:]
            if (flow['srcip'] == flow['dstip']) & (flow['sport'] == flow['dsport']):
                is_sm_ips_ports.append(1)
            else:
                is_sm_ips_ports.append(0)

        self.zeek = self.zeek.assign(is_sm_ips_ports = pd.Series(is_sm_ips_ports).values)


    def statis(self):
    
        self.same_ip_port()

        target = ['service', 'srcip']
        col = self.cnt_100_2(target)
        self.zeek = self.zeek.assign(ct_srv_src = pd.Series(col).values)

        target = ['service', 'dstip']
        col = self.cnt_100_2(target)
        self.zeek = self.zeek.assign(ct_srv_dst = pd.Series(col).values)

        target = ['srcip', 'dsport']
        col = self.cnt_100_2(target)
        self.zeek = self.zeek.assign(ct_src_dport_ltm = pd.Series(col).values)

        target = ['dstip', 'sport']
        col = self.cnt_100_2(target)
        self.zeek = self.zeek.assign(ct_dst_sport_ltm = pd.Series(col).values)

        target = ['srcip', 'dstip']
        col = self.cnt_100_2(target)
        self.zeek = self.zeek.assign(ct_dst_src_ltm = pd.Series(col).values)

        target = ['dstip']
        col = self.cnt_100_1(target)
        self.zeek = self.zeek.assign(ct_dst_ltm = pd.Series(col).values)

        target = ['srcip']
        col = self.cnt_100_1(target)
        self.zeek = self.zeek.assign(ct_src_ltm = pd.Series(col).values)

    def ip_feature(self):
    
        sttl, dttl = [],[]

        for i, idx in enumerate(self.index):

            if idx == []:
                sttl.append(0)
                dttl.append(0)
                continue
            
            flag_s = 0
            flag_d = 0

            for value in idx:

                if(self.pcaps[value].haslayer('IP') == False):
                    sttl.append(0)
                    dttl.append(0)
                    flag_d = 1
                    flag_s = 1
                    break
                
                if (flag_s == 0) & (self.direction[value] == 0):
                    sttl.append(self.pcaps[value].getlayer('IP').ttl)
                    flag_s = 1
                
                elif (flag_d == 0) & (self.direction[value] == 1):
                    dttl.append(self.pcaps[value].getlayer('IP').ttl)
                    flag_d = 1

                if flag_d & flag_s:
                    break

            if flag_d == 0:
                dttl.append(0)

        self.zeek = self.zeek.assign(sttl = pd.Series(sttl).values, dttl = pd.Series(dttl).values)

    def id_eq_http(self,flow, pkt):
        
        if ((flow['srcip'] == pkt['id_orig_h']) & (flow['dstip'] == pkt['id_resp_h']) 
        & (flow['sport'] == pkt['id_orig_p']) & (flow['dsport'] == pkt['id_resp_p'])):
            return True
        
        if  ((flow['dstip'] == pkt['id_orig_h']) & (flow['srcip'] == pkt['id_resp_h']) 
        & (flow['dsport'] == pkt['id_orig_p']) & (flow['sport'] == pkt['id_resp_p'])):
            return True
        
        return False

    def http_feature(self):
    
        trans_depth, res_len ,ct_flw_http_mthd = [], [], []

        if type(self.https) == type(-1): 
            for i in range (self.n):
                trans_depth.append(0)
                res_len.append(0)
                ct_flw_http_mthd.append(0)

            self.zeek = self.zeek.assign(trans_depth = pd.Series(trans_depth).values, res_len = pd.Series(res_len).values,
                            ct_flw_http_mthd = pd.Series(ct_flw_http_mthd).values)
            return

        for i in range (self.n):
    
            flow = self.zeek.iloc[i,:]
            if flow['service'] != 'http':
                ct_flw_http_mthd.append(0)
                trans_depth.append(0)
                res_len.append(0)
                continue

            len_avg = []
            depth_tmp = 0
            mthd_n = 0

            for j in range(len(self.https.index)):
                
                pkt = self.https.iloc[j,:]
                if self.id_eq_http(flow, pkt):
                    
                    depth_tmp = int(pkt['trans_depth'])
                    len_avg.append(int(pkt['response_body_len']))
                    mthd_n = mthd_n+1

            trans_depth.append(depth_tmp)
            ct_flw_http_mthd.append(mthd_n)

            try:
                res_len.append(int(statistics.mean(len_avg)))
            except:
                res_len.append(0)

        self.zeek = self.zeek.assign(trans_depth = pd.Series(trans_depth).values, res_len = pd.Series(res_len).values,
                            ct_flw_http_mthd = pd.Series(ct_flw_http_mthd).values)

    def general_feature(self):
        
        smeansz, dmeansz = [], []
        for i, idx in enumerate(self.index):

            if idx == []:
                smeansz.append(0)
                dmeansz.append(0)
                continue

            flow = self.zeek.iloc[i,:]

            try:
                smeansz.append(int(int(self.srcip_bytes[i])/int(flow['Spkts'])))
            except ZeroDivisionError:
                smeansz.append(int(self.srcip_bytes[i]))

            try:
                dmeansz.append(int(int(self.dstip_bytes[i])/int(flow['Dpkts'])))
            except ZeroDivisionError:
                dmeansz.append(int(self.dstip_bytes[i]))

        self.zeek = self.zeek.assign(smeansz = pd.Series(smeansz).values, dmeansz = pd.Series(dmeansz).values)


    def tcp_feature(self):
        
        swin, dwin, stcpb, dtcpb =[], [], [], []

        for i, idx in enumerate(self.index):

            if idx == []:
                swin.append(np.nan)
                dwin.append(0)
                stcpb.append(0)
                dtcpb.append(0)
                continue

            flow = self.zeek.iloc[i, :]
            swin_avg, dwin_avg = [], []
            flag_s=0
            flag_d=0
            syn=0
            syn_ack=0
            ack=0
            
            first_pck = self.pcaps[idx[0]]

            if first_pck.haslayer('TCP') == False: 
                swin.append(0)
                dwin.append(0)
                stcpb.append(0)
                dtcpb.append(0)
                continue

            for value in idx:

                #first packet in each direction : can get base sequence number and window size
                if (self.direction[value] == 0) & (flag_s==0):
                    flag_s=1
                    stcpb.append(self.pcaps[value].getlayer('TCP').seq)
                    swin_avg.append(self.pcaps[value].getlayer('TCP').window)

                elif (self.direction[value] == 1) & (flag_d==0):
                    flag_d=1
                    dtcpb.append(self.pcaps[value].getlayer('TCP').seq)
                    dwin_avg.append(self.pcaps[value].getlayer('TCP').window)
                    
                elif self.direction[value] == 0:
                    swin_avg.append(self.pcaps[value].getlayer('TCP').window)
                
                elif self.direction[value] == 1:
                    dwin_avg.append(self.pcaps[value].getlayer('TCP').window)

            

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

                
        self.zeek = self.zeek.assign(swin = pd.Series(swin).values, dwin = pd.Series(dwin).values)
        self.zeek = self.zeek.assign(stcpb = pd.Series(stcpb).values, dtcpb = pd.Series(dtcpb).values)


    def output(self):
        self.zeek.to_csv(os.path.join(log_path, filename+'.csv'), index=False)




P = preprocessor(log_path)

if __name__ == '__main__':

    P.preprossing_zeek()
    P.get_flow_index()
    P.statis()
    print('Done doing statisic...')
    P.ip_feature()
    print('Done filling ip features...')
    P.http_feature()
    print('Done filling http features...')
    P.general_feature()
    print('Done filling general features...')
    P.tcp_feature()
    print('Done filling tcp features...')

    P.output()

