#!/usr/bin/env python3
"""
Name: Isabel Gallegos
Creates a linear model of the relationship between height, sex, race, education
level, and age and expected wage.
"""
import numpy as np
import pandas

INPUT_FILENAME = 'wages.csv'

def load_data(filename):
    """
    Loads the wage data from a csv file.

    Arguments:
    filename -- the file that contains the wage data

    Returns:
    wage_data -- numpy array with the following fields
        "earn"
        "height"
        "sex"
        "race"
        "ed"
        "age"
    """
    wage_data = pandas.read_csv(filename, delimiter = ',').to_numpy()
    return wage_data


def clean_data(wage_data):
    """
    Cleans the wage data into two numpy arrays.

    Arguments:
    wage_data -- a numpy array of wages and features (height, sex, race, ed, age)

    Returns:
    X -- a numpy array of length 1379 x 5 where each row has the form
         [height, sex, race, ed, age]
    y -- a 1379-length numpy array, where y[i] is the wage associated with X[i]
    """
    # get wages
    y = wage_data[:,0]
    y = y.reshape(y.size, 1)
    y = y.astype(float)

    # get features, convert strings to 0/1 values
    height = wage_data[:,1]
    height = height.reshape(height.size, 1)

    sex = wage_data[:,2]
    male = np.where(sex == "male", 1, 0)
    male = male.reshape(male.size, 1)
    female = np.where(sex == "female", 1, 0)
    female = female.reshape(female.size, 1)

    race = wage_data[:,3]
    white = np.where(race == "white", 1, 0)
    white = white.reshape(white.size, 1)
    black = np.where(race == "black", 1, 0)
    black = black.reshape(black.size, 1)
    hispanic = np.where(race == "hispanic", 1, 0)
    hispanic = hispanic.reshape(hispanic.size, 1)
    other = np.where(race == "other", 1, 0)
    other = other.reshape(other.size, 1)

    ed = wage_data[:,4]
    ed = ed.reshape(ed.size, 1)
    age = wage_data[:,5]
    age = age.reshape(age.size, 1)

    X = np.concatenate((height, male, female, white, black, hispanic, other, ed, age), axis=1)
    X = X.astype(float)

    return X, y


def fit_model(X, y):
    """
    Processes the wage data by fitting a line to it.

    Arguments:
    X -- an 1379 x 9 numpy array, where each row is of the form [height, male,
         female, white, black, hispanic, other, ed, age] representing a single data point
    y -- a 800-length numpy array, where y[i] is the wage for the individual
         associated with X[i]

    Returns:
    weights of the model
    """
    return np.linalg.lstsq(X, y, rcond=None)[0]


def create_model():
    """
    Loads and cleans data, and uses linear regression to model relationship
    between the features [height, male, female, white, black, hispanic, other, ed, age]
    and wage.

    Returns:
    weights -- weights of the model
    """
    print("\nCreating model...")
    # Load data
    wage_data = load_data(INPUT_FILENAME)

    # Inform user about data
    if wage_data is None:
        print("Warning: no data recieved.")
        return

    # Clean data
    clean_data(wage_data)
    try:
        X, y = clean_data(wage_data)
    except TypeError:
        X, y = None, None

    # Inform user about data
    if X is None and y is None:
        print("Warning: no data cleaned.")
        return

    # Process data
    try:
        weights = fit_model(X, y)
    except TypeError:
        weights = None

    if weights is None:
        print("Warning: no model fitted.")
        return

    print("Model fitted.\n")
    return weights
