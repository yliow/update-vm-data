#!/usr/bin/python3

import sys, os

def quote(s):
    if not s.startswith('"'): s = '"%s' % s
    if not s.endswith('"'): s = '%s"' % s
    return s

if __name__ == '__main__':
    stringregex = ''
    fileregex = '"*"'
    
    if len(sys.argv) == 1:
        print ("""USAGE:
    findgrep "[stringregex]" "[file regex]"'
    WARNING: make sure you use quotes if necessary
        """)
        sys.exit()
    
    try:
        stringregex = sys.argv[1]
        stringregex = quote(stringregex)
    
        fileregex = sys.argv[2]
        fileregex = quote(fileregex)    
    except:
        pass
    
    cmd = "find . -name %s -exec grep %s {} -nH \; 2>/dev/null" % \
          (fileregex, stringregex)
    print ("\n" + cmd + "\n")
    os.system(cmd)
    
