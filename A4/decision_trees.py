import numpy as np
import random
from queue import PriorityQueue

# =============================================================================
# References:
# https://paragmali.me/building-a-decision-tree-classifier/
# https://wiki.python.org/moin/UsingPickle
# https://medium.com/@rishabhjain_22692/decision-trees-it-begins-here-93ff54ef134
# https://towardsdatascience.com/decision-tree-overview-with-no-maths-66b256281e2b
# http://www.r2d3.us/visual-intro-to-machine-learning-part-1/
# =============================================================================


# =============================================================================
# To build a tree using recursion of nodes
# =============================================================================
class Node(object):
    def __init__(self):
            self.value = 0    #label
            self.left = None  #node on left
            self.right = None #node on right
            self.split = None #Contains feature index and its corresponding split point


# =============================================================================
# Training model with train data and labels and using depth of the tree as 5 by default. 
# Any further, it will be computationally very expensive
# =============================================================================
def train_decision_tree(train_data,label,depth):
    node=Node()
#    print(len(train_data))
    if(len(train_data)<1): #If data is at the end and its not classified, then assigning random labels for it.
        node.value=random.randint(0,3) * 90 #assigning random label since this data is not classified
        return node
    else:
        (accept_it, label_assigned) = accept_and_assign_label(train_data,label)  #returns label value and whether it can be used as condition for data
        if accept_it or depth < 0 or len(train_data) < 3: # If any of the condition satisfies, then all elements available are classified in this node
            node.value = label_assigned # return the correct classification for this node
            return node
    
    entropy, splitPoint,feature_index = find_split_point_and_feature_index(train_data,label)
#    print("Check")
    node.split = (splitPoint,feature_index)
    [leftTrainData,leftLabel, rightTrainData, rightLabel] = split_left_right(train_data, splitPoint, feature_index, label)
    
#    print(leftTrainData)
#    print(rightTrainData)
#    print(rightLabel)
#    print(leftTrainData.shape)
#    print(rightTrainData[0].shape)
#    print(leftTrainData)
#    print(rightTrainData)
#    sys.exit()

    node.left = train_decision_tree(leftTrainData,leftLabel, depth-1) #Recursion
    node.right = train_decision_tree(rightTrainData,rightLabel, depth-1)

    return node


# =============================================================================
# This function checks whether data is properly classified, 
# if its not then accept value is false and it goes further into decision tree
# =============================================================================
def accept_and_assign_label(train_data,label):
    label_count = [1, 1, 1, 1] # initial default count for each label
    for each_label in label: #Counter increment for each label
#        print(each_label)
        if each_label == 0:
            label_count[0] += 1
        elif each_label == 90:
            label_count[1] += 1
        elif each_label == 180:
            label_count[2] += 1
        elif each_label == 270:
            label_count[3] += 1
            
    
    value = label_count.index(max(label_count)) * 90 #Whichever label has max count, that will be used as decision criteria for that node
    
    accept_it = False #By default its false, meaning we will go further into tree to decide
    if(max(label_count) / sum(label_count)) > 0.9: #Unless the label having 0.9 probability, i.e. its not dominating other labels, we won't accept it and go further into tree with this data 
        accept_it = True #accept this label value at the leaf.
    return (accept_it, value)

    
    
# =============================================================================
#  This function is used to find entropy for each feature and returns feature and split point of that feature 
#  which has smallest entropy and will be used as data splitting condition 
# =============================================================================
def find_split_point_and_feature_index(train_data,label):
    featureQueue = PriorityQueue() #To store entropy values, feature index and split value
    no_of_samples=20
# Taking only 20 random features instead of whole 192 feature, to make it computationally less expensive. 
# However this will result in high variance, because we dont know which feature are more important/ more pratical to use
    sample_features=random.sample(range(0,192), no_of_samples) 
    feature_matrix=train_data.transpose()
#    print(feature_matrix.shape)
#    print(sample_features)
#    dasd=feature_matrix[43]
#    print(type(dasd))
#    print(dasd.shape)
#    sys.exit()
    for i in sample_features: # For each random feature
