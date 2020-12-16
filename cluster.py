#!/usr/bin/python3
import random


# generate random positions for k_clusters
def cluster_positions(k_clusters, min_value, max_value):
    cluster_dicts = []
    k_clusters = [random.randint(min_value,max_value) for n in range(k_clusters)]
    for index, k in enumerate(k_clusters):
        cluster = {"cluster_index": index, "base_value": k, "values": []}
        cluster_dicts.append(cluster)
    return cluster_dicts

def calculate_nearest_cluster(value, clusters):
    nearest_cluster = None
    for index,cluster in enumerate(clusters):
        if nearest_cluster == None:
            nearest_cluster = index
        elif abs(value-cluster["base_value"])\
           < abs(value - clusters[nearest_cluster]["base_value"]):
            nearest_cluster = index
    return nearest_cluster


if __name__ == "__main__":
    # Create random list of thousand ints between 1 and 1000.
    dataset_size, min_value, max_value = 10000,1,10000
    dataset = [random.randint(min_value,max_value) for n in range(dataset_size)]
    
    # generate n of k-clusters and initiate cluster objects (dicts)
    cluster_amount = 3
    clusters = cluster_positions(cluster_amount, 1, 1000)
    
    # Assing each value in dataset to the nearest cluster
    for value in dataset:
        nearest_cluster = calculate_nearest_cluster(value,clusters)
        clusters[nearest_cluster]["values"].append(value)
    
    # Calculate mean from the assinged values in the cluster and use it as a new
    # base value
    for cluster in clusters:
        try:
            average_position = int(sum(cluster["values"]) / len(cluster["values"]))
            cluster.update({"base_value" : average_position})
        except:
            pass
    
    # Go through each value in each cluster and see if it still belongs to that
    # cluster and if not, assinged it to the accurate cluster
    for cluster in clusters:
        for value in cluster["values"]:
            nearest_cluster = calculate_nearest_cluster(value, clusters)
            if nearest_cluster != cluster["cluster_index"]:
                cluster["values"].remove(value)
                clusters[nearest_cluster]["values"].append(value)

    for cluster in clusters:
        print("Cluster index : " + str(cluster["cluster_index"]))
        print("Base value : " + str(cluster["base_value"]))
        print("Amount of data : " + str(len(cluster["values"])))



