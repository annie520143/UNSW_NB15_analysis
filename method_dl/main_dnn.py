import numpy as np
import pandas as pd
import sys

#keras
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from keras.models import Sequential
import keras.models as ks
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
    

    packets = prep.GetImp(packets)
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
    print('model: ', usedModel)
    print('===================================')


trainPath = "../dataset/1_0-1_mix_time.csv"
testPath = "../dataset/1_1-2_mix_time.csv"

opt = 'attack_cat'
usedModel = 'model/dnn_selfdef1_random.h5'


if __name__ == "__main__":


    #label depends on expected_output
    trainNP, trainlabelNP, trainlabelList = ProcessData(trainPath, opt)
    testNP, testlabelNP, testlabelList = ProcessData(testPath, opt)
    

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    dataset_size = trainNP.shape[0]  # how many data
    feature_dim = trainNP.shape[1] # how mant features
    output_dim = trainlabelNP.shape[1]


    # simpleDNN_dropout(feature_dim, units, atv, loss)
    if(opt == 'label'):
        model = method.simpleDNN_dropout(feature_dim, 32, 'relu', 'mse', output_dim)
    elif(opt == 'attack_cat'):
        model = method.simpleDNN_dropout(feature_dim, 32, 'relu', 'mse', output_dim)

    # Setting callback functions
    csv_logger = CSVLogger('training.log')

    checkpoint = ModelCheckpoint(filepath=usedModel,
                                verbose=1,
                                save_best_only=True,
                                monitor='accuracy',
                                mode='max')
    earlystopping = EarlyStopping(monitor='accuracy',
                                patience=10,
                                verbose=1,
                                mode='max')
    
    #training
    model.fit(trainNP, trainlabelNP, batch_size=100, epochs=100, callbacks=[earlystopping, checkpoint, csv_logger], shuffle=True)
   
    #traing result
    result = model.evaluate(trainNP,  trainlabelNP)
    print("training accuracy = ", result[1])

    model = ks.load_model(usedModel)
    #print(model.summary())
    
    #testing result
    result = model.evaluate(testNP,  testlabelNP)
    print("testing accuracy = ", result[1])
    
    #predict result
    predictLabel = model.predict_classes(testNP)
    
    method.matricsDNN(predictLabel, testlabelList, opt, output_dim)
    method.detailAccuracyDNN(predictLabel, testlabelList, opt, output_dim)
    #method.comparePredict(test_path, predictLabel, testlabelList, expected_output )

    #np.set_printoptions(threshold=sys.maxsize)



