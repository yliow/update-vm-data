#!/usr/bin/env python
import os, sys, glob
from pyutil import *
from latextool_basic import make_c, getassessment

def system(cmd):
    print(">>>>", cmd)
    return subprocessrun(cmd, shell=True, check=True)

def build_upload(y=True, # True: delete old 'q0101'
):
    assessment = getassessment() # example 'q0101'
    if os.path.isdir(assessment):
        # if every file in q0101/ is in questions/ can remove q0101/
        if y:
            p = subprocessrun('rm -rf %s' % assessment, shell=True)
        else:
            for f in glob.glob('%s/*' % assessment):
                g = os.path.split(f)[-1]
                g = os.path.join('questions', g)
                p = subprocessrun('diff %s %s' % (f, g), check=False, shell=True)
                if p.returncode != 0 or p.stdout != '':
                    print("abort ... delete %s first" % assessment)
                    sys.exit()
            p = subprocessrun('rm -rf %s' % assessment, shell=True)

    # to be safe build_upload will remake main.pdf (redundant?)
    system("cd questions && make cc && make main.pdf && make c") # why thispreamble.tex.old appears???
    print("0 .... questions:", flush=True)
    os.system("cd questions && ls -la")
    make_c(dir_='questions')
    if not os.path.isfile('questions/main.pdf'):
        raise Exception('questions/main.pdf not found')
    system("rm -rf %s %s.tar %s.tar.gz" % (assessment, assessment, assessment))
    system('mkdir %s' % assessment)
    system('cp -r questions/* %s' % assessment)
    system("tar -cvf %s.tar %s" % (assessment, assessment))
    os.system("gzip %s.tar" % assessment)
    if not os.path.isfile('%s.tar.gz' % assessment):
        raise Exception('%s.tar.gz not found' % assessment)
    
    #print(">>>> created %s.tar.gz" % assessment)
    os.system("rm -rf %s" % assessment)             # rm -rf q0101
    #p = system('tar -ztvf %s.tar.gz' % assessment)
    #print(p.stdout)
    
if __name__ == '__main__':
    build_upload()
