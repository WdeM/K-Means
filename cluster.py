#!/usr/bin/python3
import statistics
import random


# generate random positions for k_clusters
def cluster_positions(clusters, min_value, max_value):
    cluster_dicts = []
    clusters = [random.randint(min_value,max_value) for n in range(clusters)]
    for index, k in enumerate(clusters):
        cluster = {"index": index, "base_value": k, "values": [],
                   "avg_distance": 0}
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
# the centroids that the datapoints are grouped by
def optimize_clusters(clusters):
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
                    if nearest_cluster != cluster["index"]:
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

# returns multiple clusters where each cluster centroid has been
# realigned closer to the center of the group based on mean of the group
def generate_cluster_set(set_amount, cluster_amount, dataset, min_value, max_value):
    cluster_set = []
    for i in range(set_amount):
        # generate new cluster positions
        clusters = cluster_positions(cluster_amount, min_value, max_value)

        # Assing each value in dataset to the nearest cluster
        for value in dataset:
            nearest_cluster = calculate_nearest_cluster(value,clusters)
            clusters[nearest_cluster]["values"].append(value)

        # realign centroids to center of its group
        clusters = optimize_clusters(clusters)
        cluster_set.append(clusters)
    
    return cluster_set

# return the most optimal clusters from cluster set where the data is most
# evenly distrubeted around the cluster.
def return_best_clusters(cluster_set):
    best_clusters = {"clusters": None, "avg_diff": None}
    for clusters in cluster_set:
        # update the average distance for each cluster
        for cluster in clusters:
            average_distance = 0
            for value in cluster["values"]:
                average_distance += abs(cluster["base_value"]-value)
            average_distance = average_distance / len(cluster["values"])
            cluster["avg_distance"] = average_distance

        diffs = []
        for i, cluster in enumerate(clusters):
            for j, _cluster in enumerate(clusters):
                if i != j: 
                    diffs.append(abs(cluster["avg_distance"]-
                                    _cluster["avg_distance"]))
        # average difference between each average_distance, where the smaller
        # the avg_diff is the better the cluster distribution is
        avg_diff = sum(diffs)/len(diffs)
        if best_clusters["avg_diff"] == None:
            best_clusters["clusters"] = clusters
            best_clusters["avg_diff"] = avg_diff
        elif best_clusters["avg_diff"] > avg_diff:
            best_clusters["clusters"] = clusters
            best_clusters["avg_diff"] = avg_diff
    return best_clusters


if __name__ == "__main__":
    # Create random list of thousand ints between 1 and 10000.
    dataset_size, min_value, max_value = 10000,1,10000
    dataset = [random.randint(min_value,max_value) for n in range(dataset_size)]
    
    # return 10 cluster sets
    cluster_set = generate_cluster_set(10, 5, dataset, min_value, max_value)
    best_clusters = return_best_clusters(cluster_set) 
    for cluster in best_clusters["clusters"]:
        print(cluster["index"],cluster["base_value"],cluster["avg_distance"])
        print(len(cluster["values"]))

    """
    For frame of reference:
    
    - One cluster holds 
        - cluster index
        - cluster centroid value ("base_value")
        - the values nearest this cluster centroid value (data)
    
    - Clusters object holds multiple cluster objects, where the amount is
      defined by the amount of cluster used for the overall dataset

    - Cluster_set holds multiple clusters

    Calculate the average distance from each point to the nearest cluster of
    it's group. As the amount of clusters increase, the average distance for
    each datapoint to the nearest cluster should decrease. From this we should
    be able to find the optimal amount of clusters, since there should be a
    point in the curve of average distances for each K value where the amount
    of decrease gets smaller for each K value. "The curve bends".

    """
    




