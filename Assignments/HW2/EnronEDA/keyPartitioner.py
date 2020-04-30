#!/usr/bin/env python
"""
Key partioner
INPUT:
    word \t class \t partialCount 
"""

import sys
for line in sys.stdin:
    line = line.strip()
    word, is_spam, count = line.split('\t')
    if is_spam == '1':
        key = "A"
    else:
        key = "B"
    print(f'{key}\t{word}\t{is_spam}\t{count}')
