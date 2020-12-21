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

# find the most optimal center value for each cluster. Values calculated here means
# the centroids that the datapoints
def find_cluster_centers(clusters):
    iteration = 0
    last_average_positions = []

    while True:
        iteration += 1
        average_positions = []
        for cluster in clusters:
            try:
                # Calculate mean from the assinged values in the cluster and use it as a new
                # base value
                average_position = int(sum(cluster["values"]) / len(cluster["values"]))
                average_positions.append(average_position)
                cluster.update({"base_value" : average_position})

                # Go through each value in each cluster and see if it still belongs to that
                # cluster and if not, assinged it to the accurate cluster
                for value in cluster["values"]:
                    nearest_cluster = calculate_nearest_cluster(value, clusters)
                    if nearest_cluster != cluster["cluster_index"]:
                        cluster["values"].remove(value)
                        clusters[nearest_cluster]["values"].append(value)
            except:
                pass
        
        # Ugly way for making sure, the centroids aren't moving anymore
        if last_average_positions == average_positions:
            break
        else:
            last_average_positions = average_positions

    return clusters


if __name__ == "__main__":
    # Create random list of thousand ints between 1 and 10000.
    dataset_size, min_value, max_value = 10000,1,10000
    dataset = [random.randint(min_value,max_value) for n in range(dataset_size)]
    
    # generate n of k-clusters and initiate cluster objects (dicts)
    cluster_amount = 3
    clusters = cluster_positions(cluster_amount, 1, 10000)
    
    # Assing each value in dataset to the nearest cluster
    for value in dataset:
        nearest_cluster = calculate_nearest_cluster(value,clusters)
        clusters[nearest_cluster]["values"].append(value)
    
    clusters = find_cluster_centers(clusters) 

    for cluster in clusters:
        print("\nCluster index : " + str(cluster["cluster_index"]))
        print("Best cluster position : " + str(cluster["base_value"]))
        print("Amount of data : " + str(len(cluster["values"])))



