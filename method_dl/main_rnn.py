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
    #print(label_np[:10])
    return label_np


def ProcessData(datapath, opt):
    packets = pd.read_csv(datapath, low_memory=False)

    packets.fillna(value=0, inplace=True)  # fill missing with 0

    packets, attackCat, label = prep.SeperateAttackLabel(packets)

    #print("shape: ", attackCat.shape, label.shape)

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

opt = 'label'
usedModel = 'model/rnn_best_cat_10.h5'

if __name__ == "__main__":
    
    #label depends on expected_output
    trainNP, trainlabelNP, trainlabelList = ProcessData(trainPath, opt)
    testNP, testlabelNP, testlabelList = ProcessData(testPath, opt)

    
    
    dataset_size = trainNP.shape[0]  # how many data
    feature_dim = (trainNP.shape[1], trainNP.shape[2])  # input dimention
    output_dim = trainlabelNP.shape[1]  # label -> 2, attack_cat -> 10
    

    # simpleRNN(feature_dim, atv, loss, output dim)
    if(opt == 'label'):
        model = method.simpleRNN(feature_dim, 'relu', 'mse', output_dim)
    elif(opt == 'attack_cat'):
        model = method.simpleRNN(feature_dim, 'relu', 'mse', output_dim)

    # Setting callback functions
    csv_logger = CSVLogger('rnn_training.log')

    checkpoint = ModelCheckpoint(filepath=usedModel,
                                verbose=1,
                                save_best_only=True,
                                monitor='accuracy',
                                mode='max')
    earlystopping = EarlyStopping(monitor='accuracy',
                                patience=3,
                                verbose=1,
                                mode='max')

    #training
    model.fit(trainNP, trainlabelNP, batch_size=100, epochs=15, callbacks=[earlystopping, checkpoint, csv_logger], validation_split=0.1)

    #traing result
    result = model.evaluate(trainNP,  trainlabelNP)
    print("training accuracy = ", result[1])

    

