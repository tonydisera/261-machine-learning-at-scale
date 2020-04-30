#!/usr/bin/env python
"""
Reducer aggregates word counts by class and emits frequencies.

INPUT:                                               
    partitionKey \t word \t class0_partialCount,class1_partialCount       
OUTPUT:
    word \t class0_count,class1_count,class0_frequency,class1_frequency
    
    ** NOTE the first input records encountered will have keys that represent the
       total_doc_count and total_word_count from all of the mappers.  These
       will be injected by a custom prepender.  We will aggregate these 
       totals to arrive at the total document count and total word count,
       which we will use to calculate the frequencies.  

    ** NOTE we will aggregate the word counts and calculate the word frequencies
       using the total_word_count calculate before we encounter the first records
       that are 'word' records.
       We will also emit a single records with the key 'ClassPriors', containing
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

# initialize trackers
current_word = None
class0_count, class1_count = 0,0
class0_total_word_count, class1_total_word_count = 0,0
class0_total_doc_count, class1_total_doc_count = 0,0
vocab_size = 0

partition_count = int(os.environ["mapreduce_job_reduces"])

# read from standard input
for line in sys.stdin:
    # parse input
    tokens = line.split('\t')
    partitionKey = tokens[0]
    word         = tokens[1]
    value        = tokens[2]
    class0_partial_count, class1_partial_count= value.split(",")
    
    # Sum the counts for the same word
    if word == current_word or current_word is None:
        class0_count += int(class0_partial_count)
        class1_count += int(class1_partial_count)
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
            class0_freq = class0_count/class0_total_word_count if class0_count > 0 and class0_total_word_count > 0 else 0
            class1_freq = class1_count/class1_total_word_count if class1_count > 0 and class1_total_word_count > 0 else 0
            print(current_word 
                      + '\t' +  str(class0_count) 
                      + ',' +  str(class1_count)
                      + ',' +  str(class0_freq)
                      + ',' +  str(class1_freq))
            vocab_size += 1
            
        class0_count = int(class0_partial_count)
        class1_count = int(class1_partial_count)
    
    current_word = word

# Emit the counts and frequencies for the last word in the file
if (current_word != '**total_word_count' and current_word != '**total_doc_count'):
    print(current_word 
         + '\t' +  str(class0_count) 
         + ',' +  str(class1_count)
         + ',' +  str(class0_count/class0_total_word_count if class0_count > 0 and class0_total_word_count > 0 else 0)
         + ',' +  str(class1_count/class1_total_word_count if class1_count > 0 and class1_total_word_count > 0 else 0))
    vocab_size += 1
    

# Now emit ClassPrior record.  We only need to emit this in one instance of the reducer, so 
# use the partition key to detect if we are on the first reducer
class0_doc_freq = 0
class1_doc_freq = 0
if class0_total_doc_count > 0:
    class0_doc_freq = class0_total_doc_count / (class0_total_doc_count+class1_total_doc_count)
if class1_total_doc_count > 1:
    class1_doc_freq = class1_total_doc_count / (class0_total_doc_count+class1_total_doc_count)
if partitionKey == 'A' or partition_count == 1:
    print('ClassPriors'  
            + '\t' + str(class0_total_doc_count) 
            + ',' +  str(class1_total_doc_count)
            + ',' +  str(class0_doc_freq)
            + ',' +  str(class1_doc_freq))


##################### (END) CODE HERE ####################