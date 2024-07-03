#!/usr/bin/env python 
"""
Copies relevant quiz/* to a questions/ directory of a course.

quiz/
    answers.py -- a dummy one
    makefile
    parser.py
    questions/instructions.tex
    questions/latexcircuit.py
    questions/latextool_basic.py
    questions/makefile
    questions/thispreamble.tex
    questions/main.tex

USAGE:

    * assume cwd is cissxxx/q/q1234/
    * run makequiz.py
      python /home/student/yliow/Documents/work/projects/latex-templates/makequiz.py
      which will
      * copy above files into cissxxx/q/q1234/. Omit main.tex if exists.
      * substitute the "cissxxx" into thispreamble.tex
      * substitute the "q1234" into thispreamble.tex

"""

import sys, os, shutil, re
from pyutil import *

DIR = '/home/student/yliow/Documents/work/projects/latex-templates/quiz/template/'

def __dir__(x):
    """ return dir of this source file """
    return os.path.dirname(os.path.abspath(__file__))
    
# >>> FROM ALEX05
def getdefaultcourse():
    # get ciss??? or math??? from path
    p = re.compile(r'/((ciss|math)\d\d\d)(/|$)')
    s = os.getcwd()
    srch = p.search(s)
    if srch != None:
        return srch.group(1)
    else:
        return None
def getdefaultassessment():
    p = re.compile('/((a|q|p|t)[0-9]+[-0-9a-z]*)')
    s = os.getcwd()
    srch = p.search(s)
    t = None
    if srch != None:
        return srch.group(1)
    else:
        for root, dirs, files in os.walk('.'):
            for dir_ in dirs:
                path = os.path.abspath(dir_)
                srch = p.search(path)
                if srch != None:
                    return srch.group(1)
            break
        return None

def makequiz():
    """
    -- if cwd does not contain "cissxxx/q/qxxxxx" or "mathxxx/q/qxxxxx",
       exception thrown
    -- if "cissxxx/q/qxxxxx" or "cissxxx/q/qxxxxx" in cwd, make a backup
       copy of "cissxxx/q/qxxxxx" to "cissxxx/q/qxxxxx-backup-0".
       If this exists, backup to "cissxxx/q/qxxxxx-backup-1". Etc.

    ADDED: This should be executed in a quiz directory, i.e., the directory
    has to similar to
    ".../ciss240/q/q0101", i.e., .../[course]/[assessment-type]/[assessment]
    Otherwise it will halt.
    """
    course = getdefaultcourse()
    assessment = getdefaultassessment()
    assessment_type = assessment[0]
    cwd = os.getcwd()
    print("course:", course)
    print("assessment:", assessment)
    print("cwd:", cwd)
    if not course and not assessment:
        raise ValueError("invalid course or invalid assessment ... halting")
    correct_cwd_end = "%s/%s/%s" % (course, assessment_type, assessment)
    if not cwd.endswith(correct_cwd_end):
        raise ValueError('cwd does not end wih "%s" ... halting' % correct_cwd_end)
        
    backup("questions")
    backup("answers.py")
    #return;
    
    s = r'''
    answers.py
    makefile
    parser.py
    questions/instructions.tex
    questions/latexcircuit.py
    questions/latextool_basic.py
    questions/makefile
    questions/thispreamble.tex
    questions/thispackages.tex
    questions/thismacros.tex
    questions/thispostamble.tex
    questions/main.tex
    '''.strip()
    lines = [line.strip() for line in s.split('\n') \
             if line.strip() != '']
    lines0 = [os.path.join(DIR, line) \
              for line in lines]                # lines0 = abs paths
    lines1 = lines[:]                           # lines1 = relative paths

    # t = files to straight copy
    t = ['makefile',
         'parser.py',
         'instructions.tex',
         'latexcircuit.py',
         'latextool_basic.py',
         'makefile',
         'thispreamble.tex',
         'thispackages.tex',
         'thismacros.tex',
         'thispostamble.tex',
    ]
    
    if not os.path.isdir('questions'):
        print('questions/ not found ... creating ...', flush=True)
        mkdir('questions')
        
    for line0,line1 in zip(lines0, lines1):
        # Copy from latex-templates to current directory, except that
        # for files in questions/, make a copy if the file exists

        print()
        print("line0:", line0)
        print("line1:", line1)
        straight_cp = any([line0.endswith(_) for _ in t])
        print("straight_cp:", straight_cp)

        if straight_cp:
            cp(line0, line1, verbose=True)            
        else:
            if os.path.exists(line1):
                if difffiles(line0, line1) != '':
                    if os.path.exists(line1 + '.old'):
                        if difffiles(line1, line1 + '.old') != '':
                            print('ERROR: %(line1)s exists and different from %(line1)s.old ... halting' % {'line1':line1})
                            sys.exit()
                        else:
                            # line1 and line1.old are the same
                            print("%(line1)s and %(line1)s.old are the same" % {'line1':line1})
                            cp(line0, line1, verbose=True)
                    else:
                        mv(line1, line1 + '.old', verbose=True)
                        cp(line0, line1, verbose=True)
                else:
                    # line0 and line1 are the same
                    print("%s already found ... no copy" % line1) 
                    pass    
            else:
                cp(line0, line1, verbose=True)
    
        # For thispreamble.tex, replace course and assessment field
        if line1.endswith('thispreamble.tex'):
            course = getdefaultcourse()
            assessment = getdefaultassessment()
            print(">>> course:", course)
            print(">>> assessment:", assessment)
            s = readfile(line1)
            if course != None:
                old = r'\newcommand\COURSE{ciss240}'
                new = r'\newcommand\COURSE{%s}' % course
                s = s.replace(old, new)
            if assessment != None:
                old = r'\newcommand\ASSESSMENT{q0000}'
                new = r'\newcommand\ASSESSMENT{%s}' % assessment
                s = s.replace(old, new)
            writefile(line1, s)

if __name__ == '__main__':
    makequiz()
