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
"""

#create np array for label
def CategoryOneHot(label, opt):

    cat_n = 2 if(opt == 'label') else 10
    label_np = []

    for i in range(len(label)):
        for index in range(cat_n):
            if(label[i] == index):
                a = [0]*cat_n
                a[index] = 1
                label_np.append(a)

    label_np = np.array(label_np)
    return label_np


def ProcessData(datapath, opt):
    packets = pd.read_csv(datapath, low_memory=False)

    packets.fillna(value=0, inplace=True)  # fill missing with 0

    packets, attackCat, label = prep.SeperateAttackLabel(packets)

    print("shape: ", attackCat.shape, label.shape)

    packets = prep.FeatureOneHot(packets)
    packets = prep.TransDatatype(packets)

    #scaling (data type changes after scaling, i.e. df -> np)
    packetScaled = prep.FeatureScaling(packets)


    if(opt == 'attack_cat'):
        packetGroup, attackCatGroup = method.defRNN(packetScaled, attackCat, 10)
        attackCatOneHot = CategoryOneHot(attackCatGroup, opt)
        attackCatNP, packetsNP = np.array(attackCatOneHot), np.array(packetGroup)
        packetsNP = prep.NpFillna(packetsNP)
        return packetsNP, attackCatNP, attackCat
        
    elif(opt == 'label'):
        packetGroup, labelGroup = method.defRNN(packetScaled, label, 10)
        labelOneHot = CategoryOneHot(labelGroup, opt)
        labelNP, packetsNP = np.array(labelOneHot), np.array(packetGroup)
        packetsNP = prep.NpFillna(packetsNP)
        return packetsNP, labelNP, label


# all feature, except srcip dstip
all_features = ['sport', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'service', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime',
                'Sintpkt', 'Dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attackCat', 'Label']

imp_features = ['sport', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'service', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime',
                'Sintpkt', 'Dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attackCat', 'Label']

trainPath = "../dataset/UNSW-NB15_training-set.csv"
testPath = "../dataset/1_1-2_mix_time.csv"

opt = 'attack_cat'
usedModel = 'model/dnn_selfdef1_random.h5'

if __name__ == "__main__":

    train_path = "../dataset/UNSW-NB15_training-set.csv"
    
    expected_output = 'attack_cat'
    train_np, trainlabel_np, trainlabel_list = ProcessData(train_path, expected_output)

    
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

