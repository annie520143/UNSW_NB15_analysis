import pandas as pd

def packets_in_cluster(labels, n):

    packets_num = [0]*n
    for label in labels:
        if (label != -1):
            packets_num[label] = packets_num[label] + 1
    print('number of packets in each cluster: ', packets_num)


#Get what's in every cluster
def print_cluster(pkt, labels, cluster_index):
    print_list = []
    label_list = []
    att_cat_list = []
    timestamp_list = []
    index_list = []

    num = 0

    #cal accuracy ratio
    sum_label_0 = 0
    sum_label_1 = 0
    for i in range(len(labels)):
        label = labels[i]

        if label == cluster_index:
            print_list.append(list(pkt.iloc[i, :]))
            label_list.append(pkt['Label'].loc[i])

            if(pkt['Label'].loc[i] == 0):
                sum_label_0 += 1
            elif(pkt['Label'].loc[i] == 1):
                sum_label_1 += 1

            att_cat_list.append(pkt['attack_cat'].loc[i])
            timestamp_list.append(pkt['Stime'].loc[i])
            index_list.append(i)
            num = num+1

    ratio0 = (sum_label_0) / (sum_label_0 + sum_label_1)
    ratio1 = (sum_label_1) / (sum_label_0 + sum_label_1)
    print_df = pd.DataFrame(print_list, columns=pkt.keys())
    print_df['index'] = index_list
    print(cluster_index, ':')
    print(index_list)
    print(label_list)
    print(att_cat_list)
    print('ratio0: ', ratio0, ' ratio1: ', ratio1)
    #print(timestamp_list)
    pd.set_option('display.max_rows', None)

    #print(print_df)

def print_outlier(pkt, labels):
    
    outlier_info =[]
    index_info = []

    for i in range(len(labels)):
        label = labels[i]
        if label == -1:
            outlier_info.append(list(pkt.iloc[i, :]))
            index_info.append(i)

    outlier_df = pd.DataFrame(outlier_info, columns= pkt.keys())
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(index_info)
    print(outlier_df)
