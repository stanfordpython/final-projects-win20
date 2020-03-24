#!/usr/bin/env python3

import numpy as np
import time
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle

def load_dataset(filename):
    """
        Loads the pre-processed EEG 4-thought dataset into a NumPy array of labeled binary data
        for rest and focus. Then, it splits the binary dataset into separate arrays for training
        data, testing data, training labels, and testing labels.
        
        Input:
        filename - the name of the .txt file to load.
        
        Output:
        training_data - an array of the EEG features used to train the model
        testing_data - an array of the EEG features used to test the model
        training_labels - an array of the corresponding labels for the EEG training features
        testing_labels - an array of the corresponding labels for the EEG testing features
        """
    # load pre-processed 4-thought data
    with open(filename, "r") as f:
        dataset = np.loadtxt(f)
    
    # filter dataset into an array with only 2 thoughts
    binary_list = []
    for index,element in enumerate(dataset):
        if index % 4 < 2:
            binary_list.append(element)
    binary_dataset = np.asarray(binary_list)
    binary_dataset = preprocessing.scale(binary_dataset)

    # write the labels of the dataset into an array
    data_labels = np.array([0, 1] * 742)
    np.transpose(data_labels)
    
    # randomly split the dataset into training and testing subsets
    training_data, testing_data, training_labels, testing_labels = train_test_split(binary_dataset, data_labels, test_size=0.2, shuffle=False)
    
    return training_data, testing_data, training_labels, testing_labels


def logistic_regression(training_data, testing_data, training_labels, testing_labels):
    """
        Implements a logistic regression model by fitting it with the training data and labels
        and then calculates the predicted labels of the testing data. Then, it returns the testing
        labels and their corresponding predicted labels.
        
        Input:
        training_data - the array of EEG features used for training the model
        testing_data - the array of EEG features used for testing the model
        training_labels - the array of training data labels
        testing_labels - the array of testing data labels
        
        Output:
        testing_labels - the array of shuffled testing labels
        predicted_labels - the array of predicted labels corresponding to the shuffled testing labels
    """
    # creates a logistic regression model and fits it with the training data and training labels
    logistic_regression = LogisticRegression()
    logistic_regression.fit(training_data, training_labels)
    
    # shuffles testing data and testing labels in unison
    testing_data, testing_labels = shuffle(testing_data, testing_labels)

    # finds predicted labels
    predicted_labels = logistic_regression.predict(testing_data)

    return testing_labels, predicted_labels


def testing_simulation(testing_labels, predicted_labels):
    """
        Runs a real time simulation of EEG classification of resting or focused states, printing
        out the actual state compared to the predicted state as well as the accuracy of the program.
        
        Input:
        testing_labels - the array of labels for the testing data
        predicted_labels - the array of predicted labels for the testing data
    """
    # testing simulation
    total_guesses = 0
    correct_guesses = 0
    second = 1
    print("Real Time EEG Classification of Resting or Focus\n")
    for i in range(0, len(testing_labels)):
        # actual label
        if (testing_labels[second - 1] == 0):
            print("At {} mins and {} seconds, the person was resting.".format(second // 60, second % 60))
        else:
            print("At {} mins and {} seconds, the person was focused.".format(second // 60, second % 60))

        # predicted label
        if (predicted_labels[second - 1] == 0):
            print("The program predicted: resting")
        else:
            print("The program predicted: focus")

        # result
        if (testing_labels[second - 1] == predicted_labels[second - 1]):
            print("Correct!")
            correct_guesses += 1
        else:
            print("Incorrect.")
        total_guesses += 1
        print("Accuracy: {}/{}, {}%\n".format(correct_guesses, total_guesses, (correct_guesses/total_guesses) * 100))
        second += 1
        time.sleep(0.3)

    # overall result
    print("Overall Accuracy: {}/{}, {}%\n".format(correct_guesses, total_guesses, (correct_guesses/total_guesses) * 100))


if __name__ == "__main__":
    training_data, testing_data, training_labels, testing_labels = load_dataset("preprocessed_eeg_data.txt")
    testing_labels, predicted_labels = logistic_regression(training_data, testing_data, training_labels, testing_labels)
    testing_simulation(testing_labels, predicted_labels)
