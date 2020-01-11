import collections
import numpy as np
import sys
import time
import pandas as pd
from scipy.spatial import distance

def knn(train_data, train_labels, test_data, test_labels, k):
    results = distance.cdist(test_data, train_data, 'cosine') # Calculate cosine similarity between points using Scipy cdist function
    predicted = []
    
    indexes = np.argsort(results) # Sorting the indexes of the distances (not the distances)
    k_nearest_neigh = []
    
    # Getting the k-nearest neighbors from the obtained results
    for i in indexes:
        k_nearest_neigh.append(i[:k])
        
    k_nearest_neigh=np.array(k_nearest_neigh)
    
    # Obtain prediction for the test data using the train data labels for nearest points
    for i in k_nearest_neigh:
        predicted_label = []
        for ind in i:
            predicted_label.append(train_labels[ind][0])
            
        count = (collections.Counter(predicted_label).most_common(1)) # Finding the count of the orientations and finding the most common orientation among that

        predicted.append(count[0][0])

    predicted = np.array(predicted).reshape(len(predicted),1)
            
    print("Accuracy is :", 100 * np.mean(predicted == test_labels)) # Accuracy Calculation
    
    return predicted