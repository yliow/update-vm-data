#!/usr/bin/python
#check latex-templates/book

import os
from pyutil import *

substrs = {r'\section{': [], # list of filenames to ignore
           r'\input{solutions.tex}': [],
           }
for root, subdirs, filenames in os.walk('.'):
    for filename in filenames:
        if filename.endswith('tex'):
            fullpath = os.path.join(root, filename)
            #print(fullpath)
            s = readfile(fullpath)
            for key in substrs:
                if key in s and filename not in substrs[key]:
                    print("%s: %s found" % (fullpath, key))
