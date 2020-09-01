import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
"""
Import the Keras libraries and packages
"""
from keras.models import Sequential
from keras.utils import np_utils
from keras.layers import SimpleRNN
from keras.layers.normalization import BatchNormalization
from keras.layers.core import Activation, Dense, Dropout
from keras.layers.recurrent import LSTM
from keras.optimizers import SGD, Adam
#from sklearn.metrics import confusion_matrix

attack_cat_dict = {
                0: 'Nor',       
                1 : 'Fuz', 
                2 : 'Analy', 
                3 : 'Bd', 
                4 : 'DoS', 
                5 : 'Explo', 
                6 : 'Ge', 
                7 : 'Recon', 
                8 : 'Shell', 
                9 : 'Worms'
                }
attack_cat = ['Normal', 'Fuzzers', 'Analysis', 'Backdoors', 'DoS', 'Exploits', 'Generic', 'Reconnaissance', 'Shellcode', 'Worms']

label_dict = {
                0: 'Normal',       
                1: 'Attack'
            }
label = ['Normal', 'Attack']

#DNN model
def simpleDNN(feature_dim, units, atv, loss):
    
    model = Sequential()
    model.add(Dense(input_dim=feature_dim, units=units,
                    activation = atv))
    model.add(BatchNormalization())
    for i in range(10):
        model.add(Dense(units=units-i, activation=atv))
        model.add(BatchNormalization())

    model.add(Dense(units=10, activation='softmax'))
    opt = Adam(learning_rate=0.01, decay=1e-4)
    model.compile(loss=loss, optimizer=opt, metrics=['accuracy'])

    return model


#DNN model with dropout
def simpleDNN_dropout(feature_dim, units, atv, loss, output_dim):
    model = Sequential()

    model.add(Dense(input_dim=feature_dim, units=units,
        activation = atv))
    
    model.add(Dropout(0.1, input_shape=(32,)))
    
    model.add(Dense(input_dim=feature_dim, units=16,
        activation = atv)) 
    
    model.add(Dropout(0.1, input_shape=(16,)))

    """for i in range(3):
        model.add(Dense(units=units-i*2, activation=atv))"""

    model.add(Dense(units=output_dim, activation='softmax'))
    opt = Adam(learning_rate=0.01, decay=1e-6)
    model.compile(loss=loss, optimizer=opt, metrics=['accuracy'])

    return model

#DNN model
def simpleDNN_specify(feature_dim, units, atv, loss, output_dim):
    
    model = Sequential()
    model.add(Dense(input_dim=feature_dim, units=units,
                    activation = atv))
    model.add(BatchNormalization())
    for i in range(10):
        model.add(Dense(units=units-i, activation=atv))
        model.add(BatchNormalization())

    model.add(Dropout(0.2, input_shape=(units-i+1,)))
    model.add(Dense(units=4, activation='softmax'))
    opt = Adam(learning_rate=0.01, decay=1e-4)
    model.compile(loss=loss, optimizer=opt, metrics=['accuracy'])

    return model

""" def matricsDNN(predict, actual):
    matrix_arr = confusion_matrix(actual, predict)
    print(matrix_arr)
 """

def comparePredict(predict, actual, method):
    
    df = pd.DataFrame(columns = ['actual', 'predict'])

    if method == 'attack_cat':
        df['actual'] = actual
        df['predict'] = predict
        df.to_csv('./exp0831/exp1.csv')
        

def matricsDNN(predict, actual, method):
    
    if method == 'attack_cat':
        print("=========================")
        cm = pd.crosstab(actual, predict, rownames=['actual'], colnames=['predict'],dropna=False)
        actual_index = cm.columns.tolist()
        predict_index = cm.index.tolist()
        #print(predict_index, actual_index)

        for i in range(10):
            if(len(predict_index) == 10):
                if(predict_index[i] != i):
                    predict_index.insert(i, i)
            elif(len(predict_index) <= 10):
                if(len(predict_index) <= i ):
                    predict_index.insert(i, i)
                elif(predict_index[i] != i):
                    predict_index.insert(i, i)
            
            #cm = cm[~cm.index.duplicate()]
            cm = cm.reindex(index=predict_index, fill_value=0)

            if(len(actual_index) == 10):
                if(actual_index[i] != i):
                    actual_index.insert(i, i)
            elif(len(actual_index) <= 10):           
                if(len(actual_index) <= i):               
                    actual_index.insert(i, i)
                elif(actual_index[i] != i):
                    actual_index.insert(i, i)
            
            cm = cm.reindex(columns = actual_index, fill_value=0)
       
        cm = cm.rename(columns = attack_cat_dict, index = attack_cat_dict)

        cm.to_csv('cm_1.csv')
        print(cm)
        print("=========================") 




def detailAccuracyDNN(predict, actual, method):
    n = len(predict)
    #bad_index_list = []
    total = [0 for i in range(10)]
    x = [0 for i in range(10)]
    att_accuracy = 0


    for i, value in enumerate (actual):
        total[value] = total[value]+1

    for i, value in enumerate(predict):
        if(predict[i] == actual[i]):
            x[value] = x[value]+1
    
    attack_n = n - total[0]
    #print("attack_cat len:", len(attack_cat))

    if(method == 'attack_cat'):
        for index in range(10):
            print("==========================")
            
            print(index, attack_cat[index], ': ','predict: ', x[index], 'total: ', total[index])
            try:
                acc = x[index]/total[index]       
            except ZeroDivisionError:
                acc = 0.0
                
            print("acc: ", acc)
            rate = total[index]/attack_n
            if index != 0:
                att_accuracy = att_accuracy + rate*acc
        
        print("=============================")
        print('attack accuracy: ', att_accuracy)

        
    elif(method == 'label'):
        for index in range(2):
            print("==========================")
            print(index, label[index],': ', 'predict: ', x[index], 'total: ', total[index])
            try:
                print("acc: ", x[index]/total[index])
            except ZeroDivisionError:
                print("acc: ", 0.0)

    ("==========================")
    
