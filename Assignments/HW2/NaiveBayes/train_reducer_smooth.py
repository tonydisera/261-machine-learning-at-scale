#!/usr/bin/env python
"""
Reducer aggregates word counts and uses word counts by class along with vocab size to arrive at a smoothed word frequency.

INPUT:                                               
    word \t class0_partialCount,class1_partialCount       
OUTPUT:
    word \t class0_count,class1_count,class0_frequency,class1_frequency
    
    ** NOTE **
    The first input records encountered will have keys that represent the
    total document count, total document count, and vocabulary size (total number of
    unique words).  We will aggregate these totals to arrive 
    which we will use to calculate the smoothed frequencies.  
       
    At the end, we will emit a single record with the key 'ClassPriors', containing
    the total documents for each class and the document frequencies for each class.
    
Instructions:
    Again, you are free to design a solution however you see 
    fit as long as your final model meets our required format
    for the inference job we designed in Question 8. Please
    comment your code clearly and concisely.
    
    A few reminders: 
    1) Don't forget to emit Class Priors (with the right key).
    2) In python2: 3/4 = 0 and 3/float(4) = 0.75
"""
##################### YOUR CODE HERE ####################
import sys   
import os
import string

# initialize trackers
current_word = None
class0_count, class1_count = 0.0,0.0
class0_total_word_count, class1_total_word_count = float(0),float(0)
class0_total_doc_count, class1_total_doc_count = float(0),float(0)

# load the vocab size from a local file
vocab_size = None
for record in open('vocab_size.txt', 'r').readlines():
    vocab_size = int(record)
if vocab_size is None:
    print("Problem encountered.  Vocab size file not found.")


def get_smooth_freq(word_count, total_word_count, vocab_size):
    return (word_count+1)/(total_word_count+vocab_size)

# read from standard input
for line in sys.stdin:
    # parse input
    tokens = line.split('\t')
    partitionKey = tokens[0]
    word         = tokens[1]
    value        = tokens[2]

    value_tokens = value.split(",")
    class0_partial_count = value_tokens[0]
    class1_partial_count = value_tokens[1]
    
    
    # Sum the counts for the same word
    if current_word is None or (word == current_word):
        class0_count += float(class0_partial_count)
        class1_count += float(class1_partial_count)
        
    else:
        # We have encountered a new word...
        
        # The first records will be the total word and doc counts.  Don't emit these;
        # instead keep track of these counts.  We will use these to calculate
        # word and doc frequencies
        if current_word == '**total_word_count':
            class0_total_word_count = float(class0_count)
            class1_total_word_count = float(class1_count)
        elif current_word == '**total_doc_count':
            class0_total_doc_count = float(class0_count)
            class1_total_doc_count = float(class1_count)
        # Emit the record for the word counts and frequencies
        # for the class0 and class1 and store the current
        # word's counts
        else:
            class0_freq = get_smooth_freq(class0_count, class0_total_word_count, vocab_size)
            class1_freq = get_smooth_freq(class1_count, class1_total_word_count, vocab_size)


            print(current_word 
                    + '\t' + str(class0_count) 
                    + ','  + str(class1_count)
                    + ','  + str(class0_freq)
                    + ','  + str(class1_freq))
            
        class0_count = float(class0_partial_count)
        class1_count = float(class1_partial_count)
    
    current_word = word


# Emit the counts and frequencies for the last word in the file
if (current_word != '**total_word_count' and current_word != '**total_doc_count'):
    class0_freq = get_smooth_freq(class0_count, class0_total_word_count, vocab_size)
    class1_freq = get_smooth_freq(class1_count, class1_total_word_count, vocab_size)
    print(current_word 
        + '\t' + str(class0_count) 
        + ','  + str(class1_count)
        + ','  + str(class0_freq)
        + ','  + str(class1_freq))


# Emit ClassPrior record only once across all partitions 
class0_doc_freq = 0
class1_doc_freq = 0
if partitionKey == 'A':
    if class0_total_doc_count > 0:
        class0_doc_freq = class0_total_doc_count / (class0_total_doc_count+class1_total_doc_count)
    if class1_total_doc_count > 0:
        class1_doc_freq = class1_total_doc_count / (class0_total_doc_count+class1_total_doc_count)
    print('ClassPriors'
                + '\t' + str(class0_total_doc_count) 
                + ',' +  str(class1_total_doc_count)
                + ',' +  str(class0_doc_freq)
                + ',' +  str(class1_doc_freq))



#################### (END) YOUR CODE ###################