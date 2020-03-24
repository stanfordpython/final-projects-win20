WAGE PREDICTOR
==============
VIDEO LINK: https://photos.app.goo.gl/VJ6oWVugFbgz1XhAA

--------
Overview
--------
My project fits a linear model to an online dataset containing information
about people's wages, height, sex, race, education level, and age. The predict_wages
module processes the data and fits the model, and the wages_console allows users
to interact with the model and enter their own information to get a prediction.
This project also calculates how the wage predictions change if a person's sex
or race were different.

-----------------
Technical Details
-----------------
The predict_wages module processes the data by reading in a csv file, and then cleans
the data by separating the wage information from the feature information, and replaces
the categorical race and gender information with one-hot encoding. Finally, it
uses least squares to fit a model to the data. The wages_console prompts the user
for input, and uses this input to create a new user feature vector. Using the model
created by the predict_wages module, we make a wage prediction for the new user.

-------------
Prerequisites
-------------
numpy, pandas, random

----------------
Running the Code
----------------
Run the wages_console.py script with "python3 wages_console.py". This program will
fit the model to the data, then prompt the user to enter input, and finally report
its predictions.

------------
Example Test
------------
    $ python3 wages_console.py

        Welcome to the Wage Predictor!
        Enter some information about yourself, and we'll predict your wage.
        Then see how your wage would change if your gender or race were different.


    Creating model...
    Model fitted.

    ----------------------------------
    Please enter your height in inches. 61
    Please enter your sex. female
    Please enter your race. Hispanic
    Please enter the number of years you attended school. 14
    Please enter your age in years. 20

    We predict that your wage will be $13789.06.

    If you were male, your predicted wage would be $17552.54 higher.
    If you were white, your predicted wage would be $22145.33 higher.

    Again? (Y/N) N
    Goodbye!

----------
Known Bugs
----------
Unfortunately I had some trouble finding datasets that fit the needs of this
project, so this is the only dataset containing wage, race, and gender information
that I could find. The dataset didn't have much documentation, so I have no idea
what the wage values mean (e.g. annual income?). Also, the linear model may not be
the best fit, because sometimes the model predicts huge negative values, which doesn't
seem to make too much sense...
Further testing required!

-------
Authors
-------
I completed this assignment independently, but I used some of the code from
Assignments 1 and 2 as a template.
