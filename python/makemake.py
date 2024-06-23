#!/usr/bin/python
"""
Create makefile

* If makefile, abort, unless "-f" is specified. In that case original makefile
is renamed as makefile.old  
"""
import glob, os, sys, getopt, shutil
import re
import datetime


def qnum_makefile():
    print("makefile to create q??.tar.gz")
    # makefile for q01, ... 
    makefile = r'''curdir := $(notdir $(CURDIR))

run:
	cd questions; make; rm -f main-*-*-*.tex main.aux main.idx main.log main.out makefile.old main.py main.py.err main.py.out latex.py submit.tar.gz; rm -rf submit
	rm -rf $(curdir)
	rm -f $(curdir).tar.gz
	cp -r questions $(curdir)
	tar -cvf $(curdir).tar $(curdir)
	#rm -rf $(curdir)
	gzip $(curdir).tar
'''
    writefile('makefile', makefile)

def questions_makefile():
    # makefile for questions directory
    print("makefile to create submit.tar.gz")
    makefile = r'''
# make       generate pdf (and view pdf)
# make b     make a backup of main.tex with name main-[datetime stamp].tex
# make v     view pdf
# make c     remove unnecessary files
# make s     create submit.tar.gz (unnecessary files are removed)
    
pdf:
	-python /home/student/.alex/alexrunner.py replaceemail
	pdflatex --shell-escape main.tex
	#pdflatex --shell-escape main.tex
	xdg-open main.pdf

b:
	cp main.tex "main-$$(date +"%Y-%m-%-d-%H-%M-%S").tex"

v:
	xdg-open main.pdf

c:
	rm -f main-*-*-*.tex
	rm -f main.aux main.idx main.log main.out makefile.old main.py main.py.err main.py.out latex.py
    
s:
	rm -f main-*-*-*.tex
	rm -f main.aux main.idx main.log main.out makefile.old main.py main.py.err main.py.out latex.py
	rm -rf submit; rm -f submit.tar.gz; mkdir submit; rsync -av . submit --exclude submit; tar -cvf submit.tar submit; gzip submit.tar || true
	@echo ""
	@echo "done ... submit.tar.gz is created:"
	@ls -la submit.tar.gz
	@echo ""
'''
    writefile('makefile', makefile)

#------------------------------------------------------------------------------

def today(): return datetime.date.isoformat(datetime.date.today())
def writefile(filename, s):
    f =  open(filename, 'w'); f.write(s)
def readfile(filename):
    f =  open(filename, 'r')
    return f.read()
def rglob(root='.', regex='.*'):
    fs = []
    p = re.compile(regex)
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)
            if p.search(fullpath):
                fs.append(fullpath)
    return fs
    
#==============================================================================
# LaTeX
#==============================================================================
def latex_makefile(filename = 'main', kind=0):
    # latex makefiles
    # kind=0: mine
    # kind=1: student's. questions dir makefile
    if kind == 0:
        template = """
pdf:
\tpdflatex --shell-escape %(filename)s.tex
\tpdflatex --shell-escape %(filename)s.tex
\tmake cleantmp
        
student:
\tmake pdf
\trm -rf student
\trm -f student.tar
\trm -f student.tar.gz
\tmkdir student
\trsync -rv --exclude '*~' --exclude 'auto' --exclude 'student' . student
\ttar -cvf student.tar student
\tgzip student.tar

view:
\txdg-open %(filename)s.pdf

v:
\txdg-open %(filename)s.pdf
        
plain:
\tsetstyle.py %(filename)s.tex --style=plain
\tmake

fancy:
\tsetstyle.py %(filename)s.tex --style=fancy
\tmake

cleantmp:
\trm -rf abc.outut
\trm -rf '%(filename)s.log' 
\trm -rf '%(filename)s.aux'
\trm -rf '%(filename)s.toc'
\trm -rf '%(filename)s.out'
\trm -rf '%(filename)s.idx'
\trm -rf '%(filename)s.ilg'
\trm -rf 'texput.log'
\trm -rf 'shEsc.tmp'
\trm -rf '%(filename)s.vrb'
\trm -rf '%(filename)s.snm'
\trm -rf '%(filename)s.nav'
\trm -rf 'abc.output'
\trm -rf 'main.py.err'
\trm -rf 'main.py.out'
\trm -rf 'makefile.old'
\trm -rf 'auto'
\trm -rf 'desktop.ini'
\trm -rf 'main.py'
\tfind 'latex.py' -exec grep -q 'jobname="main"' '{}' \;  -delete

clean:
\trm -rf '%(filename)s.pdf'
\trm -rf student
\trm -f student.*
\tmake cleantmp
        
c:
\tmake clean
    
mail:
\tsendgmail --attach=%(filename)s.pdf

"""
        makefile = template % {'filename':filename}
    elif kind==1:
        questions_makefile()

