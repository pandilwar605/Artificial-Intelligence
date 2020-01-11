import os
from sys import argv
from collections import Counter
from operator import mul
from functools import reduce
from math import log
from utils import get_processed_words_from_file


def train_classifier(train_folder_path):

    #spam path
    spam_folder_path = os.path.join(train_folder_path, "spam")
    #ham path
    ham_folder_path = os.path.join(train_folder_path, "notspam")

    spam_words = []
    ham_words = []

    for index, file_name in enumerate(os.listdir(spam_folder_path)):
        spam_words.extend(
            get_processed_words_from_file(
                os.path.join(spam_folder_path, file_name)
            )
        )

    for index, file_name in enumerate(os.listdir(ham_folder_path)):
        ham_words.extend(
            get_processed_words_from_file(
                os.path.join(ham_folder_path, file_name)
            )
        )

    spam_counter = Counter(spam_words)
    ham_counter = Counter(ham_words)

    spam_file_count = len(os.listdir(spam_folder_path))
    ham_file_count = len(os.listdir(ham_folder_path))
    total_file_count = spam_file_count+ham_file_count

    spam_prior = spam_file_count/total_file_count
    ham_prior = ham_file_count/total_file_count

    return spam_counter, ham_counter, spam_prior, ham_prior

def test_classifier(
    test_folder_path, spam_counter, ham_counter,
    spam_prior, ham_prior, output_file
):

    test_label = {}

    with open('test-groundtruth.txt','r') as f:
        for line in f.readlines():
            name, label = line.strip().split()
            test_label[name] = label

    all_word_counter = spam_counter+ham_counter

    total = 0
    correct = 0
    predictions = {}
    for file in os.listdir(test_folder_path):
        total+=1
        words_in_email = get_processed_words_from_file(
            os.path.join(test_folder_path, file)
        )
        spam_prob = 0
        ham_prob = 0
        for word in words_in_email:
            if word in spam_counter.keys():
                word_given_spam = spam_counter[word]/all_word_counter[word]
                spam_word_prob_numerator = log(word_given_spam)+log(spam_prior)
                spam_prob+=spam_word_prob_numerator
            if word in ham_counter.keys():
                word_given_ham = ham_counter[word]/all_word_counter[word]
                ham_word_prob_numerator = log(word_given_ham)+log(ham_prior)
                ham_prob+=ham_word_prob_numerator

        prediction = 'spam'
        if spam_prob/ham_prob>2:
            if test_label[file] == 'spam':
                correct+=1
        else:
            prediction = 'notspam'
            if test_label[file] == 'notspam':
                correct+=1
        predictions[file] = prediction

    with open(output_file, 'w') as f:
        for file_name, label in predictions.items():
            f.write("{} {}\n".format(file_name, label))
    print("accuracy is {}".format(correct/total))

train_folder = argv[1]
test_folder = argv[2]
output_file = argv[3]

spam_counter, ham_counter, spam_prior, ham_prior = train_classifier(
    train_folder
)
test_classifier(
    test_folder, spam_counter, ham_counter,
    spam_prior, ham_prior, output_file
)
