import numpy as np
import pandas as pd
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

attack_cat = ['Normal', 'Fuzzers', 'Analysis',
'Backdoors', 'DoS', 'Exploits', 'Generic', 'Reconnaissance', 'Shellcode', 'Worms']

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
    
    model.add(Dropout(0.2, input_shape=(32,)))
    
    model.add(Dense(input_dim=feature_dim, units=16,
        activation = atv)) 
    
    model.add(Dropout(0.2, input_shape=(16,)))

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


def metricsDNN(predict, actual):
    print(predict.shape)
    print(actual.shape)
    print("=========================")
    confusion_metrics = pd.crosstab(actual, predict, rownames=['label'], colnames=['predict'])
    print(confusion_metrics)
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
            print(index, ': ', 'predict: ', x[index], 'total: ', total[index])
            try:
                print("acc: ", x[index]/total[index])
            except ZeroDivisionError:
                print("acc: ", 0.0)

    ("==========================")
    
