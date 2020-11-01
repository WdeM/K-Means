#!/usr/bin/python3
import random


def create_random_list(amount, min_value, max_value):
    random_numbers = [random.randint(min_value,max_value) for n in range(amount)]
    return tuple(random_numbers)

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
        elif abs(value-cluster["base_value"]) < abs(nearest_cluster-value):
            nearest_cluster = index
    return nearest_cluster

def mean(lst):
    try:
        return int(sum(lst) / len(lst))
    except:
        return None


if __name__ == "__main__":
    # Create random list of thousand ints between 1 and 1000.
    dataset_size, min_value, max_value = 1000,1,1000
    dataset = create_random_list(dataset_size, min_value, max_value)
    
    # generate n of k-clusters and initiate cluster objects (dicts)
    amount_of_clusters = 10
    clusters = cluster_positions(amount_of_clusters, 1, 1000)
    
    # Assing each value in dataset to the nearest cluster
    for value in dataset:
        nearest_cluster = calculate_nearest_cluster(value,clusters)
        clusters[nearest_cluster]["values"].append(value)
    
    # Calculate mean from the assinged values in the cluster and use it as a new
    # base value
    for cluster in clusters:
        average_position = mean(cluster["values"])
        if average_position != None:
            cluster.update({"base_value" : average_position})

    print(clusters) 
