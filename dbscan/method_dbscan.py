from sklearn.cluster import DBSCAN
import numpy as np
import scipy as sp
import sys


def DBscan_fixed_eps(packets, eps):
    model = DBSCAN(eps=eps, min_samples=5)
    dbscan = model.fit(packets)
    np.set_printoptions(threshold=sys.maxsize)  # ???

    group_number_list = dbscan.labels_

    max_label = 0
    for label in group_number_list:
        if label > max_label:
            max_label = label

    for i in range(max_label):



    #max_label + 1 -> 分幾群
    #print(dbscan.components_)

    return dbscan, max_label, group_number_list
    #dbscan -> model, max_label -> how many groups, group_number_list -> label for each instance


def DBscan_predict(packets_test, eps, dbscan):

    metric = sp.spatial.distance.cosine

    #unclassfied points first go into outlier
    label_test = np.ones(len(packets_test.index), dtype=int)*(-1)

    for j, test in enumerate(packets_test.to_numpy()):
        for i, core in enumerate(dbscan.components_):
            #print(test)
            if sp.spatial.distance.cosine(test, core) < eps:
                label_test[j] = dbscan.labels_[dbscan.core_sample_indices_[i]]
                break

    return label_test


def DBscan_score(label_test, label_actual):

    score = []

    for i in range(len(label_test)):

        lab0 = label_actual[i]
        lab1 = label_test[i]

        #malicious packets and dbscan outlier ( predict as malicious)
        if (lab0 == 1) & (lab1 == -1):
            score.append(1)

        #malicious packets and dbscan inlier ( predict as normal)
        elif (lab0 == 1) & (lab1 != -1):
            score.append(0)

        #normal packets and dbscan outlier ( predict as malicious)
        elif (lab0 == 0) & (lab1 == -1):
            score.append(0)

        #normal packets and dbscan inlier ( predict as normal)
        elif (lab0 == 0) & (lab1 != -1):
            score.append(1)

    print(score)
