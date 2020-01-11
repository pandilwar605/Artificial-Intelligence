import numpy as np
import sys

def get_processed_data(file):
    data_arr = []
    label_arr = []
    labels = [0, 90, 180, 270]
    with open(file, 'r') as f:
        contents = f.readlines()
        for content in contents:
            split_content = content.split()
            data_arr.append(np.array(split_content[2:]))
            label_arr.append([1 if int(split_content[1]) == labels[i] else 0 for i in range(4)])
    return np.array(data_arr, dtype=np.float32), np.array(label_arr)

def read_data_for_tree(file):
    data_arr = []
    label_arr = []
    with open(file, 'r') as f:
        contents = f.readlines()
        for content in contents:
            split_content = content.split()
            data_arr.append(np.array(split_content[2:]))
            label_arr.append(int(split_content[1]))
    return np.array(data_arr, dtype=np.float32), np.asarray(label_arr, dtype=np.int32)
    

def writepredictionfile(readfile, predictions, writefile):
    content_to_write = ""
    img_names = []
    labels = ['0', '90', '180', '270']
    with open(readfile, 'r') as f:
        contents = f.readlines()
        for content in contents:
            split_content = content.split()
            img_names.append(split_content[0])

    with open(writefile, 'w') as f:
        for index in range(len(predictions)):
            label = labels[predictions[index]]
            f.write('{} {}\n'.format(img_names[index], label))



def normalize_data_for_neural_network(data):
    return data/255
