import numpy as np

from sys import argv

from utils import *

import pickle

class NeuralNet:
    def __init__(self, x=None, y=None, act='sig'):
        self.input = x
        self.output = y
        hid1units = 96
        hid2units = 48
        self.lr = 5e-2
        input_size = 192
        output_size = 4
        self.w1 = np.random.standard_normal((input_size, hid1units))
        self.b1 = np.zeros((1, hid1units))
        self.w2 = np.random.standard_normal((hid1units, hid2units))
        self.b2 = np.zeros((1, hid2units))
        self.w3 = np.random.standard_normal((hid2units, output_size))
        self.b3 = np.zeros((1, output_size))
        self.act = self.sigmoid if 'sig' in act else self.relu
        self.act_derv = self.sigmoid_derv if 'sig' in act else self.relu_derv
        self.loss_arr = []

    def forward(self, test = False):
        x = self.testdata if test else self.input
        z1 = np.dot(x, self.w1) + self.b1
        self.a1 = self.act(z1)
        z2 = np.dot(self.a1, self.w2) + self.b2
        self.a2 = self.act(z2)
        z3 = np.dot(self.a2, self.w3) + self.b3
        self.a3 = self.softmax(z3)

    def sigmoid(self, x):
        #not keeping this as a classmethod
        return 1/(1 + np.exp(-x))

    def sigmoid_derv(self, x):
        sig_x = self.sigmoid(x)
        return sig_x * (1 - sig_x)

    def relu(self, x):
        #fast implementation of relu
        #ref https://stackoverflow.com/questions/32109319/how-to-implement-the-relu-function-in-numpy
        return np.maximum(x, 0, x)

    def relu_derv(self, x):
        #fast implementation of relu derivative
        #ref https://stackoverflow.com/questions/54969120/faster-implementation-for-relu-derivative-in-python/54969428
        return (x>=0).view('i1')

    def softmax(self, x):
        #not keeping this as a classmethod
        #This is neumarically stable softmax
        #ref https://stackoverflow.com/questions/42599498/numercially-stable-softmax
        exps = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exps/np.sum(exps, axis=1, keepdims=True)

    def cross_entropy(self, op, labels):
        sample_count = labels.shape[0]
        res = op - labels
        return res/sample_count

    def error(self, op, labels):
        sample_count = labels.shape[0]
        numerator = np.sum(
            - np.log(op[np.arange(sample_count), labels.argmax(axis=1)])
        )
        loss = numerator/sample_count
        return loss

    def backward(self, show_loss=False, save_loss=True):
        loss = self.error(self.a3, self.output)
        if save_loss:
            self.loss_arr.append(loss)
        if show_loss:
            print('Error :', loss)
        a3_delta = self.cross_entropy(self.a3, self.output)
        z2_delta = np.dot(a3_delta, self.w3.T)
        a2_delta = z2_delta * self.act_derv(self.a2)
        z1_delta = np.dot(a2_delta, self.w2.T)
        a1_delta = z1_delta * self.act_derv(self.a1)
        self.b3 -= self.lr * np.sum(a3_delta, axis=0, keepdims=True)
        self.w2 -= self.lr * np.dot(self.a1.T, a2_delta)
        self.b2 -= self.lr * np.sum(a2_delta, axis=0)
        self.w1 -= self.lr * np.dot(self.input.T, a1_delta)
        self.b1 -= self.lr * np.sum(a1_delta, axis=0)

    def predict(self, data):
        self.testdata = data
        self.forward(test=True)
        return self.a3.argmax(axis=1)

    def fit(self, epochs, error_show_interval=None):
        if error_show_interval is None:
            error_show_interval = epochs/10
        show_loss = False
        for epoch in range(epochs):
            print("Epoch {} of {}".format(epoch+1, epochs))
            self.forward()
            if epoch%error_show_interval == 0:
                show_loss = True
            self.backward(show_loss)
            show_loss = False

    def check_accuracy(self, testdata, testlabels):

        predictions = self.predict(testdata)
        labels = np.argmax(testlabels, axis=1)
        correct = (predictions == labels).sum()
        total = predictions.shape[0]
        accuracy = correct*100./total

        return accuracy, predictions

    def loadmodelfromfile(self, modelfile):
        model_dict = {}
        params = ['w1', 'b1', 'w2', 'b2','w3', 'b3']
        with open(modelfile, 'rb') as f:
            model_dict = pickle.load(f)

        for param in params:
            setattr(self, param, model_dict[param])

    def savemodeltofile(self, modelfile):
        model_dict = {}
        params = ['w1', 'b1', 'w2', 'b2','w3', 'b3']
        for param in params:
            model_dict[param] = getattr(self, param)

        with open(modelfile, 'wb') as f:
            pickle.dump(model_dict, f)
