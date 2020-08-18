import numpy as np
import pandas as pd
import sys

"""
callback function
"""
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
import keras.models as ks

"""
preprocessing
"""
import preprocessing as prep
"""
Keras Method
"""
from keras.models import Sequential
import method_dnn as method 
#import temp_iptable as iptable

normalize_all = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1', 'dstip2']


def init(packets, result_opt):
    #deal with missing
    packets.fillna(value=0, inplace=True)  # fill missing with 0

    packets = prep.proto_to_value(packets)    
    #packets = prep.state_to_value(packets)   
    del packets['state'] 
    packets = prep.service_to_value(packets)
    #packets, srcip = prep.ip_to_value(packets)
    
    if(result_opt == 'attack_cat'):
        packets, attack_cat = prep.seperate_att_lab_catagory(packets)
        #if we want to do get specfic
        packets = prep.get_imp(packets)

        return packets, attack_cat
    elif(result_opt == 'label'):
        packets, label = prep.seperate_att_lab_label(packets)
        #if we want to do get specfic
        packets = prep.get_imp(packets)
        return packets, label
    
    
    

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
def attackcat_to_nparr_specify(label_list):

    label_np = []
    for i in range (label_list.shape[0]):
        if(label_list[i] == 5):
            label_np.append([1, 0, 0, 0])
        elif(label_list[i] == 6):
            label_np.append([0, 1, 0, 0])
        elif(label_list[i] == 7):
                label_np.append([0, 0, 1, 0])
        elif(label_list[i] == 8):
            label_np.append([0, 0, 0, 1])
        
    return label_np

#create np array for label
def attackcat_to_nparr(label_list):

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

    label_np = np.array(label_np)

    return label_np


def processed_data(datapath, result_opt):
    data_df = pd.read_csv(datapath, low_memory=False)
    
    if(result_opt == 'attack_cat'):
        data_df, attcat_list = init(data_df, result_opt)
        #print("1 ", type(data_srcip))

        del data_df['attack_cat']
        del data_df['Label']

        #transforming datatype
        data_df_transtype = prep.trans_datatype(data_df)
        #print("2 ", type(data_df))

        #scaling (data type changes after scaling, i.e. df -> np)
        data_df_scale = prep.feature_scaling(data_df_transtype)
        #print("3 ", type(data_df))

        #create an one-hot list for label list
        attcat_list_oneHot = attackcat_to_nparr(attcat_list)

        #turn dataframe and list to np array
        attcat_np, data_np = np.array(attcat_list_oneHot), np.array(data_df_scale)
        #deal with problem of key 'ct_ftp_cmd'
        
        data_np = prep.np_fillna(data_np)


        return data_np, attcat_np, attcat_list

    elif(result_opt == 'label'):
        data_df, label_list = init(data_df, result_opt)

        del data_df['attack_cat']
        del data_df['Label']

        #transforming datatype
        data_df_transtype = prep.trans_datatype(data_df)
        #print("2 ", type(data_df))

        #scaling (data type changes after scaling, i.e. df -> np)
        data_df_scale = prep.feature_scaling(data_df_transtype)
        #print("3 ", type(data_df))

        #create an one-hot list for label list
        datalabel_list_oneHot = label_to_nparr(label_list)
        
        #turn dataframe and list to np array
        label_np, data_np = np.array(datalabel_list_oneHot), np.array(data_df_scale)
        #deal with problem of key 'ct_ftp_cmd'
        data_np = prep.np_fillna(data_np)

        return data_np, label_np, label_list

def info():
    print('Basic info:')
    print('training dataset:', train_path)
    print('testing dataset: ', test_path)
    print('model: ', used_model)
    print('===================================')


train_path = "../dataset/UNSW-NB15_1_random(2w).csv"
test_path = "../dataset/2_0w4_1w4_nshf_notime.csv"

expected_output = 'attack_cat'
used_model = 'model/dnn_selfdef1_random.h5'


if __name__ == "__main__":


    #label depends on expected_output
    train_np, trainlabel_np, trainlabel_list = processed_data(train_path, expected_output)
    test_np, testlabel_np, testlabel_list = processed_data(test_path, expected_output)
    #print(len(train_attackcat[0]))

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    dataset_size = train_np.shape[0]  # how many data
    feature_dim = train_np.shape[1] # how mant features

    print(train_np.shape)

    # simpleDNN_dropout(feature_dim, units, atv, loss)
    if(expected_output == 'label'):
        model = method.simpleDNN_dropout(feature_dim, 32, 'relu', 'mse', 2)
    elif(expected_output == 'attack_cat'):
        model = method.simpleDNN_dropout(feature_dim, 32, 'relu', 'mse', 10)

    # Setting callback functions
    csv_logger = CSVLogger('training.log')

    checkpoint = ModelCheckpoint(filepath=used_model,
                                verbose=1,
                                save_best_only=True,
                                monitor='accuracy',
                                mode='max')
    earlystopping = EarlyStopping(monitor='accuracy',
                                patience=10,
                                verbose=1,
                                mode='max')

    
    #training
    model.fit(train_np, trainlabel_np, batch_size=100, epochs=100, callbacks=[
            earlystopping, checkpoint, csv_logger], shuffle=True)
    #model.fit(train_np, trainlabel_np, batch_size=100, epochs=10, shuffle=True)

    result = model.evaluate(train_np,  trainlabel_np)
    print("training accuracy = ", result[1])
   

    model = ks.load_model(used_model)
    #print(model.summary())
    
    """ result = model.evaluate(test_np,  testlabel_np)
    print("testing accuracy = ", result[1])"""
    
    predictLabel = model.predict_classes(test_np)
    #print(predictLabel)
    np.set_printoptions(threshold=sys.maxsize)

    method.matricsDNN(predictLabel, testlabel_list, expected_output)
    method.detailAccuracyDNN(predictLabel, testlabel_list, expected_output)


