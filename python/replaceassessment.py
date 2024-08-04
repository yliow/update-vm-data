#!/usr/bin/env python
import os, sys, glob
from pyutil import *

def replaceassessment(filename='thispreamble.tex'):
    ''' To replace q0000, Quiz in thispreamble.tex:
    
\newcommand\ASSESSMENT{q0000}
\newcommand\ASSESSMENTTYPE{Quiz}
    
    '''
    cwd = os.getcwd() # assume in .../q1234/questions/
    if cwd.find('/questions') == -1:
        raise Exception("'/questions' not found. cwd is '%s'." % cwd)
    a, _ = cwd.split('/questions') # a = '.../q1234'
    #print("a,_:", a,_)
    a0,a1 = os.path.split(a) # a1 = 'q1234'
    #print("a1:", a1)
    assessmenttype = a1[0]   # 'q'
    assessment = a1          # q1234
    d = {'q':'Quiz',
         'a':'Assessment',
         't':'Test',
         'f':'Final',
         'p':'Project',}
    if assessmenttype not in d:
        raise Exception("assessmenttype %s is not in %s. cwd is '%s'." % \
                        (assessmenttype, d.keys(), cwd))
    assessmenttype = d[assessmenttype]
    print("assessmenttype:", assessmenttype)
    print("assessment:", assessment)
    s = readfile(filename)
    lines = s.split('\n')
    tlines = lines[:]
    assessment_found = False
    assessmenttype_found = False
    for (i,line) in enumerate(lines):
        line = line.strip()
        if line.startswith(r'\newcommand\ASSESSMENT{') and line.endswith('}'):
            line = r'\newcommand\ASSESSMENT{%s}' % assessment
            tlines[i] = line
            assessment_found = True
        elif line.startswith(r'\newcommand\ASSESSMENTTYPE{') and line.endswith('}'):
            line = r'\newcommand\ASSESSMENTTYPE{%s}' % assessmenttype
            tlines[i] = line
            assessmenttype_found = True
    if not assessment_found:
        print("ASSESSMENT NOT FOUND!")
    if not assessmenttype_found:
        print("ASSESSMENTTYPE NOT FOUND!")
    s = '\n'.join(tlines)
    writefile(filename, s)
    
if __name__ == '__main__':
    replaceassessment()
    
