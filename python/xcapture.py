#!/usr/bin/env python

"""
Runs a program and captures its window to an image file.

main(program='./a.exe',         # program to execute
     window='test',             # name of window that program opens
     filename='screenshot.jpg', # save screenshot here
    )

To run as script
./xcapture --program=widget --window=Qt --filename=main.jpg

Y. Liow

Ref:
https://www.geeksforgeeks.org/import-command-in-linux-with-examples/
"""
import sys, os, re
VERSION = sys.version_info.major

from subprocess import Popen, PIPE

PROGRAM = './a.out'
WINDOW = '"OpenGL!!!"'
FILENAME = 'screenshot.jpg'
BORDER = True
SLEEP = 1

def shell(cmd, stdout=True):
    print("cmd:", cmd)
    p = Popen(cmd,
              shell=True,
              bufsize=2048,
              stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    print("pid:", p.pid)
    if stdout:
        return p.stdout.read()
    else:
        return 

def search(p, s, g=None):
    if g==None:
        return p.search(s)
    else:
        if VERSION == 2:
            return p.search(s).group(g)
        elif VERSION == 3:
            return p.search(s.decode()).group(g)
        else:
            raise Exception
        
def main(program=PROGRAM,   # run x program in background
         window=WINDOW,     # name of window to capture
         filename=FILENAME, # save screenshot here
         #--------------------------------------------------------
         # Adjust the window in order to capture the border
         # surrounding the window.
         # dx
         # dy
         # dw
         # dh
         border=BORDER,
         sleep=SLEEP,
         #dx=-4,
         #dy=-22, # -24
         #dw=8,
         #dh=26, # 28
         dx=0,
         dy=0, # -24
         dw=0,
         dh=0, # 28
         ):
    #print program
    #print window
    #print filename

    #--------------------------------------------------------------------------
    # If program does not have a directory, prepend it with './'.
    #--------------------------------------------------------------------------
    if os.path.split(program)[0] == '':
        program = os.path.join('./', program)
    #--------------------------------------------------------------------------
    # Run the program in background. Have s short sleep to ensure that the
    # window is opened.
    #--------------------------------------------------------------------------
    if not program.endswith('&'): cmd = "%s &" % program
    shell(cmd, stdout=False)
    shell('sleep %s' % sleep) # make sure stdout=True to force it to wait

    #--------------------------------------------------------------------------
    # Compute the coordinates of the window to capture
    # x, y: x,y offset of top-left of window
    # w   : width of window
    # h   : height of window
    #--------------------------------------------------------------------------
    s = shell('xwininfo -name "%s"' % window)
    
    p = 'Absolute upper-left X:\s*([0-9]+)'
    p = re.compile(p)
    x = int(search(p, s, 1))
    
    p = 'Absolute upper-left Y:\s*([0-9]+)'
    p = re.compile(p)
    y = int(search(p, s, 1))

    p = 'Width:\s*([0-9]+)'
    p = re.compile(p)
    w = int(search(p, s, 1))

    p = 'Height:\s*([0-9]+)'
    p = re.compile(p)
    h = int(search(p, s, 1))

    if border:
        x += dx
        y += dy
        w += dw
        h += dh

    print("x, y, w, h:", w, y, w, h)

    #--------------------------------------------------------------------------
    # Switch to the window of the program to be captured (otherwise the window
    # to be captured might be hidden).
    #--------------------------------------------------------------------------
    shell('wmctrl -a %s' % window)

    #--------------------------------------------------------------------------
    # Perform fullscreen capture, crop, and save to a file
    #--------------------------------------------------------------------------
    #print x, y, w, h
    #shell('import -window root -crop %sx%s+%s+%s %s' % \
    #      (w, h, x, y, filename))

    # This version will capture the specified window by name without
    # cropping but you cannot get the surrounding border of the window
    shell('import -border -frame -window %s %s' % (window, filename))

    #--------------------------------------------------------------------------
    # Finally kill the program in background
    #--------------------------------------------------------------------------
    if program.startswith('./'): program = program[2:]
    if program.endswith(' &'): program = program[:-2]
    s = shell('ps | grep %s' % program).strip()
    lines = s.split(b'\n')
    #print "s:", s
    regex = re.compile(b'([0-9]+) ')
    for line in lines:
        srch = search(regex, line)
        if srch:
            shell('kill -9 %s' % srch.group(1))

if __name__ == '__main__':
    import sys, getopt
    d = getopt.gnu_getopt(sys.argv[1:],
                          '',
                          ['program=',
                           'window=',
                           'filename=',
                           'border=',
                           'sleep='])[0]
    d = [(a.replace('--',''),b) for a,b in d]    
    d = dict(d)
    if not 'program' in d: d['program'] = PROGRAM
    if not 'window' in d: d['window'] = WINDOW
    if not 'filename' in d: d['filename'] = FILENAME
    if not 'border' in d: d['border'] = BORDER
    if not 'sleep' in d: d['sleep'] = SLEEP

    if d['border'] == '0':
        d['border'] = False
        
    print(d)
    main(program=d['program'],
         window=d['window'],
         filename=d['filename'],
         border=d['border'],
         sleep=d['sleep'])
