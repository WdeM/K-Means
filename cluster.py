#!/usr/bin/python3
import random


def create_random_list(amount, min_value, max_value):
    random_numbers = [random.randint(min_value,max_value) for n in range(amount)]
    return tuple(random_numbers)

# generate random positions for k_clusters
def cluster_positions(k_clusters, min_value, max_value):
    cluster_set = dict()
    k_clusters = [random.randint(min_value,max_value) for n in range(k_clusters)]
    for k in k_clusters:
        cluster_set[k] = []
    return cluster_set

def calculate_nearest_cluster(value, cluster_set):
    nearest_cluster = None
    for cluster in cluster_set:
        if nearest_cluster == None:
            nearest_cluster = cluster
        elif abs(value-cluster) < abs(nearest_cluster-value):
            nearest_cluster = cluster
    return nearest_cluster


if __name__ == "__main__":
    # Create random list of thousand ints between 1 and 1000.
    dataset = create_random_list(1000, 1, 1000)
    
    # generate two k-clusters
    amount_of_clusters = 2
    clusters = cluster_positions(amount_of_clusters, 1, 1000)

    for value in dataset:
        nearest_cluster = calculate_nearest_cluster(value,clusters)
        clusters[nearest_cluster].append(value)
