import numpy as np
import pandas as pd

"""
callback function
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping

"""
preprocessing
"""
import preprocessing as prep
"""
Keras Method
"""
from keras.models import Sequential
import method_rnn as method

""" 
normalize_all = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1', 'dstip2']
"""

def init(packets, result_opt):
    #deal with missing
    packets.fillna(value=0, inplace=True)  # fill missing with 0

    #one hard encoding
    packets = prep.proto_to_value(packets)
    #packets = prep.state_to_value(packets)
    del packets['state']  
    
    packets = prep.service_to_value(packets)
    #packets, temp_srcip = prep.ip_to_value(packets)

    #seperate attack category and label (in case of future comparing, don't return)
    if(result_opt == 'attack_cat'):
        packets, attack_cat = prep.seperate_att_lab_catagory(packets)
    elif(result_opt == 'label'):
        packets, label = prep.seperate_att_lab_label(packets)

    #if we want to do get only non-flow features
    packets = prep.get_imp(packets)

    return packets

#create np array for label
def label_to_nparr(label_list):

    label_np = []
    for i in range (label_list.shape[0]):
        if(label_list[i] == 0):
            label_np.append([1, 0])
        elif(label_list[i] == 1):
            label_np.append([0, 1])
        
    return label_np



#create np array for label
def cat_to_nparr(label_list):

    label_np = []
    for i in range(label_list.shape[0]):
        if(label_list[i] == 0):
            label_np.append([1,0,0,0,0,0,0,0,0,0])
        elif(label_list[i] == 1):
            label_np.append([0,1,0,0,0,0,0,0,0,0])
        elif(label_list[i] == 2):
            label_np.append([0,0,1,0,0,0,0,0,0,0])
        elif(label_list[i] == 3):
            label_np.append([0,0,0,1,0,0,0,0,0,0])
        elif(label_list[i] == 4):
            label_np.append([0,0,0,0,1,0,0,0,0,0])
        elif(label_list[i] == 5):
            label_np.append([0,0,0,0,0,1,0,0,0,0])
        elif(label_list[i] == 6):
            label_np.append([0,0,0,0,0,0,1,0,0,0])
        elif(label_list[i] == 7):
            label_np.append([0,0,0,0,0,0,0,1,0,0])
        elif(label_list[i] == 8):
            label_np.append([0,0,0,0,0,0,0,0,1,0])
        elif(label_list[i] == 9):
            label_np.append([0,0,0,0,0,0,0,0,0,1])

    return label_np


def processed_data(datapath, result_opt):
    data_df = pd.read_csv(datapath, low_memory=False)
    data_df = init(data_df, result_opt)

    if(result_opt == 'attack_cat'):
        data_np, datalabel_list = method.defRNN_cat(data_df, 10)
        
        #create an one-hot list for label list
        datalabel_list_oneHot = cat_to_nparr(datalabel_list)
    elif(result_opt == 'label'):  
        data_np, datalabel_list = method.defRNN_label(data_df, 10)
        #create an one-hot list for label list
        datalabel_list_oneHot = label_to_nparr(datalabel_list)
    
    #turn dataframe and list to np array
    datalabel_np = np.array(datalabel_list_oneHot)

    data_np = prep.np_fillna(data_np)
    
    return data_np, datalabel_np, datalabel_list



if __name__ == "__main__":

    train_path = "../dataset/UNSW_NB15_training-set.csv"
    
    expected_output = 'attack_cat'
    train_np, trainlabel_np, trainlabel_list = processed_data(train_path, expected_output)

    
    dataset_size = train_np.shape[0]  # how many data
    feature_dim = train_np[0].shape   # input dimention

    

    # simpleRNN(feature_dim, atv, loss, output dim)
    if(expected_output == 'label'):
        model = method.simpleRNN(feature_dim, 'relu', 'mse', 2)
    elif(expected_output == 'attack_cat'):
        model = method.simpleRNN(feature_dim, 'relu', 'mse', 10)

    # Setting callback functions
    csv_logger = CSVLogger('training.log')

    checkpoint = ModelCheckpoint(filepath='model/rnn_best_cat_10.h5',
                                verbose=1,
                                save_best_only=True,
                                monitor='accuracy',
                                mode='max')
    earlystopping = EarlyStopping(monitor='accuracy',
                                patience=3,
                                verbose=1,
                                mode='max')

    #training
    model.fit(train_np, trainlabel_np, batch_size=100, epochs=15, callbacks=[earlystopping, checkpoint, csv_logger], validation_split=0.1)

