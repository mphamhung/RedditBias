from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import numpy as np
import argparse
import sys
import os

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix

import csv
from sklearn.utils import resample

from sklearn.model_selection import KFold
from scipy import stats

skipTraining = False
def accuracy( C ):
    ''' Compute accuracy given Numpy array confusion matrix C. Returns a floating point value '''
    correct = 0
    total = 0

    for i in range(len(C)):
        correct += C[i][i]
        total += C[i].sum()

    return correct/total

def recall( C ):
    ''' Compute recall given Numpy array confusion matrix C. Returns a list of floating point values '''
    recallScores = []
    
    for i in range(len(C)):
        recallScores.append(C[i][i]/sum(C[i,:]))
    
    return recallScores


def precision( C ):
    ''' Compute precision given Numpy array confusion matrix C. Returns a list of floating point values '''
    precisionScores = []
    
    for i in range(len(C)):
        precisionScores.append(C[i][i]/sum(C[:,i]))

    return precisionScores
    

classifiers = [0,1,2,3,4]
classifiers[0] = SVC(kernel = 'linear' ,max_iter = 1000)
classifiers[1] = SVC(gamma = 2, max_iter = 1000)
classifiers[2] = RandomForestClassifier(max_depth = 5, n_estimators = 10,verbose = True)
classifiers[3] = MLPClassifier(alpha = 0.05,verbose = True)
classifiers[4] = AdaBoostClassifier()
keys = ['linsvm','rbf','rfc','mlp','ada']

def class31(filename):
    ''' This function performs experiment 3.1
    
    Parameters
       filename : string, the name of the npz file from Task 2

    Returns:      
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes
       i: int, the index of the supposed best classifier
    '''
    data = np.load(filename)
    data = data[data.files[0]]
    print("splitting data")
    X_train, X_test, y_train, y_test = train_test_split([row[:-1] for row in data], [row[-1] for row in data], train_size = 0.8, random_state = 0)
    
    if skipTraining:
        return (X_train, X_test, y_train, y_test, 4)
    with open('a1_3.1.csv', 'w', newline = '') as csvfile:
        cwriter = csv.writer(csvfile)        
        #cwriter.writerow(['classifier id', 'accuracy', 'recall: 0' , 'recall: 1' , 'recall: 2' , 'recall: 3' , 'precision: 0','precision: 1','precision: 2','precision: 3', 'C' ])
        
        best = 0
        for num, key in enumerate(keys):
            print("Fitting " + key)
            classifiers[num].fit(X_train,y_train)
            print("Predicting " + key)
            y_pred = classifiers[num].predict(X_test)
            C = confusion_matrix(y_test, y_pred)
            
            perf = [accuracy(C)] + recall(C) + precision(C) 
            cwriter.writerow([num] + perf +  [e for row in C for e in row])
            
            if accuracy(C) > best:
                iBest = num
                best = accuracy(C) 
                
    print("The best classifer was: " + keys[iBest] + str(iBest))
    return (X_train, X_test, y_train, y_test, iBest)


def class32(X_train, X_test, y_train, y_test,iBest):
    ''' This function performs experiment 3.2
    
    Parameters:
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes
       i: int, the index of the supposed best classifier (from task 3.1)  

    Returns:
       X_1k: numPy array, just 1K rows of X_train
       y_1k: numPy array, just 1K rows of y_train
    '''
    sizes = [1000, 5000,10000,15000,20000]
    
    bestClassifier = classifiers[iBest]
    
    with open('a1_3.2.csv', 'w', newline = '') as csvfile:
        cwriter = csv.writer(csvfile)        
        #cwriter.writerow(sizes)
        
        accuracies = []
        for size in sizes:
            sampled_x_train, sampled_y_train = resample(X_train, y_train, n_samples = size, random_state = size)
            bestClassifier.fit(sampled_x_train, sampled_y_train)
            y_pred = bestClassifier.predict(X_test)
            C = confusion_matrix(y_test, y_pred)
            accuracies.append(accuracy(C))
            if size == 1000:
                X_1k, y_1k = sampled_x_train, sampled_y_train
            
        cwriter.writerow(accuracies)
    return (X_1k, y_1k)
    
