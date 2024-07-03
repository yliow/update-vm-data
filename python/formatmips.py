#!/usr/bin/env python
import sys, glob
from pyutil import *

LABEL_WIDTH = 8
OP_WIDTH = 8
PARAMS_WIDTH = 16

def format(s):
    lines = s.split('\n')
    ret = ""
    for line in lines:
        
        if line.strip() == '':
            # blank line
            ret += '\n'
            continue
        
        elif line.startswith('#'):
            # Column 0 Comment
            ret += line + '\n'
            continue
        
        elif line.lstrip().startswith('.'):
            # Directive
            # Make sure there's one space between words
            while '  ' in line:
                line = line.replace('  ', ' ')
            ret += (LABEL_WIDTH*' ') + line.strip() + '\n'
            continue
        
        elif line.lstrip().startswith('#'):
            # There are 4 columns
            # [label]:   [op]    [params]   [comment] ....... CASE 1
            #
            # or
            #            [comment]                    ....... CASE 2
            #
            # or
            #                               [comment] ....... CASE 3
            #
            # CASE 2, 3
            line = line.replace('\t', '      ')
            if line.startswith((LABEL_WIDTH + OP_WIDTH) * ' '):
                # CASE 3
                line = line.strip()
                ret += '%s%s%s%s\n' % (' '.ljust(LABEL_WIDTH),
                                       ' '.ljust(OP_WIDTH),
                                       ' '.ljust(PARAMS_WIDTH),
                                       line,
                                       )
                continue
            else:
                # CASE 2
                line = line.strip()
                ret += '%s%s\n' % (' '.ljust(LABEL_WIDTH),
                                   line,
                                   )
                continue

        else:
            if ':' in line:
                label, line = line.split(':', 1)
                label += ':'
            else:
                label = ''
                
            label = label.strip()
            line = line.strip()

            # Either column 2 comment or op or column 4 comment
            if line.startswith('#'):
                ret += LABEL_WIDTH*' ' + line + '\n'; continue
            
            if '#' in line:
                line, comment = line.split('#', 1)
                comment = '#' + comment
            else:
                comment = ''
                
            line = line.strip()
            comment = comment.strip()
            line = line.replace('\t', ' ')
            
            if ' ' in line:
                op, params = line.split(' ', 1)
            else:
                op = line
                params = ''
            op = op.strip()
            params = params.strip()
            
            if params:
                params = params.split(',')
                params = [_.strip() for _ in params]
                params = ", ".join(params)

            ret += '%s%s%s%s\n' % (label.ljust(LABEL_WIDTH),
                                   op.ljust(OP_WIDTH),
                                   params.ljust(PARAMS_WIDTH),
                                   comment,
                                   )
    return ret.rstrip()

def main(filename):
    print("MIPS formatter")
    print("filename:", filename)
    s = readfile(filename)
    writefile('%s.old' % filename, s)
    writefile(filename, format(s))
    print("formatted program:", filename)
    print("original save as :", ('%s.old' % filename))

if __name__ == '__main__':
    regex = sys.argv[1]

    try:
        s = sys.argv[2]
        if s[0] == '-': LABEL_WIDTH -= int(s[1:])
        elif s[0] == '+': LABEL_WIDTH += int(s[1:])
        else: LABEL_WIDTH = int(s)
    except: pass
    try:
        s = sys.argv[3]
        if s[0] == '-': OP_WIDTH -= int(s[1:])
        elif s[0] == '+': OP_WIDTH += int(s[1:])
        else: OP_WIDTH = int(s)
    except: pass
    try:
        s = sys.argv[4]
        if s[0] == '-': PARAMS_WIDTH -= int(s[1:])
        elif s[0] == '+': PARAMS_WIDTH += int(s[1:])
        else: PARAMS_WIDTH = int(s)
    except: pass

    for filename in glob.glob(regex):
        main(filename)
