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

def init(packets, result_opt):
    #deal with missing
    packets.fillna(value=0, inplace=True)  # fill missing with 0

    if(result_opt == 'attack_cat'):
        packets, attack_cat = prep.seperate_att_lab_catagory(packets)
        #packets, attack_cat = prep.seperate_att_lab_kmeans(packets)
        
        #if we want to do get specfic
        packets = prep.get_imp(packets)

        try: packets = prep.proto_to_value(packets)
        except: pass  
        try: packets = prep.state_to_value(packets)
        except: pass
        try: packets = prep.service_to_value(packets)
        except: pass

        
        #packets, srcip = prep.ip_to_value(packets)
        #print(packets.keys())

        return packets, attack_cat
    elif(result_opt == 'label'):
        packets, label = prep.seperate_att_lab_label(packets)
        #if we want to do get specfic
        packets = prep.get_imp(packets)

        packets = prep.proto_to_value(packets)    
        packets = prep.state_to_value(packets)   
        packets = prep.service_to_value(packets)
        #packets, srcip = prep.ip_to_value(packets)
        return packets, label

    
#create np array for label
def label_to_nparr(label_list):
    """ 
    label_np = []
    onehoten = OneHotEncoder(sparse=False)
    label_np = onehoten.fit_transform(label_list.reshape(-1, 1)).astype(int)
    #print(label_np.shape) 
    """

    #如果原本資料沒有那一類 one hot出來就沒有！！ 
  
    label_np = []
    for i in range(label_list.shape[0]):
        if(label_list[i] == 0):
            label_np.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
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

#create np array for label
def attackcat_to_nparr_specify(label_list):

    label_np = []
    for i in range (label_list.shape[0]):
        x = label_list[i]
        if(x == 4):
            label_np.append([1, 0])
        elif(x == 5):
            label_np.append([0, 1])
        """elif(label_list[i] == 6):
                label_np.append([0, 0, 1, 0])
        elif(label_list[i] == 7):
            label_np.append([0, 0, 0, 1])"""
        
    return label_np


def processed_data(datapath, result_opt):
    data_df = pd.read_csv(datapath, low_memory=False)
    
    if(result_opt == 'attack_cat'):
        data_df, attcat_list = init(data_df, result_opt)
        data_df = prep.del_useless_features(data_df)
        #transforming datatype
        data_df_transtype = prep.trans_datatype(data_df)

        #scaling (data type changes after scaling, i.e. df -> np)
        data_df_scale = prep.feature_scaling(data_df_transtype)

        #create an one-hot list for label list
        attcat_list_oneHot = label_to_nparr(attcat_list)

        #turn dataframe and list to np array
        attcat_np, data_np = np.array(attcat_list_oneHot), np.array(data_df_scale)
        #deal with problem of key 'ct_ftp_cmd'
        
        data_np = prep.np_fillna(data_np)


        return data_np, attcat_np, attcat_list

    elif(result_opt == 'label'):
        data_df, label_list = init(data_df, result_opt)
        data_df = prep.del_useless_features(data_df)
        # ; print(data_df.keys())

        #transforming datatype
        data_df_transtype = prep.trans_datatype(data_df)

        #scaling (data type changes after scaling, i.e. df -> np)
        data_df_scale = prep.feature_scaling(data_df_transtype)

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


