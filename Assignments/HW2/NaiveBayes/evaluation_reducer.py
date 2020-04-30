#!/usr/bin/env python
"""
Reducer to calculate precision and recall as part
of the inference phase of Naive Bayes.
INPUT:
    ID \t true_class \t P(ham|doc) \t P(spam|doc) \t predicted_class
OUTPUT:
    precision \t ##
    recall \t ##
    accuracy \t ##
    F-score \t ##
         
Instructions:
    Complete the missing code to compute these^ four
    evaluation measures for our classification task.
    
    Note: if you have no True Positives you will not 
    be able to compute the F1 score (and maybe not 
    precision/recall). Your code should handle this 
    case appropriately feel free to interpret the 
    "output format" above as a rough suggestion. It
    may be helpful to also print the counts for true
    positives, false positives, etc.
"""
import sys
import numpy as np

# initialize counters
FP = 0.0 # false positives
FN = 0.0 # false negatives
TP = 0.0 # true positives
TN = 0.0 # true negatives
doc_count = 0.0

# read from STDIN
for line in sys.stdin:
    # parse input
    docID, class_, pHam, pSpam, pred = line.split()
    # emit classification results first
    print(line[:-2], class_ == pred)
    
    # then compute evaluation stats
    if class_ == pred:
        if pred == '0':
            TN += 1
        else:
            TP += 1
    else:
        if pred == '0':
            FN += 1
        else:
            FP += 1

    doc_count += 1
    
prec     = np.round(TP/(TP+FP),4)
recall   = np.round(TP/(TP+FN),4)
accuracy = np.round((TP+TN)/(TP+TN+FP+FN),4)
f1       = np.round(2*((prec*recall)/(prec+recall)),4)

print('# Documents'       + '\t' + str(doc_count))
print('True Positives'    + '\t' + str(TP))
print('True Negatives'    + '\t' + str(TN))
print('False Positives'   + '\t' + str(FP))
print('False Negatives'   + '\t' + str(FN))
print('Accuracy'          + '\t' + str(accuracy))
print('Precision'         + '\t' + str(prec))
print('Recall'            + '\t' + str(recall))
print('F-score'           + '\t' + str(f1))

        
#################### YOUR CODE HERE ###################























#################### (END) YOUR CODE ###################
    