def class33(X_train, X_test, y_train, y_test, iBest, X_1k, y_1k):
    ''' This function performs experiment 3.3
    
    Parameters:
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes
       i: int, the index of the supposed best classifier (from task 3.1)  
       X_1k: numPy array, just 1K rows of X_train (from task 3.2)
       y_1k: numPy array, just 1K rows of y_train (from task 3.2)
    '''
    
    numfeats = [5,10,20,30,40,50]
    with open('a1_3.3.csv', 'w', newline = '') as csvfile:
        cwriter = csv.writer(csvfile)        

        #cwriter.writerow(['32k training set'])
        #cwriter.writerow(['num Features', 'p-values'])
        print('32k training set')
        sum32 = 0
        for n in numfeats:
            print("{} features".format(n))
            selector = SelectKBest(k=n)
            X_new = selector.fit_transform(X_train, y_train)
            pp = selector.pvalues_

            featureIndices = selector.get_support(indices=True)
            print(featureIndices)
            cwriter.writerow([n] + [pp[i] for i in featureIndices])
            sum32 += sum([pp[i] for i in featureIndices])

        print('1k training set')
        sum1 = 0
        for n in numfeats:
            print("{} features".format(n))
            selector = SelectKBest(k=n)
            X_new = selector.fit_transform(X_train, y_train)
            pp = selector.pvalues_
            featureIndices = selector.get_support(indices=True)
            print(featureIndices)
            sum1 += sum([pp[i] for i in featureIndices])

        bestClassifier = classifiers[iBest]
        selector = SelectKBest(k=5)
        X_new_32k = selector.fit_transform(X_train, y_train)
        X_new_1k = selector.fit_transform(X_1k, y_1k)
        featureIndices = selector.get_support(indices=True).tolist()
        X_new_test = [[row[i] for i in featureIndices] for row in X_test]

        bestClassifier.fit(X_new_32k , y_train)
        y_pred = bestClassifier.predict(X_new_test)
        C = confusion_matrix(y_test, y_pred)
        acc_32k = accuracy(C)
    
        bestClassifier.fit(X_new_1k , y_1k)
        y_pred = bestClassifier.predict(X_new_test)
        C = confusion_matrix(y_test, y_pred)
        acc_1k = accuracy(C)
        
        cwriter.writerow([acc_1k,acc_32k])
        print(sum32, sum1)
    
def class34( filename, iBest ):
    ''' This function performs experiment 3.4
    
    Parameters
       filename : string, the name of the npz file from Task 2
       i: int, the index of the supposed best classifier (from task 3.1)  
        '''
    kf = KFold(n_splits = 5, shuffle = True, random_state = 0)
    data = np.load(filename)
    data = data[data.files[0]]
    X = [row[:-1] for row in data]
    y = [row[-1] for row in data]

    a = [[] for i in range(len(classifiers))]
    with open('a1_3.4.csv', 'w', newline='') as csvfile:
        cwriter = csv.writer(csvfile)

        for train_index, test_index in kf.split(X, y):
            X_train = [X[i] for i in train_index]
            X_test = [X[i] for i in test_index]
            y_train = [y[i] for i in train_index]
            y_test = [y[i] for i in test_index]

            accuracies = []
            for num, key in enumerate(keys):
                print("Fitting " + key)
                classifiers[num].fit(X_train, y_train)
                print("Predicting " + key)
                y_pred = classifiers[num].predict(X_test)
                C = confusion_matrix(y_test, y_pred)
                accuracies.append(accuracy(C))
                a[num].append(accuracy(C))
            cwriter.writerow(accuracies)
        p = []
        for num, key in enumerate(keys):
            if num == iBest:
                continue
            S = stats.ttest_rel(a[num], a[iBest])
            p.append(S)

        cwriter.writerow(p)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='aaa')

    parser.add_argument("-i", "--input", help="the input npz file from Task 2", required=True)
    args = parser.parse_args()

    # TODO : complete each classification experiment, in sequence.
    X_train, X_test, y_train, y_test,iBest = class31(args.input)
    X_1k, y_1k = class32(X_train, X_test, y_train, y_test,iBest)
    class33( X_train, X_test, y_train, y_test,iBest, X_1k, y_1k)
    class34(args.input, iBest)