import numpy as np
import pandas as pd
import sys

#keras
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.models import load_model
from sklearn.preprocessing import OneHotEncoder

#preprocessing
import preprocessing as prep

#DNN Method
import method_dnn as method 


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
    
    packets.fillna(value=0, inplace=True)

    packets, attackCat, label = prep.SeperateAttackLabel(packets)

    packets = prep.GetImp(packets,imp_features)
    packets = prep.FeatureOneHot(packets)
    #transforming datatype
    packets = prep.TransDatatype(packets)
    #scaling (data type changes after scaling, i.e. df -> np)
    packetScaled = prep.FeatureScaling(packets)

    if(opt == "attack_cat"):
        
        attackCatOneHot = CategoryOneHot(attackCat,opt)       
        attackCatNP, packetsNP = np.array(attackCatOneHot), np.array(packetScaled)
        packetsNP = prep.NpFillna(packetsNP)
        return packetsNP, attackCatNP, attackCat

    elif(opt == "label"):
        labelOneHot = CategoryOneHot(label, opt)
        labelNP, packetsNP= np.array(labelOneHot), np.array(packetScaled)
        packetsNP = prep.NpFillna(packetsNP)
        return packetsNP, labelNP, label



def info():
    print('Basic info:')
    print('training dataset:', trainPath)
    print('testing dataset: ', testPath)
    print('model: ', usedModelPath)
    print('===================================')


trainPath = "../dataset/1_0-1_mix_time.csv"
testPath = "../dataset/1_1-2_mix_time.csv"

opt = 'attack_cat'  
newModelName = 'seldef'

reTrain = True
usedModelPath = 'model/dnn_selfdef1_random.h5'

# all feature, except srcip dstip
all_features = ['sport', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'service', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime','Sintpkt', 'Dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attackCat', 'Label']

imp_features = ['sport', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'service', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attackCat', 'Label']


if __name__ == "__main__":

    
    #label depends on expected_output
    trainNP, trainlabelNP, trainlabelList = ProcessData(trainPath, opt)
    testNP, testlabelNP, testlabelList = ProcessData(testPath, opt)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    dataset_size = trainNP.shape[0]  # how many data
    feature_dim = trainNP.shape[1]  # how mant features
    output_dim = trainlabelNP.shape[1]

        
    if(reTrain):
        # simpleDNN_dropout(feature_dim, atv, loss, output_dim)
        if(opt == 'label'):
            model = method.simpleDNN_dropout(feature_dim, 'relu', 'mse', output_dim)
        elif(opt == 'attack_cat'):
            model = method.simpleDNN_dropout(
                feature_dim, 'relu', 'mse', output_dim)

        usedModelPath = 'model/dnn_' + newModelName + '.h5'
        model.save(usedModelPath)

        #csv_logger = CSVLogger('dnn_' + newModelName+ '.log')

    # Setting callback functions
    checkpoint = ModelCheckpoint(filepath=usedModelPath,
                                verbose=1,
                                save_best_only=True,
                                monitor='accuracy',
                                mode='max')
    earlystopping = EarlyStopping(monitor='accuracy',
                                patience=10,
                                verbose=1,
                                mode='max')


    model = load_model(usedModelPath)


    #training
    model.fit(trainNP, trainlabelNP, batch_size=100, epochs=100, callbacks=[earlystopping, checkpoint], shuffle=True)

    #traing result
    result = model.evaluate(trainNP,  trainlabelNP)
    print("training accuracy = ", result[1])
    
    #testing result
    result = model.evaluate(testNP,  testlabelNP)
    print("testing accuracy = ", result[1])
    
    #predict result
    predictLabel = np.argmax(model.predict(testNP), axis=1)
    
    method.matricsDNN(predictLabel, testlabelList, opt, output_dim)
    method.detailAccuracyDNN(predictLabel, testlabelList, opt, output_dim)



