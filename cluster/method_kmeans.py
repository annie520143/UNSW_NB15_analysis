from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.pyplot as plt


def Elbow(packets):
    sum_of_squared_dis = []
    K = range(1, 10)  # origin -> 1, 10
    for k in K:
        model = KMeans(n_clusters=k)
        km = model.fit(packets)
        sum_of_squared_dis.append(km.inertia_)  # SSE

    # Plot the elbow
    plt.plot(K, sum_of_squared_dis, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k')
    plt.show()


def Silh(packets):
    silhouette_avg = []
    K = range(2, 20)
    for k in K:
        model = KMeans(n_clusters=k)
        km = model.fit(packets)
        silhouette_avg.append(silhouette_score(packets, km.labels_))

    #Plot
    plt.plot(range(2, 20), silhouette_avg)
    plt.show()

    #return max(silhouette_avg)  # parameter(k) of Kmeans_silh_fixed_size(k)


def Silh_fixed_size(packets, k):
    # global group_number
    model = KMeans(n_clusters=k)
    km = model.fit(packets)

    group_number_list = km.labels_

    max_label = 0
    for label in group_number_list:
        if label > max_label:
            max_label = label

    return max_label, group_number_list
    """
    c_info.packets_in_cluster(km.labels_, max_label+1)

    for i in range(max_label+1):
        c_info.print_cluster(pkt, km.labels_, i) 
    """
