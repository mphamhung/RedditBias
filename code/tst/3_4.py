import numpy as np
from scipy import stats

def accuracy(mat):
    return float(np.trace(mat))/float(np.sum(mat))
    
def precision(mat):
    #only works for 2x2 matrices, i.e. 2 classes
    col_sums = np.sum(mat, axis=0)
    return [float(mat[0][0])/float(col_sums[0]), float(mat[1][1])/float(col_sums[1])]

def recall(mat):
    #only works for 2x2 matrices, i.e. 2 classes
    row_sums = np.sum(mat, axis=1)
    return [mat[0][0]/float(row_sums[0]), mat[1][1]/float(row_sums[1])]

def print_results(a, acc_mat):
    print ("Accuracy: " + str(round(accuracy(a)*100, 2)) + "%")
    acc_mat.append(round(accuracy(a)*100, 2))
    print ("Precision:\n    Class 0: " + str(round(precision(a)[0]*100, 2)) + "%    Class 4: " + str(round(precision(a)[1]*100, 2)) + "%")
    print ("Recall:\n   Class 0: " + str(round(recall(a)[0]*100, 2)) + "%   Class 4: " + str(round(recall(a)[1]*100, 2)) + "%")

acc_mat_SVM = []
acc_mat_Bayes = []
acc_mat_trees = []

print ("\nResults for partition 1:")
print_results(np.array([[685, 315], [411, 589]]), acc_mat_SVM)

print ("\nResults for partition 2:")
print_results(np.array([[669, 331], [430, 570]]), acc_mat_SVM)

print ("\nResults for partition 3:")
print_results(np.array([[685, 315], [445, 555]]), acc_mat_SVM)

print ("\nResults for partition 4:")
print_results(np.array([[686, 314], [434, 566]]), acc_mat_SVM)

print ("\nResults for partition 5:")
print_results(np.array([[675, 325], [403, 597]]), acc_mat_SVM)

print ("\nResults for partition 6:")
print_results(np.array([[661, 339], [390, 610]]), acc_mat_SVM)

print ("\nResults for partition 7:")
print_results(np.array([[674, 326], [414, 586]]), acc_mat_SVM)

print ("\nResults for partition 8:")
print_results(np.array([[681, 319], [419, 581]]), acc_mat_SVM)

print ("\nResults for partition 9:")
print_results(np.array([[598, 402], [404, 596]]), acc_mat_SVM)

print ("\nResults for partition 10:")
print_results(np.array([[608, 392], [408, 592]]), acc_mat_SVM)


#Using result for Bayes
a = np.array([[634, 366], [386, 614]])
acc_mat_Bayes.append(round(accuracy(a)*100, 2))

a = np.array([[673, 327], [407, 593]])
acc_mat_Bayes.append(round(accuracy(a)*100, 2))

a = np.array([[629, 371], [419, 581]])
acc_mat_Bayes.append(round(accuracy(a)*100, 2))

a = np.array([[697, 303], [431, 569]])
acc_mat_Bayes.append(round(accuracy(a)*100, 2))

a = np.array([[587, 413], [374, 626]])
acc_mat_Bayes.append(round(accuracy(a)*100, 2))

a = np.array([[613, 387], [381, 619]])
acc_mat_Bayes.append(round(accuracy(a)*100, 2))

a = np.array([[694, 306], [441, 559]])
acc_mat_Bayes.append(round(accuracy(a)*100, 2))

a = np.array([[649, 351], [405, 595]])
acc_mat_Bayes.append(round(accuracy(a)*100, 2))

a = np.array([[543, 457], [382, 618]])
acc_mat_Bayes.append(round(accuracy(a)*100, 2))

a = np.array([[582, 418], [405, 595]])
acc_mat_Bayes.append(round(accuracy(a)*100, 2))


#Using result for Decision Trees
a = np.array([[591, 409], [438, 562]])
acc_mat_trees.append(round(accuracy(a)*100, 2))

a = np.array([[583, 417], [390, 610]])
acc_mat_trees.append(round(accuracy(a)*100, 2))

a = np.array([[607, 393], [432, 568]])
acc_mat_trees.append(round(accuracy(a)*100, 2))

a = np.array([[569, 431], [413, 587]])
acc_mat_trees.append(round(accuracy(a)*100, 2))

a = np.array([[609, 391], [433, 567]])
acc_mat_trees.append(round(accuracy(a)*100, 2))

a = np.array([[529, 471], [408, 592]])
acc_mat_trees.append(round(accuracy(a)*100, 2))

a = np.array([[597, 403], [416, 584]])
acc_mat_trees.append(round(accuracy(a)*100, 2))

a = np.array([[587, 413], [415, 585]])
acc_mat_trees.append(round(accuracy(a)*100, 2))

a = np.array([[570, 430], [428, 572]])
acc_mat_trees.append(round(accuracy(a)*100, 2))

a = np.array([[587, 413], [408, 592]])
acc_mat_trees.append(round(accuracy(a)*100, 2))


print "\n\nAccuracy vectors for the three classifiers:\n"
print "SVMs:", acc_mat_SVM
print "Bayes:", acc_mat_Bayes
print "DTrees:", acc_mat_trees

p_1 = stats.ttest_rel(acc_mat_SVM, acc_mat_Bayes)
p_2 = stats.ttest_rel(acc_mat_SVM, acc_mat_trees)
p_3 = stats.ttest_rel(acc_mat_trees, acc_mat_Bayes)

print "\nSVM/Bayes p-val:", p_1[1]
print "DTrees/Bayes p-val:", p_2[1]
print "SVM/DTrees p-val:", p_3[1]