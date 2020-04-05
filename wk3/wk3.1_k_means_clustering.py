################################
# Week 3.1: k-means clustering #
################################
# importing libraries
import random # library for random numbers generator
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.datasets.samples_generator import make_blobs

#print('libraries imported')

##############################################
# 1. k-means on a Randomly Generated Dataset #
##############################################

# 30 different points, belonging to two clusters

# data
x1 = [-4.9, -3.5, 0, -4.5, -3, -1, -1.2, -4.5, -1.5, -4.5, -1, -2, -2.5, -2, -1.5, 4, 1.8, 2, 2.5, 3, 4, 2.25, 1, 0, 1, 2.5, 5, 2.8, 2, 2]
x2 = [-3.5, -4, -3.5, -3, -2.9, -3, -2.6, -2.1, 0, -0.5, -0.8, -0.8, -1.5, -1.75, -1.75, 0, 0.8, 0.9, 1, 1, 1, 1.75, 2, 2.5, 2.5, 2.5, 2.5, 3, 6, 6.5]

# checking length to confirm 30 elements
# print(len(x1))
# print(len(x2))

# print('Datapoints defined!')

# defining function for assigning clusters
colors_map = np.array(['b', 'r'])
def assign_members(x1, x2, centers):
    compare_to_first_center = np.sqrt(np.square(np.array(x1) - centers[0][1]) + np.square(np.array(x2) - centers[0][1]))
    compare_to_second_center = np.sqrt(np.square(np.array(x1) - centers[0][1]) + np.square(np.array(x2) - centers[0][1]))
    class_of_points = compare_to_first_center > compare_to_second_center
    colors = colors_map[class_of_points + 1 - 1]
    return colors, class_of_points

#print('assign_members function defined!')

# defining a function that recalculates and reassigns centroids
# update means
def update_centers(x1, x2, class_of_points):
    center1 = [np.mean(np.array(x1)[~class_of_points]), np.mean(np.array(x2)[~class_of_points])]
    center2 = [np.mean(np.array(x1)[class_of_points]), np.mean(np.array(x2)[class_of_points])]
    return [center1, center2]

#print('assign_members function defined!')

# defining a function to plot clusters and centroids
def plot_points(centroids=None, colors='g', figure_title=None):
    # plotting the figure
    fig = plt.figure(figsize=(15,10))
    ax = fig.add_subplot(1, 1, 1)

    centroid_colors = ['bx', 'rd']
    if centroids:
        for (i, centroid) in enumerate(centroids):
            ax.plot(centroid[0], centroid[1], centroid_colors[i], markeredgewidth=5, markersize=20)
    plt.scatter(x1, x2, s=500, c=colors)

    # defining the ticks
    xticks = np.linspace(-6, 8, 15, endpoint=True)
    yticks = np.linspace(-6, 6, 13, endpoint=True)

    # fixing the horizontal axis
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)

    # add tick labels
    xlabels = xticks
    ax.set_xticklabels(xlabels)
    ylabels = yticks
    ax.set_yticklabels(ylabels)

    # style the ticks
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params('both', length=2, width=1, which='major', labelsize=15)

    # add labels to axes
    ax.set_xlabel('x1', fontsize=20)
    ax.set_ylabel('x2', fontsize=20)

    # add title to figure
    ax.set_title(figure_title, fontsize=24)

    plt.show()

# print('plot_points function defined!')

# initializing k means data points
#plot_points(figure_title='Scatter Plot of x2 vs x1')

# initializing k means - arbitrarily defining clusters
centers = [[-2,2], [2,-2]]
#plot_points(centers, figure_title='k-means Initialization')

# running 4 iterations
# number_of_iterations = 4
# for i in range(number_of_iterations):
#     input('Iteration {} - Press Enter to update the members of each cluster'.format(i + 1))
#     colors, class_of_points = assign_members(x1, x2, centers)
#     title = 'Iteration {} - Cluster Assignment'.format(i + 1)
#     plot_points(centers, colors, figure_title=title)
#     input('Iteration {} - Press Enter to update the centers'.format(i + 1))
#     centers = update_centers(x1, x2, class_of_points)
#     title = 'Iteration {} - Centroid Update'.format(i + 1)
#     plot_points(centers, colors, figure_title=title)

# generating the data
np.random.seed(0)

# feature matrix
X, y = make_blobs(n_samples=5000, centers=[[4,4], [-2,-1], [2,-3], [1,1]], cluster_std=0.9)

plt.figure(figsize=(15,10))
plt.scatter(X[:,0], X[:,1], marker='.')
# plt.show()

# Setting up k-means

# output parameter
k_means = KMeans(init="k-means++", n_clusters=4, n_init=12)

# fitting model
k_means.fit(X)

# labelling each point
k_means_labels = k_means.labels_
k_means_labels

# also pulling cluster centers
k_means_cluster_centers = k_means.cluster_centers_
k_means_cluster_centers

# Visualizing Cluster Results

# initializing plot, plus dimensions
fig = plt.figure(figsize=(15,10))

# using colors to differentiate clustering levels
colors = plt.cm.Spectral(np.linspace(0, 1, len(set(k_means_labels))))

# create a plot
ax = fig.add_subplot(1, 1, 1)

# looping through, to plot clusters
# k range is 1 to 3, for 3 clusters
for k, col in zip(range(len([[4,4], [-2, -1], [2, -3], [1, 1]])), colors):

    # listing datapoints, marking ones in cluster as true
    # and ones outside cluster as false
    my_members = (k_means_labels == k)

    # assigning the cluster centroid
    cluster_center = k_means_cluster_centers[k]

    # using color maps for clusters
    ax.plot(X[my_members, 0], X[my_members, 1], 'w', markerfacecolor=col, marker='.')

    # plotting centroids with a darker outline than cluster points
    ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)

# titling plot
ax.set_title('Kmeans')

# removing x axis ticks
ax.set_xticks(())

# removing y axis ticks
ax.set_yticks(())

# displaying plot
# plt.show()

###########################################################
# 2. Applying K-means clustering to customer segmentation #
###########################################################
import wget

# downloading csv
url = "https://cocl.us/customer_dataset"
# wget.download(url, 'customer_segmentation.csv')

# print('data downloaded')

# converting to a dataframe
customers_df = pd.read_csv('customer_segmentation.csv')
customers_df.head()

# Getting ready for pre-processing.
# clustering only applies to numeric vars
df = customers_df.drop('Address', axis=1)
df.head()

# normalization to help interpretability across features
from sklearn.preprocessing import StandardScaler

X = df.values[:,1:] # assigning dataframe values
X = np.nan_to_num(X) # transforming
cluster_dataset = StandardScaler().fit_transform(X)
print(cluster_dataset)

# modeling
num_clusters = 3

k_means = KMeans(init="k-means++", n_clusters=num_clusters, n_init=12)
k_means.fit(cluster_dataset)
labels = k_means.labels_

print(labels)

# insights drawn

# every row / customer is assigned a label / cluster
df["Labels"] = labels
print(df.head(5))

# averaging cluster features, to check centroid
print(df.groupby('Labels').mean())


























# in order to display plot within window
# plt.show()
