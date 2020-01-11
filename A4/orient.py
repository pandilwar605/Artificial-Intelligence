from nn import *
from sys import argv
from utils import *
from nearest import *
import pandas as pd
import time
import pickle
import numpy as np
from decision_trees import *

mode = argv[1]
readfile = argv[2]
modelfile = argv[3]
model = argv[4]

if model == 'nnet':
    if mode == 'train':
        print("Loading data")

        train_data, train_labels = get_processed_data(readfile)
        train_data = normalize_data_for_neural_network(train_data)
        print("Training neural net")
        net = NeuralNet(train_data, train_labels)
        epochs = 500
        loss_epoch = 10
        net.fit(epochs, loss_epoch)
        print("Saving model")
        net.savemodeltofile(modelfile)
    elif mode == 'test':
        print("Loading data")
        test_data, test_labels = get_processed_data(readfile)
        test_data = normalize_data_for_neural_network(test_data)
        print("Loading trained neural net from file")
        net = NeuralNet()
        net.loadmodelfromfile(modelfile)
        print("Predicting using trained neural net")
        accuracy, preds = net.check_accuracy(test_data, test_labels)
        print("Accuracy is {}:".format(accuracy))
        print("Writing predictions to output.txt")
        writepredictionfile(readfile, preds, 'output.txt')
        print("Done")
        
elif model == 'nearest' or model == 'best': # Accuracy for knn is the highest, hence giving the same treatment for best classifier
    k = 11
    start_time = time.time()

    if mode == 'train':
        if model == 'nearest':
            with open(readfile) as f:
                with open("nearest_model.txt", "w") as f1:
                    for line in f:
                        f1.write(line)
            end_time = time.time()
            print("Time taken to train KNN:", end_time-start_time)
        else:
            with open(readfile) as f:
                with open("best_model.txt", "w") as f1:
                    for line in f:
                        f1.write(line)
            end_time = time.time()
            print("Time taken to train Best:", end_time-start_time)
    
    elif mode == 'test':
        print("Loading data")
        # Train data
        training_data = pd.read_csv(modelfile, delim_whitespace = True, header = None)
        train_labels = training_data[1].values
        train_labels = train_labels.reshape(-1,1)
        training_data.drop([0,1] , axis = 1, inplace = True)
        train_data = training_data.values
        
        # Test data
        testing_data = pd.read_csv(readfile, delim_whitespace = True, header = None)
        test_labels = testing_data[1].values  # Labels of test data, to be used in calculating accuracy
        test_labels = test_labels.reshape(-1,1)
        testing_data.drop([0,1] , axis = 1, inplace = True)
        test_data = testing_data.values # Only values of the test data: to be used in output
        print("Predicting")

        knn_output = knn(train_data, train_labels, test_data, test_labels, k)
    
        end_time = time.time()
        print("Time taken to execute:", end_time-start_time)
            
        filename_train = pd.read_csv("test-data.txt",delim_whitespace=True,header=None).iloc[:,0]
        print("Writing predictions to output.txt")
        file=open("output.txt", "w")
        for i in range(len(test_data)):
            file.write(filename_train[i]+ " ")
            file.write(str(knn_output[i][0]) + '\n')
        print("Done")
        
elif model == 'tree':
    depth = 5
    if mode == 'train':
        print("Loading data")
        train_data, labels = utils.read_data_for_tree(readfile)
        labels=labels.reshape(labels.shape[0])
        print("Training decision tree")
        tree_model=train_decision_tree(train_data,labels,5)
        print("Saving model")        
        with open(modelfile, 'wb') as fp:
            pickle.dump(tree_model, fp)
        
    elif mode == 'test':
        print("Loading data")
        test_data, labels = utils.read_data_for_tree(readfile)
        test_labels=labels.reshape(labels.shape[0])        
        with open (modelfile, 'rb') as fp:
            tree = pickle.load(fp)
        
        correct = 0
        predictions=[]
        for i in range(len(test_data)):
            predict=test_decision_tree(tree,test_data[i])
            predictions.append(predict)
            if(predict == test_labels[i]):
                correct += 1
        print("Accuracy of Tree model = ", str((correct/len(test_data))*100) + "%")
        
        filename_train = pd.read_csv(readfile,delim_whitespace=True,header=None).iloc[:,0]
        print("Writing predictions to output.txt")
        file=open("output.txt", "w")
        for i in range(len(test_data)):
            file.write(filename_train[i]+ " ")
            file.write(str(predictions[i]) + '\n')
        print("Done")