#==============================================================================
# CPP
#==============================================================================

#------------------------------------------------------------------------------
# Dictionary that relates header files to link options
# TODO: Add SDL case
# TODO: Remove duplicates
#------------------------------------------------------------------------------
LINKFLAGS_CONFIG = {"GL/glew.h": "-lGL -lGLU -lglut -lGLEW",
                    "GL/glut.h": "-lGL -lGLU -lglut",
                    "GL/freeglut.h": "-lGL -lGLU -lglut",
                    "GL/gl.h": "-lGL -lGLU -lglut",
                   }

def cpp_makefile(main = 'main',
                 headerfilenames = [],
                 LINKFLAGS = '',
                 include={}):
    # include is a dictionary relating cpp files to header files.
    # Example:
    # include['main.cpp']['stds'] = ['iostream', 'cmath']
    # include['main.cpp']['nonstds'] = ['mystuff1', 'mystuff2']

    EXE = '%s.exe' % main.replace('.cpp', '')
    
    filename = main
    #--------------------------------------------------------------------------
    # Form linkflags for LINKFLAGS macro
    #--------------------------------------------------------------------------
    allheaderfiles = []
    for _ in include.values():
        allheaderfiles += _['stds']
        allheaderfiles += _['nonstds']
    del _
    
    for key in LINKFLAGS_CONFIG.keys():
        if key in allheaderfiles:
            LINKFLAGS += LINKFLAGS_CONFIG[key] + ' '    
    del allheaderfiles

    #--------------------------------------------------------------------------
    # Find cpp files that are found. This is used to create the obj files.
    #--------------------------------------------------------------------------
    cpps = include.keys()
    #print "... cpps:", cpps
    #--------------------------------------------------------------------------
    # Form OBJS macro. main is included.
    #--------------------------------------------------------------------------
    OBJS = ' '.join(['%s.o' % _.replace('.cpp', '') for _ in cpps])
    #print "OBJS:", OBJS
    #--------------------------------------------------------------------------
    # Form targets for object files using each value in OBJS
    #--------------------------------------------------------------------------
    objtargets = []
    for cpp in cpps:
        target = cpp.replace('.cpp', '.o')
        headerfiles = ' '.join(include[cpp]['nonstds'])
        print("target + cpp + headerfiles:", target, cpp, include[cpp]['nonstds'], headerfiles)
        objtargets.append('''%(target)s:	%(cpp)s %(headerfiles)s
	$(CXX) $(CXXFLAGS) %(cpp)s -c -o %(target)s
''' % {'target':target, 'cpp':cpp, 'headerfiles':headerfiles})
        print(objtargets[-1])
    objtargets = '\n'.join(objtargets)
    print(objtargets)

    #--------------------------------------------------------------------------
    # Create makefile
    #--------------------------------------------------------------------------
    s = r"""# Makefile for %(filename)s
# Y. Liow
#------------------------------------------------------------------------------
# Macros
#------------------------------------------------------------------------------
CXX       = g++
CXXFLAGS  = -c -std=c++2a -fmax-errors=3 -Wall -Werror -Wextra -Wpedantic \
	    -Wconversion
LINK      = g++
LINKFLAGS = %(LINKFLAGS)s
OBJS      = %(OBJS)s
EXE       = %(EXE)s

#------------------------------------------------------------------------------
# Executable
#------------------------------------------------------------------------------
$(EXE):	$(OBJS)
	$(LINK) $(OBJS) -o $(EXE) $(LINKFLAGS)

asan: $(OBJS)
	$(LINK) $(OBJS) -o $(EXE) $(LINKFLAGS) -g -fsanitize=address
#------------------------------------------------------------------------------
# Object files
#------------------------------------------------------------------------------
%(objtargets)s
#------------------------------------------------------------------------------
# Utilities
#------------------------------------------------------------------------------
clean:
	rm -rf $(OBJS) $(EXE)
c:
	rm -rf $(OBJS) $(EXE)

run:
	ASAN_OPTIONS=detect_leaks=1 ./$(EXE)
r:
	ASAN_OPTIONS=detect_leaks=1 ./$(EXE)
""" % {'EXE': EXE,
       'filename': filename,
       'LINKFLAGS': LINKFLAGS,
       'OBJS': OBJS,
       'objtargets': objtargets,
      }
    writefile('makefile', s)

#==============================================================================
# main
#==============================================================================
def getinclude(s):
    # returns (x,y) where
    # x is a list of includes of the form <...>
    # y is a list of includes of the "..."
    p = r'#include[ \t]*((<([^>]*)>)|(\"([^"]*)\"))'
    q = re.compile(p)
    r = q.search(s)
    std = None
    nonstd = None
    if r != None:
        if r.group(3) not in ['', None]:
            std = r.group(3).strip()
        if r.group(5) not in ['', None]:
            nonstd = r.group(5).strip()
    #print "getinclude ..."
    #print "    s     :", s
    #print "    std   :", std
    #print "    nonstd:", nonstd
    return std, nonstd # WARNING: can be None


