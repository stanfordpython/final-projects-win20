CS 41 Final Project: EEG Classifier
Name: Grant Sheen 
Email: gsheen@stanford.edu

For my final project, I created a Python program that can predict whether a person is resting or focused based on their EEG data. The program can be executed by adding the eeg_classifier.py and preprocessed_eeg_data.txt files into the current directory and then running "python3 eeg_classifier.py" in the command line. 

My program is made up of 3 functions - load_dataset, logistic_regression, and testing_simulation.

load_dataset:
This function takes in the pre-processed EEG 4-thought data file, which contains the features of the EEG data where the lines are in alternating order of each thought. These features were previously found by applying fourier transform to the raw voltage data and converting them to power spectrum densities and applying a frequency filter from 2-32 Hz. A binary dataset is extracted from the 4-thought data file by taking the first 2 lines in each group of 4 lines and adding them to an array. Then, the data is split into training data, testing data, training labels, and testing labels arrays using the train_test_split in sklearn. Then, those arrays are returned.

logistic_regression:
This function takes in the training data, testing data, training labels, and testing labels arrays and implements a logistic regression neural network model. This logistic regression model is imported from sklearn and then fit using the training data. Then, the predicted labels are calculated based on the testing data. Then, the arrays of testing labels and predicted labels are returned.

testing_simulation:
This function runs a real time simulation of EEG classification of resting or focused states, printing out the actual state compared to the predicted state as well as the accuracy of the program. It traverses through the testing labels and predicted labels arrays and prints out the accuracy of the predictions and the overall accuracy at the end. 
