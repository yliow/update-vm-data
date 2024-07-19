#!/usr/bin/python3

"""
myqtmake
Utility for building C++ Qt executables.
Y.Liow

Description:
myqtmake will
- Create project file (NOTE: All *.o and *.pro will be removed)
- Add 'QT += core gui widgets' to project file
- Create Makefile
- Create executable
- Run executable

Usage:
Run "myqtmake.py" as a script or execute using python2/python3 in the
Qt project directory.
"""

import os, sys, glob

def readfile(filename):
    f = open(filename, 'r')
    s = f.read();
    f.close()
    return s
def writefile(filename, s):
    f = open(filename, 'w')
    f.write(s)
    f.close()
def system(cmd):
    print('    $ %s' % cmd)
    os.system(cmd + " 2>stderr.txt")
    stderr = readfile('stderr.txt').strip()
    os.system('rm -f stderr.txt')
    if stderr:
        print(stderr)
        sys.exit()
    return stderr

def find_unique_pro_filename():
    filenames = glob.glob('*.pro')
    if len(filenames) == 0:
        print("Project file not found")
        sys.exit()
    elif len(filenames) > 1:
        print("Number of project files is > 1")
        sys.exit()
    else:
        pro_filename = filenames[0]
    return pro_filename

def make_project_file():
    print("Creating project file ...")
    system('rm -f *.pro *.o')
    system('qmake-qt5 -project')
    return find_unique_pro_filename()
    
def add_to_QT(pro_filename=None, qt = 'gui widgets'):
    print("Adding 'QT += %s' to project file ..." % qt)
    if not pro_filename:
        pro_filename = find_unique_pro_filename()
    else:
        if not pro_filename.endswith('.pro'):
            print("pro_filename %s does not end with .pro" % pro_filename)
            sys.exit()
    filename = pro_filename
    s = readfile(filename)
    lines = s.split('\n')
    tlines = []
    for line in lines:
        if line.startswith('INCLUDEPATH'):
            tlines.append(line)
            tlines.append('QT += %s' % qt)
            tlines.append('CONFIG += qt console debug') # console printing
            tlines.append('OUTPUT += Console')
        else:
            tlines.append(line)
    s = '\n'.join(tlines)
    writefile(filename, s)

def make_Makefile(pro_filename):
    print("Creating Makefile ...")
    filename_wo_pro = pro_filename.replace('.pro', '')
    system('qmake-qt5 %s' % pro_filename)
    s = readfile('Makefile').strip()
    s += '\n\nr:\n\texport "QT_LOGGING_RULES=*.debug=true";./%s\n' % \
         filename_wo_pro
    s += '\n\nc:\n\trm -f %s *.o core *.core main*.jpg moc_*' % filename_wo_pro
    s += '\n\nmain.jpg:\n\txcapture ' \
        '--program=%s --window=Qt --filename=main.jpg' % \
        filename_wo_pro
    writefile('Makefile', s)

def make_executable(filename_wo_pro):
    print("Calling make ...")
    system('rm -f %s' % filename_wo_pro)
    system('make')
    if not os.path.exists(filename_wo_pro):
        print("executable '%s' not created" % filename_wo_pro)
        sys.exit()

def run_executable():
    print("Running executable ...")
    system('make r')

def main():
    pro_filename = make_project_file()
    add_to_QT(pro_filename=pro_filename, qt='core gui widgets')
    make_Makefile(pro_filename=pro_filename)
    filename_wo_pro = pro_filename.replace('.pro', '')
    make_executable(filename_wo_pro=filename_wo_pro)
    run_executable()

if __name__ == '__main__':
    main()