def check_includes(stds, nonstds):
    """ Analyze for possible errors (?) or move includes from std
    includes to nonstd includes or vice versa.
    """
    pass


def getincludes(filename, include={}):
    """ Search for all includes in file (with given filename) as a dictionary.
    {'stds':v0, 'nonstds': v1, file_found: True}
    -- file_found: True iff filename is found
    -- v0 is a list of standard includes
    -- v1 is a list of non-standard includes.
    A standard include is of the form <iostream>
    A nonstandard include is of the form "mystuff.h"
    In the above case {'stds':['iostream'], 'nonstds':['mystuff.h']}

    TODO: Make this recursive.
    """
    print("enter getincludes ...", filename)
    
    # BASE: if filename not found, done.
    #       if filename in include, done <-- CHECK
    include[filename] = {'stds':[], 'nonstds':[], 'file_found':False}
    if not os.path.exists(filename):
        print("getincludes WARNING: %s not found in current dir" % filename)
        return 
    else:
        include[filename]['file_found'] = True
        
    # RECURSIVE
    stds, nonstds = [], []

    # Compute includes for file with filename
    f = open(filename, 'r')
    for line in f:
        std, nonstd = getinclude(line)
        if std not in ['', None] and std not in stds:
            stds.append(std)
        if nonstd not in ['', None] and nonstd not in nonstds:
            nonstds.append(nonstd)
    print("stds:", stds)
    print("nonstds:", nonstds)
    print("include 0:", include)
    include[filename]['stds'] = stds
    include[filename]['nonstds'] = nonstds
    print("include 1:", include)
    for _ in nonstds: # ignore looking for std include ... ?
        getincludes(_, include)

    return


def is_main(filename):
    """ Returns true is the file with given filename contains main()"""
    f = open(filename, 'r')
    for line in f:
        if line.find('main(') > 0:
            return True
    return False



def help():
    print("Utility to create makefile")
    print("USAGE: makemake")
    print("       makemake --cpp")
    print("       makemake --cpp --helloworld")
    print("       makemake --latex")


def article():
    f = open('main.tex', 'w')
    f.write(r'''
\input{myarticlepreamble}
\input{yliow}
\renewcommand\TITLE{SOME TITLE}

\begin{document}
\topmatter

\end{document}
    ''')
    
