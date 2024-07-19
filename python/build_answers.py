#!/usr/bin/env python
import os
from pyutil import *
from latextool_basic import *

def build_answers(questions_path='./questions/',
                  answers_path='./answers/',
                  answers=None, # dictionary
                  answers_py_path ='./answers.py', # path of answers.py
                  src="./answers/main.tex", dest="./answers/main.tex"):
    os.system('rm -rf %s' % answers_path)
    os.system('mkdir %s' % answers_path)
    os.system('cp -r %s %s' % (os.path.join(questions_path, '*'), answers_path))
    if answers == None:
        # will the following accidentally corrupt some variables?
        s = readfile(answers_py_path)
        locals_ = locals()
        exec(s, globals(), locals_)
        answers = locals_["answers"]
        #print("answers:", answers)
    addanswertolatex(answers, src=src, dest=dest)
    subprocessrun('cd %s && make no_v' % answers_path, shell=True, check=True)
    make_c('answers')
    
    print(">>>> created answers/")
    os.system('ls -la answers')

if __name__ == '__main__':
    build_answers()

