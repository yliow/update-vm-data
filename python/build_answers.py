#!/usr/bin/env python
import os, sys
from pyutil import *
from latextool_basic import *

def system(cmd):
    print(">>>>", cmd, flush=True)
    sys.stdout.flush()
    os.system(cmd)
    
def build_answers(questions_path='./questions/',
                  answers_path='./answers/',
                  answers=None, # dictionary
                  answers_py_path ='./answers.py', # path of answers.py
                  src="./answers/main.tex", dest="./answers/main.tex"):
    #print("build_answers", flush=True)
    cwd = os.getcwd()
    #print("1 ... cwd:", cwd, flush=True)
    system('rm -rf %s' % answers_path)
    system('mkdir %s' % answers_path)
    system('cp -r %s %s' % (os.path.join(questions_path, '*'), answers_path))
    print('>>>> cp -r %s %s' % (os.path.join(questions_path, '*'), answers_path), flush=True)
    if answers == None:
        #print("2 ... answers_py_path:", answers_py_path, flush=True)
        #print("3 ... answers.py?", os.path.isfile(answers_py_path), flush=True)
        ret = os.system('ls -la')
        #print("ret:", ret, flush=True)
        #print(" 4 ...", flush=True)
        #print("enter to cont ...", flush=True)
        #input("")
        # will the following accidentally corrupt some variables?
        if os.path.isfile(answers_py_path):
            sys.path.append(cwd)
            # "answers.py" exists
            dir_, _ = os.path.split(answers_py_path)
            if dir_ in ['', '.']:
                import answers as A
                answers = A.answers
            else:
                cwd0 = os.getcwd()
                os.chdir(dir_)
                from answers import answers
                os.chdir(cwd0)
        else:
            # no answers.py ... add a blank one
            s = ',\n'.join(['""' for _ in range(10)])
            s = ('answers = [%s]' % s).replace('\n', '\n' + 11*' ')
            writefile(answers_py_path, s)
            print(s)
            s = readfile(answers_py_path)
            #print(s)
            #input(" ... ")
            #locals_ = locals()
            #exec(s, globals(), locals_)
            answers = ['' for _ in range(10)]
                
    #print("answers:", answers, type(answers))
    #input()
    addanswertolatex(answers, src=src, dest=dest)

    # to be safe build_answer will remake main.pdf
    subprocessrun('cd %s && make cc && make main.pdf && make c' % answers_path, shell=True, check=True)
    
    make_c('answers')
    
    #print(">>>> created answers/")
    #os.system('ls -la answers')

if __name__ == '__main__':
    build_answers()

