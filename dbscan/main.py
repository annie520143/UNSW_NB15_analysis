import pandas as pd
import numpy as np
import sys
"""
"""
import method_dbscan as method_db
import cluster_info as c_info
import preprocessing as prep




def init(packets):
    packets, attack_cat = prep.seperate_att_lab_catagory(packets)
    #if we want to do get specfic
    packets = prep.get_imp(packets)
    #packets = prep.add_sd_feature(packets)

    try:
        packets = prep.proto_to_value(packets)
    except:
        pass
    try:
        packets = prep.state_to_value(packets)
    except:
        pass
    try:
        packets = prep.service_to_value(packets)
    except:
        pass

    #print(packets.keys())

    return packets, attack_cat


def targeting(data_df, target):

    data_df = data_df[data_df.attack_cat == target]

    return data_df


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

    return data_np, attcat_list

"""
def Dbscan_fixed_eps_info(eps, packets):
    c_info.packets_in_cluster(db_group_number_list, db_max_label+1)
    for i in range(db_max_label+1):
        c_info.print_cluster(pkt, db_group_number_list, i)
    c_info.print_outlier(pkt, db_group_number_list)
"""

#reduce_d.LDA(packets, db_group_number_list)
train_path = "../dataset/UNSW-NB15_1_attack(balances).csv"
target = 'Reconnaissance'
eps = 1.5


#if this file being run directly by python(__name__ == "__main__") or is it being imported
if __name__ == "__main__":

    df = pd.read_csv(train_path, low_memory=False)

    data_df = df.copy(deep=True)
    data_df = targeting(data_df, target)
    
    #trained by normal packets
    

    train_np, trainlabel_list = processed_data(data_df)

    #mix packets, see outlier as abnormal packets
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    dbscan, db_max_label, db_group_number_list = method_db.DBscan_fixed_eps(train_np, eps)
    print("how many group? ", db_max_label+1)
    print(db_group_number_list)

    #label_test = method_db.DBscan_predict(packets, eps, dbscan)
    #method_db.DBscan_score(label_test, label)

    """normalize_features = normalize_http
    prep.normalization(packets_0, normalize_features)
    prep.normalization(packets, normalize_features)
    dbscan, db_max_label, db_group_number_list = method_db.DBscan_fixed_eps(
        packets_0, eps)
    label_test = method_db.DBscan_predict(packets, eps, dbscan)
    method_db.DBscan_score(label_test, label)"""

    """ for i in range(10):
        forest = method_iF.isolation_forest(packets_0)
        method_iF.outlier_predict(forest, packets, label)
 """
