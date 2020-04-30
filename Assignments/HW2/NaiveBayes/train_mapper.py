#!/usr/bin/env python
"""
Mapper reads in text documents and emits word counts by class.
INPUT:                                                    
    DocID \t true_class \t subject \t body                
OUTPUT:                                                   
    partitionKey \t word \t class0_partialCount,class1_partialCount       
    

Instructions:
    You know what this script should do, go for it!
    (As a favor to the graders, please comment your code clearly!)
    
    A few reminders:
    1) To make sure your results match ours please be sure
       to use the same tokenizing that we have provided in
       all the other jobs:
         words = re.findall(r'[a-z]+', text-to-tokenize.lower())
         
    2) Don't forget to handle the various "totals" that you need
       for your conditional probabilities and class priors.
       
Partitioning:
    In order to send the totals to each reducer, we need to implement
    a custom partitioning strategy.
    
    We will generate a list of keys based on the number of reduce tasks 
    that we read in from the environment configuration of our job.
    
    We'll prepend the partition key by hashing the word and selecting the
    appropriate key from our list. This will end up partitioning our data
    as if we'd used the word as the partition key - that's how it worked
    for the single reducer implementation. This is not necessarily "good",
    as our data could be very skewed. However, in practice, for this
    exercise it works well. The next step would be to generate a file of
    partition split points based on the distribution as we've seen in 
    previous exercises.
    
    Now that we have a list of partition keys, we can send the totals to 
    each reducer by prepending each of the keys to each total.
       
"""

import re                                                   
import sys                                                  
import numpy as np      

from operator import itemgetter
import os



#################### YOUR CODE HERE ###################
import string

class0_word_count, class1_word_count = 0,0 
class0_doc_count, class1_doc_count = 0,0


# determine how many reduce jobs we will use
partition_count = int(os.environ["mapreduce_job_reduces"])

alpha_keys = string.ascii_lowercase.upper()
partition_keys = alpha_keys[0:partition_count]


def makeKeyHash(key, num_reducers):
    byteof = lambda char: int(format(ord(char), 'b'), 2)
    current_hash = 0
    for c in key:
        current_hash = (current_hash * 31 + byteof(c))
    return current_hash % num_reducers

def get_partition_key(word, partition_count):
    return partition_keys[makeKeyHash(word, partition_count)]


#
# Mapper code - emit key,value for each word indicate the count 
# of 1 for each class0 or class1.  Also emit the total word
# count and doc count.  We use a partition key to
# separate the keys into different partitions and to copy
# all word and doc counts across all partitions.
#

# read from standard input
for line in sys.stdin:
    # parse input
    docID, _class, subject, body = line.split('\t')
    # tokenize
    words = re.findall(r'[a-z]+', str(subject + ' ' + body).lower())
    
    # for each word...
    for word in words:
        
        # increment the counter for the corresponding class
        if _class == '0':
            print(get_partition_key(word,partition_count) + '\t' + word + '\t' + '1,0')
            class0_word_count += 1
        else:
            print(get_partition_key(word,partition_count) + '\t' + word + '\t' + '0,1')
            class1_word_count += 1
    
    if _class == '0':
        class0_doc_count += 1
    else:
        class1_doc_count += 1

# Emit total word and document counts across all partitions
for partition_key in partition_keys:
    print(partition_key + '\t' + "**total_word_count" + '\t' + str(class0_word_count) + "," + str(class1_word_count))
    print(partition_key + '\t' + "**total_doc_count"  + '\t' + str(class0_doc_count)  + "," + str(class1_doc_count))
    
    




























#################### (END) YOUR CODE ###################