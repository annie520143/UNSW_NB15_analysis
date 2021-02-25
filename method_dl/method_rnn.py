import numpy as np
import pandas as pd
"""
Import the Keras libraries and packages
"""
from keras.models import Sequential
from keras.utils import np_utils
from keras.layers import SimpleRNN
from keras.layers.core import Activation, Dense, Dropout
from keras.layers.recurrent import LSTM
from keras.optimizers import SGD, Adam
import keras.layers.advanced_activations
""" 
Scaling
"""
from sklearn.preprocessing import MinMaxScaler
import preprocessing as prep

attack_cat = ['Normal', 'Fuzzers', 'Analysis', 'Backdoors', 'Dos', 'Exploits', 'Generic', 'Reconnaissance', 'Shellcode', 'Worms']

def defRNN(data, label, group_num):
    X, y = [], []
    n = group_num  # n packets per group
    

    for i in range(data.shape[0] - n):
        X.append(data[i:i+n])  # i - i+n-1
        y.append(label[i+n-1])  # i+n-1


    X = np.array(X)
    y = np.array(y)


    return X, y


#RNN model
def simpleRNN(feature_dim, atv, loss, output_dim):
    model = Sequential()
    model.add(LSTM(100,  return_sequences=True,input_shape=feature_dim))
    model.add(LSTM(100))
    #model.add(Dense(80))
    model.add(Dense(15))
    model.add(Dense(15))
    model.add(Dense(units=output_dim, kernel_initializer='uniform', activation=atv))

    adam = Adam(0.00006)

    model.compile(loss=loss, optimizer=adam, metrics=['accuracy'])
    

    return model


def metricsRNN(predict, actual):

    print("==========================")
    confusion_metrics = pd.crosstab(actual, predict, rownames=['label'], colnames=['predict'])
    print(confusion_metrics)
    print("==========================")

#RNN details
def detailAccuracyRNN(predict, actual, method):
    
    n = len(predict)
    bad_index_list = []
    total = [0 for i in range(10)]
    x = [0 for i in range(10)]


    for i, value in enumerate (actual):
        total[value] = total[value]+1

    for i, value in enumerate(predict):
        if(predict[i] == actual[i]):
            x[value] = x[value]+1

    if(method == 'attack_cat'):
        for index in range(10):
            print("==========================")
            print(index, attack_cat[index], ': ','predict: ', x[index], 'total: ', total[index])
            try:
                print("acc: ", x[index]/total[index])
            except ZeroDivisionError:
                print("acc: ", 0.0)
    elif(method == 'label'):
        for index in range(2):
            print("==========================")
            print(index, ': ', 'predict: ', x[index], 'total: ', total[index])
            try:
                print("acc: ", x[index]/total[index])
            except ZeroDivisionError:
                print("acc: ", 0.0)


    print("=========================")

    

    """for i in range(len(predict)):
        if (actual[i] == 0) & (predict[i] == 0):
            G_G = G_G+1

        elif (actual[i] == 0) & (predict[i] == 1):
            G_B = G_B+1

        elif (actual[i] == 1) & (predict[i] == 0):
            B_G = B_G+1

        elif (actual[i] == 1) & (predict[i] == 1):
            B_B = B_B+1
            #must return its index for the usage in iptable
            bad_index_list.append(i)"""

    
    """print("===========================")
    print("predict right:")
    print("Good to Good: ", G_G/n)
    print("Bad to Bad: ", B_B/n)
    print("===========================")
    print("predict wrong:")
    print("Good to Bad: ", G_B/n)
    print("Bad to Good: ", B_G/n)"""
    
    
    return bad_index_list