def run():

    try:
        opt = {}
        opt = getopt.gnu_getopt(sys.argv[1:],
                                'f',
                                ['latex', 'cpp', 'main', 'help', 'helloworld', 'article'])
        opt = dict([(x.replace('-','') ,y) for x,y in opt[0]])
        if sys.argv[1] == 'cpp' and 'cpp' not in opt.keys():
            opt['cpp'] = ''
        if sys.argv[1] == 'article':
            opt['article'] = ''
    except:
        pass

    #print(">>> opt:", opt)
    
    if "help" in opt:
        help()
        sys.exit()

    if 'article' in opt:
        article()
        sys.exit()
        
    if os.path.exists('makefile'):
        print("WARNING: previous makefile renamed as makefile.old")
        shutil.copyfile('makefile', 'makefile.old')

    #--------------------------------------------------------------------------
    # LaTeX
    #--------------------------------------------------------------------------
    def find_latex_main():
        filenames = glob.glob('*.tex')
        if len(filenames) != 0:
            #print("found latex file(s)")
            mains = []
            main = None
            for filename in filenames:
                if not os.path.exists(filename): continue
                if readfile(filename).find(r'\begin{document}') >= 0:
                    mains.append(filename)
            if len(mains) > 1:
                print("more than one candidate main ...")
                print("mains:", mains)
                i = input("enter index: ")
                main = mains[i]
            elif len(mains) == 1:
                main = mains[0]
            if main == None:
                print(r"no latex file with \begin{document}")

            if main == None:
                return False
            else:
                #print(r"found latex file with \begin{document}")
                main = main.replace(".tex", "")
                #print("main file ... %s.tex" % main)

                cwd = os.path.split(os.getcwd())[-1]
                if cwd in ['questions', 'answers'] and os.path.isdir('.'):
                    # questions makefile
                    #print("questions or answers dir")
                    kind = 1
                else:
                    kind = 0

                # now ... determine my makefile or student's makefile
                latex_makefile(main, kind=kind)
                return True
    
    #--------------------------------------------------------------------------
    # CPP
    #
    # Given a cpp file, we have a tree of includes. The non-root nodes are all
    # header files. Only the root is a cpp. A cpp is a leaf if it does not have
    # any includes. A header file is a leave if it does not have any includes
    # or the includes were already in the tree because of a previous header
    # include.
    #
    # Each of the above cpp tree will give rise to an object file. So each of
    # them will give rise to an object target in the makefile.
    #
    # The main cpp file will give rise to the executable. Note that not all
    # cpp files under the search will be needed for the executable.
    #
    # The forest building starts with the main cpp file. For each include
    # header file, if the header file has a cpp file in the current search
    # space, that cpp file will be a forest root.
    #
    # Note that I do not need a tree structure. I just need for each root to
    # have a collection of the leaves. For each leave, I need to know if
    # the header is a std or a non-std. Right now std or non-std is determined
    # by #include<...> or #include"...". Each new includes for a root,
    # the header is placed in a "TODO" pile if it's not in the "visited" pile.
    #
    # Each filename (cpp or header) points to data in a dictionary, fileinfo
    # that tells us information about the file:
    # fileinfo['xyz.h']['found'] = True or False
    # fileinfo['xyz.h']['std'] = True or False
    #
    # Here is the data we need:
    # Initially: forest = {
    #                       'main.cpp':{'headers':[], 'todo':['main.cpp']}
    #                     }
    #            main = 'main.cpp'
    #            header = {}
    #
    # [If using GNU, the dependencies can be printed using g++ -MM hw.cpp.]
    #--------------------------------------------------------------------------
    def find_cpp_main():
        cppfilenames = glob.glob('*.cpp') + glob.glob('*.c')
        if len(cppfilenames) > 0 or 'cpp' in opt.keys():
            print("makefile type: cpp")
            #------------------------------------------------------------------
            # If there's no cpp file, create helloworld.cpp
            #------------------------------------------------------------------
            if len(cppfilenames) == 0 and opt.has_key('helloworld'):
                print("no cpp file found ... creating helloworld.cpp")("cppfilenames:", cppfilenames)
            headerfilenames = glob.glob('*.h')
            print("all cpp files in current search space   :", cppfilenames)
            print("all header files in current search space:", headerfilenames)
            #------------------------------------------------------------------
            # Search for main (the cpp file with "main()" and also insert this
            # cpp as the initial work for the loop.
            #------------------------------------------------------------------
            main = ''
            for filename in cppfilenames:
                if main == '' and is_main(filename):
                    main = filename
                    break
            print("main filename:", main)
            if main == '':
                print("no main file found! halting ...")
                sys.exit()
            #------------------------------------------------------------------
            # Initialize start state for loop
            #------------------------------------------------------------------
            forest = {main:{'stds':[], 'nonstds':[], 'todo':'True'}}

            while 1:
                work = None
                for cpp in forest.keys():
                    if forest[cpp]['todo']:
                        forest[cpp]['todo'] = False
                        work = cpp
                        break
                if work == None: break # no more work to do

                d2 = {}
                getincludes(work, d2)
                nonstds, stds = [], []
                for key in d2.keys():
                    for _ in d2[key]['stds']:
                        if _ not in stds: stds.append(_)
                    for _ in d2[key]['nonstds']:
                        if _ not in nonstds: nonstds.append(_)
                        
                # WHAT HAPPENS IF work is None?
                stds = [_ for _ in stds if _ != None]
                nonstds = [_ for _ in nonstds if _ != None]
                forest[work]['stds'] = stds
                forest[work]['nonstds'] = nonstds

                #--------------------------------------------------------------
                # For each nonstd header in nonstds, check to see if the
                # corresponding cpp file is in current search space and not
                # already in the forest. If so, add that to the forest for
                # work to be done.
                #--------------------------------------------------------------
                #print "nonstds:", nonstds
                for _ in nonstds:
                    cpp = _.replace('.h', '.cpp')
                    if cpp not in forest.keys() and cpp in cppfilenames:
                        forest[cpp] = {'stds':[], 'nonstds':[], 'todo':True}
            
            #print "includes:"
            for k,v in forest.items():
                print("    %s" % k)
                print("        std headers   :", v['stds'])
                print("        nonstd headers:", v['nonstds'])
                                
            #print
            # Check if non std headers have cpp file in current directory
        
            #
            # TODO: Handle case where main = '' ... build lib??
            #
            main = main.replace(".cpp", "")
            cpp_makefile(main=main,
                         headerfilenames=headerfilenames,
                         include=forest)
            return

    if 'cpp' in opt:
        find_cpp_main()
    elif 'latex' in opt:
        print("has key latex")
        find_latex_main()
    else:
        if find_latex_main():
            pass
        else:
            find_cpp_main()

        # check if it's a quiz or assignment directory
        cwd = os.path.split(os.getcwd())[-1]
        if cwd[0] in ['q', 'a'] and cwd[1] in '0123456789' and \
           os.path.isdir('questions'):
            qnum_makefile() # q01, q02, ... makefile

if __name__ == '__main__':
    run()
