Reading your mind: Predicting choice based on brain activity

Leili Mortazavi
March 13, 2020


Overview:
I am using machine learning to classify brain activity – measured by Functional Magnetic Resonance Imaging – and to predict what the person is about to choose on a gambling task.    

The data in this project comes from a study where participants chose to take a gamble or not while being scanned using functional MRI (fMRI). They were presented with two options in each of the 72 trials, where they had to choose to take a gamble for real money or choose a safe no-risk/no-outcome option. 

To do this, I am taking the average fMRI signal from 3 brain regions (preprocessed and normalized to percent change) at the first two seconds of observing the options but before making a choice (i.e. the anticipation phase). There were 432 acquisition timepoints during the task, each of which take 2 seconds. 

Data:
- 'bactive-epi-f_{ROI}.1D': Data from each of the 3 regions of interest (ROIs) are in a separete 1D file in each of the 20 subjects' directories. 

- 'achoosepos.1D': Information about the choice of participants in each trial. It contains 0, 1, or -1. 0 denotes all timepoints that are of no interest to us (i.e. all non-anticipation timepoints). 1 denotes anticipation period of trials where they chose to take a risk, and -1 for those, where they chose the safe option. 

Code: 
The code uses pandas library to import all of these 1D files and organize them in a tidy daraframe format. 

Then it makes a scatterplot for each ROI. 

Then it uses sickit learn package to make 2 separate classifiers. For each one, it trains the model on 80% of the data, tests it on the remaining 20%, and reports the results. The first classifier uses a linear kernel and the second one uses a gaussian kernel. 





