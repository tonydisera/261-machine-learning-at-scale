#!/usr/bin/env python
"""

"""

import sys
for line in sys.stdin:
    line = line.strip()
    partion_key, word, is_spam, count = line.split('\t')
    print(f'{word}\t{is_spam}\t{count}')
