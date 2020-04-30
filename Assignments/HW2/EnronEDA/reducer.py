#!/usr/bin/env python
"""
Reducer takes words with their class and partial counts and computes totals.
INPUT:
    word \t class \t partialCount 
OUTPUT:
    word \t class \t totalCount  
"""
import re
import sys

# initialize trackers
current_word = None
spam_count, ham_count = 0,0

# read from standard input
for line in sys.stdin:
    # parse input
    word, is_spam, count = line.split('\t')
    
############ YOUR CODE HERE #########


    if word == current_word or current_word is None:
        if is_spam == '1':
            spam_count += int(count)
        else:
            ham_count += int(count)
    else:
        print(current_word + '\t' + '1' + '\t' + str(spam_count))
        print(current_word + '\t' + '0'  + '\t' + str(ham_count))
        if is_spam == '1':
            spam_count = int(count)
            ham_count = 0
        else:
            spam_count = 0
            ham_count = int(count)
    
    current_word = word

print(current_word + '\t' + '1' + '\t' + str(spam_count))
print(current_word + '\t' + '0'  + '\t' + str(ham_count))
















############ (END) YOUR CODE #########