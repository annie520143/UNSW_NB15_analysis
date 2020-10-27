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
from sklearn.preprocessing import OneHotEncoder

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

#create np array for label
def categoryOneHot(label, opt): 
    
    cat_n = 2 if(opt == 'label') else 10
    label_np = []

    for i in range(label.shape[0]):      
        for index in range(cat_n):
            if(label[i] == index):
                a = [0]*cat_n
                a[index] = 1
                label_np.append(a)

    label_np = np.array(label_np)
    return label_np




def processed_data(datapath, opt):
    
    packets = pd.read_csv(datapath, low_memory=False)
    

    packets.fillna(value=0, inplace=True)

    packets, attack_cat = prep.seperate_att_lab_catagory(packets)

    packets = prep.get_imp(packets)

    try: packets = prep.proto_to_value(packets)
    except: pass  
    try: packets = prep.state_to_value(packets)
    except: pass
    try: packets = prep.service_to_value(packets)
    except: pass

    #transforming datatype
    packets = prep.trans_datatype(packets)

    #scaling (data type changes after scaling, i.e. df -> np)
    packetScaled = prep.feature_scaling(packets)

    #create an one-hot list for label list
    attcatOneHot = categoryOneHot(attack_cat,opt)

    #turn dataframe and list to np array
    attcat_np, packets_np = np.array(attcatOneHot), np.array(packetScaled)
        
    #deal with problem of key 'ct_ftp_cmd'
    packets_np = prep.np_fillna(packets_np)

    return packets_np, attcat_np, attack_cat

def info():
    print('Basic info:')
    print('training dataset:', train_path)
    print('testing dataset: ', test_path)
    print('model: ', used_model)
    print('===================================')


train_path = "../dataset/test_balance.csv"
test_path = "../dataset/1_10-18_mix_time.csv"

expected_output = 'attack_cat'
used_model = 'model/dnn_selfdef1_random.h5'


if __name__ == "__main__":


    #label depends on expected_output
    train_np, trainlabel_np, trainlabel_list = processed_data(train_path, expected_output)
    test_np, testlabel_np, testlabel_list = processed_data(test_path, expected_output)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    dataset_size = train_np.shape[0]  # how many data
    feature_dim = train_np.shape[1] # how mant features
    output_dim = trainlabel_np.shape[1]

    print(output_dim)
    

    # simpleDNN_dropout(feature_dim, units, atv, loss)
    if(expected_output == 'label'):
        model = method.simpleDNN_dropout(feature_dim, 32, 'relu', 'mse', output_dim)
    elif(expected_output == 'attack_cat'):
        model = method.simpleDNN_dropout(feature_dim, 32, 'relu', 'mse', output_dim)

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
    model.fit(train_np, trainlabel_np, batch_size=100, epochs=100, callbacks=[earlystopping, checkpoint, csv_logger], shuffle=True)
    #model.fit(train_np, trainlabel_np, batch_size=100, epochs=10, shuffle=True)

    result = model.evaluate(train_np,  trainlabel_np)
    print("training accuracy = ", result[1])
   

    model = ks.load_model(used_model)
    #print(model.summary())
    
    result = model.evaluate(test_np,  testlabel_np)
    print("testing accuracy = ", result[1])
    
    predictLabel = model.predict_classes(test_np)
    #shape(1 * dataset_size)
    np.set_printoptions(threshold=sys.maxsize)

    method.matricsDNN(predictLabel, testlabel_list, expected_output, output_dim)
    method.detailAccuracyDNN(predictLabel, testlabel_list, expected_output, output_dim)
    #method.comparePredict(test_path, predictLabel, testlabel_list, expected_output )


