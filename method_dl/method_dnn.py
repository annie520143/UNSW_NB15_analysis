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


attack_cat_dict = {
                0: 'Nor',       
                1 : 'Fuz', 
                2 : 'Ana',
                3 : 'Bd', 
                4 : 'Dos',
                5 : 'Exp', 
                6 : 'Ge', 
                7 : 'Re', 
                8 : 'Sh',
                9 : 'Worms'
} 

label_dict = {
            0: 'Normal',
            1: 'Attack'
}

#attack_cat = ['Normal', 'Fuzzers', 'Analysis', 'Backdoors', 'DoS', 'Exploits', 'Generic', 'Reconnaissance', 'Shellcode', 'Worms']
attack_cat = ['Nor', 'Fuz', 'Ana', 'Bd', 'Dos', 'Exp', 'Ge', 'Re', 'Sh', 'Worms']

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
def simpleDNN_dropout(feature_dim, atv, loss, output_dim):
    model = Sequential()
    
    model.add(Dense(input_dim=feature_dim, units=64,
        activation = atv)) 
    
    model.add(Dropout(0.1, input_shape=(64,)))

    model.add(Dense(units=32,
        activation = atv)) 
    
    model.add(Dropout(0.1, input_shape=(32,)))

    model.add(Dense(units=16,
        activation = atv)) 
    
    model.add(Dropout(0.1, input_shape=(16,)))

    model.add(Dense(units=output_dim, activation='softmax'))
    opt = Adam(learning_rate=0.01, decay=1e-6)
    model.compile(loss=loss, optimizer=opt, metrics=['accuracy'])

    return model

def matricsDNN(predict, actual, method, dim):
    print("=========================")

    #index and column for the crosstab must have type numpy.ndarray
    cm = pd.crosstab(actual, predict, rownames=['actual'], colnames=['predict'],dropna=False)
    actual_index = cm.columns.tolist()
    predict_index = cm.index.tolist()


    for i in range(dim):
        if(len(predict_index) == dim):
            if(predict_index[i] != i):
                predict_index.insert(i, i)
        elif(len(predict_index) <= dim):
            if(len(predict_index) <= i ):
                predict_index.insert(i, i)
            elif(predict_index[i] != i):
                predict_index.insert(i, i)
        
        #cm = cm[~cm.index.duplicate()]
        cm = cm.reindex(index=predict_index, fill_value=0)

        if(len(actual_index) == dim):
            if(actual_index[i] != i):
                actual_index.insert(i, i)
        elif(len(actual_index) <= dim):           
            if(len(actual_index) <= i):               
                actual_index.insert(i, i)
            elif(actual_index[i] != i):
                actual_index.insert(i, i)
        
        cm = cm.reindex(columns = actual_index, fill_value=0)

    if method == 'attack_cat':
        cm = cm.rename(columns = attack_cat_dict, index = attack_cat_dict)
    elif method == 'label':
        cm = cm.rename(columns = label_dict, index = label_dict)

    #cm.to_csv('./output/cm/cm10.csv')
    print(cm)
    print("=========================") 
    

def detailAccuracyDNN(predict, actual, method, dim):
    n = len(predict)

    total = [0 for i in range(dim)]
    x = [0 for i in range(dim)]
    att_accuracy = 0


    for i, value in enumerate (actual):
        total[value] = total[value]+1

    for i, value in enumerate(predict):
        if(predict[i] == actual[i]):
            x[value] = x[value]+1
    
    attack_n = n - total[0]
    
    if(method == 'attack_cat'):
        for index in range(dim):
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
    
