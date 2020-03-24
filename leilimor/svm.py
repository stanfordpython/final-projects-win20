#!/usr/bin/env python3 

import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import metrics     
from sklearn.linear_model import SGDClassifier        
import matplotlib.pyplot as plt


################################ 
#    define variables
################################

#.1D files that denote the beginning of each trial with either 1 or -1
# choice of the risky option is denoted by 1 (risky) or -1 (safe) option
# 1 or -1 is the target variable of my classifier
PATH_CHOICE = 'data/{}/achoosepos.1D'

# Regions of interest (ROI) in the brain that will be used to predict choice
ROIs = ['mpfc', 'nacc', 'ins']

# .1D files that are timeseries data with ageraged activity of each ROI
PATH_mpfc_AVG = 'data/{}/bactive-epi-f_mpfc.1D' 
PATH_nacc_AVG = 'data/{}/bactive-epi-f_nacc8mm.1D'
PATH_ins_AVG = 'data/{}/bactive-epi-f_ins.1D'

# subject IDs range from 'sub-1' to 'sub-20' (including 20)
SUBJECTS = ['sub-{}'.format(str(x)) for x in range(1,21)]

# tr is time point when we get a brain volume
n_tr = 432

################################
#    import data 
#    and wrangle it
################################

# I want the dataframe to have the following variables (i.e. columns)
varNames = ['tr', 'subject', 'choice', 'mpfc', 'nacc', 'ins']

# make an empty dataframe that will contain all the data in the format we need it
df = pd.DataFrame(
	{'tr' : [],
	'subject' : [],
	'choice' : [],
	'mpfc' : [],
	'nacc' : [],
	'ins' : []}
	)

# import the input files:
# go into each subject's directory and read in the .1D data files
print("############\n IMPORTING DATA\n###########")
for SUB in SUBJECTS:
	# get the choice file
	fChoice = open(PATH_CHOICE.format(SUB), 'r')
	choiceList = fChoice.readlines() # makes a list on strings like this '-1\n'
	choice = [int(x.replace('\n', '')) for x in choiceList] # converts the format to integer excluding \n

    # get the 3 ROI files
    # mpfc
	fMPFC = open(PATH_mpfc_AVG.format(SUB), 'r')
	mpfcList = fMPFC.readlines() # makes a list on strings like this '-0.43234\n'
	mpfc = [float(x.replace('\n', '')) for x in mpfcList] # converts the format to float excluding \n
    # nacc 
	fNACC = open(PATH_nacc_AVG.format(SUB), 'r')
	naccList = fNACC.readlines() 
	nacc = [float(x.replace('\n', '')) for x in naccList]
    # insula 
	fINS = open(PATH_ins_AVG.format(SUB), 'r')
	insList = fINS.readlines() 
	ins = [float(x.replace('\n', '')) for x in insList]
	# make a the variable 'tr'
	tr = [x for x in range(1, n_tr+1)]
	# make a column for subject id
	subject = [SUB]*n_tr
	# make a numpy matrix
	matrix = pd.DataFrame(
		{'tr' : tr,
		'subject' : subject,
		'choice' : choice,
		'mpfc' : mpfc,
		'nacc' : nacc,
		'ins' : ins}
		)
	# row-wise stacking of the matrix for this SUB to the dataframe
	df = pd.concat([df, matrix])
	print("{} data added".format(SUB))

if len(df) == n_tr*len(SUBJECTS):
    print("Dataframe has been successfully made for all subjects.")

# inspect datafrmae
df.head(10)

# save out the dataframe as a csv file
np.savetxt("df_pd.csv", df, fmt="%s", delimiter=",")


# prepping the data some more
""" 
since I only want to use the anticipation phase of each trial to predict choice, 
I'll subset only those timepoints
"""
dfAnt = df[df.choice != 0]

# create arrays for the features (X) and for target variable (y)
X = dfAnt[['mpfc', 'nacc', 'ins']]
y = dfAnt['choice']


###################################
#             plot 
###################################
print("############\n PLOTTING DATA\n###########\n (Must close the popped-up plots to continue with the script)")

# plotting the points  
plt.scatter(dfAnt.choice, dfAnt.nacc)   
# naming the x axis 
plt.xlabel('Choice of the risky option') 
# naming the y axis 
plt.ylabel('% BOLD change (NAcc)') 
# giving a title to my graph 
plt.title('Nucleus Accumbens')  
# function to show the plot 
plt.show() 

# feature 2: ins
plt.scatter(dfAnt.choice, dfAnt.ins)
plt.xlabel('Choice of the risky option') 
plt.ylabel('% BOLD change (Ant. Insula)') 
plt.title('Anterior Insula')  
plt.show()

# feature 3: mpfc
plt.scatter(dfAnt.choice, dfAnt.mpfc)
plt.xlabel('Choice of the risky option') 
plt.ylabel('% BOLD change (mPFC)') 
plt.title('Medial Prefrontal Cortex')  
plt.show()


###################################
#        classification
###################################

print("############\n CLASSIFICATION\n ###########")

# make a training and test set (80-20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 41)


##### SVC with a linear kernel ######
# make a linear classifier
linClf = svm.SVC(kernel = "linear")

# fit the linear classifier on the train set
linClf.fit(X_train, y_train)

# predict choice (y) for the test set
y_pred = linClf.predict(X_test)

print("SVM classifier with linear kernel:")
# evaluate model accuracy
print(" - Model accuracy:", metrics.accuracy_score(y_test, y_pred))

##### SVC with a gaussian kernel (using a RBF or radial basis function) ######
# (rbf is the default)
rbf = svm.SVC(kernel = "rbf") 

# search for the svm classification parameters that maximize cross-validation accuracy
#(parameters: gamma and C)
#(gamma: higher values higher accuracy but danger of overfitting)
#(C: trade-off between simplicity and accuracy; lower values encourage a simpler function at the cost of accuracy)
# define different values of gamma and C
parameters = {'gamma':[0.00001, 0.0001, 0.001, 0.01, 0.1], 'C':[0.1, 1, 10]}
searcher = GridSearchCV(rbf, parameters)

# fit the classifier using the gamma that yield highest accuracy
searcher.fit(X_train, y_train)

print("SVM classifier with RBF kernel:")
# what were the best cross-validation parameters?
print(" - Model accuracy (best CV accuracy):", searcher.best_score_)
print(" - Model accuracy (best grid search hypers):", searcher.score(X_test, y_test))
print(" - CV parameters (best CV):", searcher.best_params_)