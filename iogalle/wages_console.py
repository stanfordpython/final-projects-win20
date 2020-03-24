#!/usr/bin/env python3
"""
Name: Isabel Gallegos
Run a console menu to interact with the wage predictor.

The model fitting functionality is provided by the `predict_wages` module.
"""
import random
import numpy as np
from predict_wages import create_model

HEADER = r"""
    Welcome to the Wage Predictor!
    Enter some information about yourself, and we'll predict your wage.
    Then see how your wage would change if your gender or race were different.
"""

def get_num_input(prompt):
    """Ask the user for numerical input.

    Return responses that can be converted to floats.
    All other responses (including '') cause a reprompt.

    Arguments:
    prompt -- string to prompt user for input

    Return:
    choice_float -- float representation of user input
    """
    while True:
        try:
            choice = input(prompt).upper()
            choice_float = float(choice)
            return choice_float
        except ValueError:
            print("Please enter a valid number.")
            pass
    return choice_float


def get_string_input(prompt, options):
    """Ask the user for string input that matches an option in `options`.

    Return responses that are contained in `options`.
    All other responses (including '') cause a reprompt.

    Arguments:
    prompt -- string to prompt user for input

    Return:
    choice -- user's input
    """
    choice = input(prompt).upper()
    while not choice or choice not in options:
        choice = input("{} Please enter one of {}. ".format(prompt, '/'.join(options))).upper()
    return choice


def get_yes_or_no(prompt, reprompt=None):
    """Ask the user whether they would like to continue.

    Responses that begin with a `Y` return True. (case-insensitively)
    Responses that begin with a `N` return False. (case-insensitively)
    All other responses (including '') cause a reprompt.

    Arguments:
    prompt -- string to prompt user for input

    Return:
    True is user enters 'Y', False otherwise
    """
    if not reprompt:
        reprompt = prompt

    choice = input("{} (Y/N) ".format(prompt)).upper()
    while not choice or choice[0] not in ['Y', 'N']:
        choice = input("Please enter either 'Y' or 'N'. {} (Y/N)? ".format(reprompt)).upper()
    return choice[0] == 'Y'


def get_user_features():
    """Ask the user for the personal information to populate their user vector.

    Populate and return vector containing user's height, sex, race, education, and
    age information.

    Return:
    user_vector -- length-9 array containing user's features
    """
    # get user input
    height = get_num_input("Please enter your height in inches. ")
    sex = get_string_input("Please enter your sex. ", ["MALE", "FEMALE"])
    race = get_string_input("Please enter your race. ", ["WHITE", "BLACK", "HISPANIC", "OTHER"])
    ed = get_num_input("Please enter the number of years you attended school. ")
    age = get_num_input("Please enter your age in years. ")

    # populate user vector
    # height, male, female, white, black, hispanic, other, ed, age
    user_vector = np.zeros(9)
    user_vector[0] = height
    user_vector[1] = 1 if sex.upper() == "MALE" else 0
    user_vector[2] = 1 if sex.upper() == "FEMALE" else 0
    user_vector[3] = 1 if race.upper() == "WHITE" else 0
    user_vector[4] = 1 if race.upper() == "BLACK" else 0
    user_vector[5] = 1 if race.upper() == "HISPANIC" else 0
    user_vector[6] = 1 if sex.upper() == "OTHER" else 0
    user_vector[7] = ed
    user_vector[8] = age
    return user_vector.reshape(user_vector.size, 1), sex.upper(), race.upper()


def predict_wage(model_weights, user_vector):
    """Predict wage using model weights and the user's vector.

    Take dot product of `model_weights` and `user_vector`.

    Return:
    predicted_wage -- wage calculated by model
    """
    predicted_wage = np.dot(model_weights.T, user_vector)[0][0]
    return predicted_wage


def change_user_feature(user_vector, orig_ind, change_ind):
    """Changes one feature of `user_vector`.

    Sets element at `orig_ind` to 0 and element at `change_ind` to 1.

    Arguments:
    user_vector -- original user user_vector
    orig_ind -- index to set to 0
    change_ind -- index to set to 1

    Return:
    user_vector_new -- modified vector
    """
    user_vector_new = user_vector
    user_vector_new[orig_ind] = 0
    user_vector_new[change_ind] = 1
    return user_vector_new


def print_alternate_wage(original_wage, alternate_wage, feature):
    """Prints formatted output for alternate wage.

    Calculates difference between original wage and alternate wage, and prints
    result.

    Arguments:
    original_wage -- predicted wage for user with provided features
    alternate_wage -- predicted wage for user with a modified features
    feature -- string label of feature that was changed
    """
    diff = original_wage - alternate_wage
    diff_string = "lower" if diff > 0 else "higher"

    print("If you were " + feature + ", your predicted wage would be ${:.2f} {}.".format(abs(diff), diff_string))
    pass


def alternate_prediction(model_weights, original_wage, user_vector, sex, race):
    """Changes features of user vector and outputs new predicted wage.

    Changes gender and race of user to predict what their wage would be with all
    other features the same.

    Arguments:
    model_weights -- weights of the model
    original_wage -- predicted wage for user with provided features
    user_vector -- length-9 array containing user's features
    sex -- user's sex
    race -- user's race
    """
    is_male = sex == "MALE"
    is_white = race == "WHITE"

    if is_male:
        # change gender to female
        user_vector_female = change_user_feature(user_vector, 1, 2)
        wage_female = predict_wage(model_weights, user_vector_female)
        print_alternate_wage(original_wage, wage_female, "female")
    else:
        # change gender to male
        user_vector_male = change_user_feature(user_vector, 2, 1)
        wage_male = predict_wage(model_weights, user_vector_male)
        print_alternate_wage(original_wage, wage_male, "male")

    if is_white:
        # change race to black
        user_vector_black = change_user_feature(user_vector, 3, 4)
        wage_black = predict_wage(model_weights, user_vector_black)
        print_alternate_wage(original_wage, wage_black, "black")

        # change race to Hispanic
        user_vector_hispanic = change_user_feature(user_vector, 3, 5)
        wage_hispanic = predict_wage(model_weights, user_vector_hispanic)
        print_alternate_wage(original_wage, wage_hispanic, "Hispanic")
    else:
        # change race to white
        user_vector_white = change_user_feature(user_vector, 4, 3)
        user_vector_white = change_user_feature(user_vector_white, 5, 3)
        user_vector_white = change_user_feature(user_vector_white, 6, 3)
        wage_white = predict_wage(model_weights, user_vector_white)
        print_alternate_wage(original_wage, wage_white, "white")
    pass


def run_suite(model_weights):
    """Run a single iteration of the wage predictor suite.

    Asks the user to input their personal information, predicts their wage, and
    makes alternate predictions if some aspects of their identity were different.

    Arguments:
    model_weights -- weights of model calculated by `predict_wages` module
    """
    print('-' * 34)
    user_vector, sex, race = get_user_features()

    predicted_wage = predict_wage(model_weights, user_vector)
    print()
    print("We predict that your wage will be ${:.2f}.".format(predicted_wage))

    print()
    alternate_prediction(model_weights, predicted_wage, user_vector, sex, race)


def main():
    """Run the main interactive console for the wage predictor."""
    print(HEADER)
    model_weights = create_model()
    run_suite(model_weights)
    while get_yes_or_no("\nAgain?"):
        run_suite(model_weights)
    print("Goodbye!")


if __name__ == '__main__':
    main()
