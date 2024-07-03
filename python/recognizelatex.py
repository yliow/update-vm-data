#!/usr/bin/python
"""
Add %-*-latex-*- to tex files 
"""
from pyutil import *
import glob
fs = glob.glob('./**/*.tex', recursive=True)
for f in fs:    
    s = readfile(f)
    if not s.startswith('%-*-latex-*-'):
        s = '%-*-latex-*-\n' + s
        writefile(f, s)
        print('changed:', f)
        
