import pandas as pd
import numpy as np
import sys

import read_data as rd
import preprocessing as prep
import cluster_info as c_info

import method_kmeans as method_km


def Kmeans_fixed_k_info(packets, groups):
    km_max_label, km_group = method_km.Silh_fixed_size(packets, groups) 
    #6是從silh的圖中看出來的
    #print(km_group_number_list)

    return km_group
    

def init(packets):
    packets, attack_cat = prep.seperate_att_lab_catagory(packets)
    #if we want to do get specfic
    packets = prep.get_imp(packets)
    #packets = prep.add_sd_feature(packets)

    try: packets = prep.proto_to_value(packets)
    except: pass  
    try: packets = prep.state_to_value(packets)
    except: pass
    try: packets = prep.service_to_value(packets)
    except: pass

    print(packets.keys())

    return packets, attack_cat

def processed_data(data_df):
    
    data_df, attcat_list = init(data_df)

    del data_df['attack_cat']
    del data_df['Label']

    #transforming datatype
    data_df_transtype = prep.trans_datatype(data_df)

    #scaling (data type changes after scaling, i.e. df -> np)
    data_df_scale = prep.feature_scaling(data_df_transtype)

    #turn dataframe and list to np array
    data_np = np.array(data_df_scale)       
    data_np = prep.np_fillna(data_np)

    return data_np,attcat_list

def targeting(data_df, target):

    data_df = data_df[data_df.attack_cat != target]

    return data_df

def append_label(df, kmeans, base):
    j = 0
    n = len(df.index)
    origin_label = df['kmeans_label'].to_list()
    
    for i in range(n):
        #df.loc[(df.attack_cat == target), 'selfdef_label'] = base + kmeans[]
        if df.iloc[i,47] == target:
            #df.iloc[i,49] = base + kmeans[j]
            origin_label[i] = base + kmeans[j]
            j = j +1
    df['kmeans_label'] = origin_label
    df.to_csv('UNSW-NB15_1_random(2w)_self.csv', index=False)


train_path = "UNSW-NB15_1_random(2w)_self.csv"
target = 'Fuzzers'
base = 1
groups = 1

if __name__ == '__main__':

    df = pd.read_csv(train_path, low_memory=False)

    data_df = df.copy(deep=True)
    data_df = targeting(data_df, target)

    train_np, trainlabel_list = processed_data(data_df)
    
    np.set_printoptions(threshold=sys.maxsize)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    #method_km.Elbow(train_np)
    #method_km.Silh(train_np)
    kmeans = Kmeans_fixed_k_info(train_np, groups)

    append_label(df, kmeans, base)
