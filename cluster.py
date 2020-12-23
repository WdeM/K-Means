#!/usr/bin/python3
import statistics
import random


# generate random positions for k_clusters
def cluster_positions(cluster_set, min_value, max_value):
    cluster_dicts = []
    cluster_set = [random.randint(min_value,max_value) for n in \
                   range(cluster_set)]
    
    for index, k in enumerate(cluster_set):
        cluster = {"index": index, "base_value": k, "values": [],
                   "avg_distance": 0}
        cluster_dicts.append(cluster)
    return cluster_dicts

def calculate_nearest_cluster(value, cluster_set):
    nearest_cluster = None
    for index,cluster in enumerate(cluster_set):
        if nearest_cluster == None:
            nearest_cluster = index
        elif abs(value-cluster["base_value"])\
           < abs(value - cluster_set[nearest_cluster]["base_value"]):
            nearest_cluster = index
    return nearest_cluster

# find the most optimal center value for each cluster. Values calculated here means
# the centroids that the datapoints are grouped by
def optimize_cluster_set(cluster_set):
    iteration = 0
    last_average_positions = []

    while True:
        iteration += 1
        average_positions = []
        for cluster in cluster_set:
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
                        cluster_set[nearest_cluster]["values"].append(value)
            except:
                pass
        
        # Ugly way for making sure, the centroids aren't moving anymore
        if last_average_positions == average_positions:
            break
        else:
            last_average_positions = average_positions
    return cluster_set

# returns multiple clusters where each cluster centroid has been
# realigned closer to the center of the group based on mean of the group
def generate_cluster_group(set_amount, cluster_amount, dataset, min_value, max_value):
    cluster_group = []
    for i in range(set_amount):
        # generate new cluster positions
        cluster_set = cluster_positions(cluster_amount, min_value, max_value)

        # Assing each value in dataset to the nearest cluster
        for value in dataset:
            nearest_cluster = calculate_nearest_cluster(value,cluster_set)
            cluster_set[nearest_cluster]["values"].append(value)

        # realign centroids to center of its group
        cluster_set = optimize_cluster_set(cluster_set)
        cluster_group.append(cluster_set)
    
    return cluster_group

# return the most optimal clusters from cluster set where the data is most
# evenly distrubeted around the cluster.
def return_best_cluster_set(cluster_group):
    best_cluster_set = {"cluster_set": None, "avg_diff": None}
    for cluster_set in cluster_group:
        # update the average distance for each cluster
        for cluster in cluster_set:
            average_distance = 0
            for value in cluster["values"]:
                average_distance += abs(cluster["base_value"]-value)
            average_distance = average_distance / len(cluster["values"])
            cluster["avg_distance"] = average_distance

        diffs = []
        for i, cluster in enumerate(cluster_set):
            for j, _cluster in enumerate(cluster_set):
                if i != j: 
                    diffs.append(abs(cluster["avg_distance"]-
                                    _cluster["avg_distance"]))
        # average difference between each average_distance, where the smaller
        # the avg_diff is the better the cluster distribution is
        avg_diff = sum(diffs)/len(diffs)
        if best_cluster_set["avg_diff"] == None:
            best_cluster_set["cluster_set"] = cluster_set
            best_cluster_set["avg_diff"] = avg_diff
        elif best_cluster_set["avg_diff"] > avg_diff:
            best_cluster_set["cluster_set"] = cluster_set
            best_cluster_set["avg_diff"] = avg_diff
    return best_cluster_set


if __name__ == "__main__":
    # Create random list of thousand ints between 1 and 10000.
    dataset_size, min_value, max_value = 10000,1,10000
    dataset = [random.randint(min_value,max_value) for n in range(dataset_size)]
    
    # return a set of 10 clusters
    cluster_group = generate_cluster_group(100, 3, dataset, min_value, max_value)
    best_cluster_set = return_best_cluster_set(cluster_group) 
    for cluster in best_cluster_set["cluster_set"]:
        print(cluster["index"],cluster["base_value"],cluster["avg_distance"])
        print(len(cluster["values"]))

    """
    For frame of reference:
    
    - One cluster holds 
        - cluster index
        - cluster centroid value ("base_value")
        - the values nearest this cluster centroid value (data)
        - average distance for values to the cluster centroid    
    - One cluster set holds multiple individual clusters
    - One cluster group holds multiple cluster sets

    Calculate the average distance from each point to the nearest cluster of
    it's group. As the amount of clusters increase, the average distance for
    each datapoint to the nearest cluster should decrease. From this we should
    be able to find the optimal amount of clusters, since there should be a
    point in the curve of average distances for each K value where the amount
    of decrease gets smaller for each K value. "The curve bends".

    """
    




