#!/usr/bin/env python
"""
Mapper tokenizes and emits words with their class.
INPUT:
    ID \t SPAM \t SUBJECT \t CONTENT \n
OUTPUT:
    word \t class \t count 
"""
import re
import sys

# read from standard input
for line in sys.stdin:
    # parse input
    docID, _class, subject, body = line.split('\t')
    # tokenize
    #words = re.findall(r'[a-z]+', subject + ' ' + body)
    words = re.findall(r'[a-z]+', str(subject + ' ' + body).lower())
    
############ YOUR CODE HERE #########
    for word in words:
        print(word + '\t' + _class + '\t' + '1')
        


############ (END) YOUR CODE #########