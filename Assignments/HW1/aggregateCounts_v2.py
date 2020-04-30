#!/usr/bin/env python
"""
This script reads word counts from STDIN and aggregates
the counts for any duplicated words.

INPUT & OUTPUT FORMAT:
    word \t count
USAGE (standalone):
    python aggregateCounts_v2.py < yourCountsFile.txt

Instructions:
    For Q7 - Your solution should not use a dictionary or store anything   
             other than a single total count - just print them as soon as  
             you've added them. HINT: you've modified the framework script 
             to ensure that the input is alphabetized; how can you 
             use that to your advantage?
"""

# imports
import sys
from collections import defaultdict


################# YOUR CODE HERE #################

prevWord = None
prevCount = 0

counts = defaultdict(int)
# stream over lines from Standard Input
for line in sys.stdin:
    # extract words & counts
    word, count  = line.split()
    
    if prevWord is None or word == prevWord:
        prevCount += int(count)
    else:
        print(prevWord + '\t' + str(prevCount))
        prevCount = int(count)
        
    prevWord = word
    
if prevCount > 0:
    print(prevWord + '\t' + str(prevCount))
    










################ (END) YOUR CODE #################