#        print(i)
#        print(feature_matrix[i])
        feature = feature_matrix[i]
        feature=feature.reshape(feature.shape[0],1)
        (entropy,split)=find_split_point(feature,train_data,label) #Find entropy 
        featureQueue.put((entropy,split,i))
    
    return featureQueue.get() #Returns split point which has lowest entropy
    
# =============================================================================
#  This functions splits the data into left and right node based on feature index's split point value    
# =============================================================================
def split_left_right(train_data, split_point, ind, label):
#    print(train_data.shape)
#    print(split_point)
#    print(ind)
#    print(label.shape)
    leftTrainData = []
    leftLabel=[]
    rightTrainData = []
    rightLabel=[]
    for i in range(len(train_data)):
        if train_data[i][ind] < split_point:
            leftTrainData.append(train_data[i])
            leftLabel.append(label[i])
#            print(np.asarray(leftTrainData))
#            print(leftLabel)
        else:
            rightTrainData.append(train_data[i])
            rightLabel.append(label[i])
#            print(np.asarray(rightTrainData[0][0]))
#            print(np.asarray(rightTrainData[0][1]))
    leftTrainData = np.array(leftTrainData)
    rightTrainData = np.array(rightTrainData)
    partition_data = [leftTrainData,leftLabel, rightTrainData, rightLabel]
    return partition_data
    
# =============================================================================
#  This function calculates and returns split point value for a feature and whichever point has less entropy         
# =============================================================================
def find_split_point(feature,train_data,label):
    N=len(train_data)
    queue = PriorityQueue() #For storing entropy and split point value
    temp,unique_indices = np.unique(feature, return_index=True) #Take only unique values
#    print(unique_indices)
    for each_index in unique_indices:
        split_point = feature[each_index]
        left = []
        right = []
        for index in range(len(feature)):
            if feature[index] < split_point:
                left.append((index,feature[index]))
            else:
                right.append((index,feature[index]))
        label_count = [1, 1, 1, 1]  # initial default count for each label
        entropy = 0
        for point in left:
            if label[point[0]] == 0:
                label_count[0] += 1
            elif label[point[0]] == 90:
                label_count[1] += 1
            elif label[point[0]] == 180:
                label_count[2] += 1
            elif label[point[0]] == 270:
                label_count[3] += 1

        n_left = len(left)
        n = sum(label_count)

# References: Entropy calculation is referred from following link as well as took help from some of the colleagues while implementing it. Couldn't do it myself.
# https://medium.com/@rishabhjain_22692/decision-trees-it-begins-here-93ff54ef134
        entropy += n_left/N * ((label_count[0]/n * label_count[0]/n) + (label_count[1]/n * label_count[1]/n) + \
        (label_count[2]/n * label_count[2]/n) + (label_count[3]/n * label_count[3]/n))
        label_count = [1, 1, 1, 1] # initial default count for each label
        for point in right:
            if label[point[0]] == 0:
                label_count[0] += 1
            elif label[point[0]] == 90:
                label_count[1] += 1
            elif label[point[0]] == 180:
                label_count[2] += 1
            elif label[point[0]] == 270:
                label_count[3] += 1

        n_right = len(right)
        n = sum(label_count)
# Entropy calculation
        entropy += n_right/N * ((label_count[0]/n * label_count[0]/n) + (label_count[1]/n * label_count[1]/n) + \
        (label_count[2]/n * label_count[2]/n) + (label_count[3]/n * label_count[3]/n))
        queue.put((1-entropy, feature[each_index]))
    return queue.get() #returns an element which has lowest entropy


# =============================================================================
# Test function which returns predicted image orientation
# =============================================================================
def test_decision_tree(tree,test_data):
    if tree.left == None and tree.right == None: #If it is leaf node or no tree is available
        return tree.value
    else: #Recusively go deep into decision tree unless predicted label is not found  and return predicted label
        [splitPoint, col_num] = tree.split
        if test_data[col_num] < splitPoint:
            return test_decision_tree(tree.left, test_data)
        else:
            return test_decision_tree(tree.right, test_data)   