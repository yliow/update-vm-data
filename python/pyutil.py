import json
import os, requests, shutil
import difflib
import math
import scipy.special
import random; random.seed()
import string, sys
import subprocess


def subprocessrun(args,
                  check=True,
                  shell=False):
    """
    return p has p.stdout, p.stderr, p.returncode.
    Note that if check is True, the exception error msg is not useful.
    The stderr is more useful. But if check is True, I don't get stderr.
    See subprocessrun2 below.
    """
    return subprocess.run(args,
                          capture_output=True, text=True,
                          check=check, shell=shell)

def subprocessrun2(args,
                   check=True,
                   shell=False):
    if not check:
        p = subprocess.run(args,
                           capture_output=True, text=True,
                           check=False, shell=shell)
    else:
        p = subprocess.run(args,
                           capture_output=True, text=True,
                           check=False, shell=shell)
        if p.returncode != 0:
            raise Exception("returncode: %s\nstdout:%s\nstderr:%s" % (p.returncode, p.stdout, p.stderr))


def myeval(dir_=None, package='q0001', module='main', func_name='question'):
    if dir_: sys.path.append(dir_)
    module_name = randstr() # 'M'
    exec('import %s.%s as %s' % (package, module, module_name), globals())
    ret = getattr(globals()[module_name], func_name)()
    del globals()[module_name]
    if dir_: del sys.path[-1]
    return ret

def randstr(length=32, chars=string.ascii_letters):
    xs = list(chars)
    random.shuffle(xs)
    return ''.join(xs[:length])

def system(cmd, verbose=True):
    # check if cmd has ">"
    #filename = 'tmp%s.txt' % randstr()
    #if ">" not in cmd:
    #    cmd = "%s > %s" % (cmd, filename)
    if verbose: print(cmd)
    os.system(cmd)
    #return readfile(filename)

def IFELSE(b, x, y):
    if b: return x
    return y

def cp(f0, f1, verbose=False):
    if verbose: print('cp %s %s' % (f0, f1), flush=True)
    shutil.copy2(f0, f1)
def mv(f0, f1, verbose=False):
    if verbose: print('mv %s %s' % (f0, f1), flush=True)
    shutil.move(f0, f1)
def mkdir(dir_='questions', verbose=False):
    if verbose: print('mkdir %s' % dir_, flush=True)    
    os.makedirs(dir_)
def rm(filenames, verbose=False):
    cmd = 'rm -f %s' % filenames
    if verbose: print(cmd, flush=True)    
    system(cmd, verbose=False)
def readfile(path, format=None):
    '''
    format = 'r' or 'rb'. Default 'r'.
    '''
    try:
        if format==None:
            f = open(path, 'r')
        else:
            f = open(path, format)
        return f.read()
    except:
        print("path:", path)
        raise
        
def readfile_here(filename):
    dir_ = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir_, filename)
    return readfile(path)

def writefile(path, s, format='utf-8'):
    assert isinstance(s, (str, bytes)), "s = %s is not str/bytes" % s
    if isinstance(s, bytes):
        f = open(path, 'wb')
    else:
        s = bytes(s, 'utf-8')
        f = open(path, 'wb')
    f.write(s)
    f.close()

def myrequests_get(url, stream=False, allow_redirects=True):
    """This is basically requests.get except that raise_for_status is called"""
    try:
        r = requests.get(url, stream=stream, allow_redirects=allow_redirects)
        r.raise_for_status()
    except Exception as e:
        print("ERROR: requests.get to %s status code %s\n\n%s" % (url, r.status_code, e))
        raise
    return r

def save_url(url, stream=False, allow_redirects=True, chunksize=1024*1024,
             destdir=None, destpath=None,
             verbose=False):
    """ save url to path """
    if destdir==None: destdir = '.'
    if destpath==None: destpath = os.path.split(url)[-1]
    destpath = os.path.join(destdir, destpath)
    # Create subdirs if necessary
    dirs, filename = os.path.split(destpath)
    if dirs != '':
        os.makedirs(dirs, exist_ok=True)
        
    if chunksize==None:
        if verbose: print('%s -> %s' % (url, destpath))
        r = myrequests_get(url, stream)
        writefile(destpath, r.content)
    else:
        done = 0
        r = myrequests_get(url, stream=True)
        #total_length = '?'
        #try:
        #    total_length = int(r.headers.get('Content-Length', None))
        #    if total_length == None:
        #        total_length = '?'
        #    input("content length: %s .... " % total_length)
        #except:
        #    total_length = '?'
        output = '%s -> %s [%sb]'
        f = open(destpath, 'wb')    
        for chunk in r.iter_content(chunksize):
            f.write(chunk)
            done += len(chunk)
            if verbose:
                s = output % (url, destpath, done)
                print(s + (len(s)*'\b'), end='')
        f.close()    
        if verbose:
            print()
    
def wget(url, dest=None, verbose=True, chunksize=None):
    save_url(url=url, destpath=dest, verbose=verbose, chunksize=chunksize)
    
def download_github(user='yliow', repo=None, path=None,
                    chunksize=None,
                    destpath=None,
                    destdir=None,
                    verbose=True):
    url = 'https://raw.githubusercontent.com/%s/%s/master/%s' % (user, repo, path)
    stream = True
    if chunksize==None: stream = False
    save_url(url, stream=stream,
             destdir=destdir, destpath=destpath, chunksize=chunksize,
             verbose=verbose)
    
def difffiles(path1, path2, cleanup=True):
    """
    returns True if files different
    -- if path* are regular files, diff on the files
    -- if path* are directorites, diff the tar
    -- if one path is regular, one is dir or one/both does not exists, return False
    """
    if os.path.isfile(path1) and os.path.isfile(path2):
        system('diff "%s" "%s" > diff.txt' % (path1, path2), verbose=False)
        s = readfile('diff.txt').strip()
    elif os.path.isdir(path1) and os.path.isdir(path2):
        cmd = 'diff -r "%s" "%s" > diff.txt' % (path1, path2)
        os.system(cmd)
        s = readfile('diff.txt').strip()
    if cleanup: rm('diff.txt cmp.txt tar123.tar.gz tar234.tar.gz')    
    return s
def diff(path1, path2):
    #print("diff", path1, path2)
    return difffiles(path1, path2)

def backup(path, verbose=True):
    """
    path = regular file or directory.
    The backup path is returned.
    
    If path = 'a/b/c/d.txt', then this is copied to 'a/b/c/d.txt.backup.0'.
    If 'a/b/c/d.txt.backup.0' exists, a copy is not made if 'a/b/c/d.txt' is the
    same as 'a/b/c/d.txt.backup.0'.
    If there are multiple backups, the "latest" back is compared against
    'a/b/c/d.txt'.
    For instance if 'a/b/c/d.txt.backup.42' exists and there is no 
    'a/b/c/d.txt.backup.43', then 'a/b/c/d.txt' is compared against
    'a/b/c/d.txt.backup.42'.

    Same thing happens if path = 'a/b/c/d/' is a directory.
    """
    if not os.path.exists(path):
        raise ValueError("path %s does not exist" % path)
    
    def backup_paths(path):
        """
        Return last backup path and new backup path.
        Example:
        -- backup_paths("a.txt") return None, "a.txt.backup.000" is there's no backup of "a.txt"
        -- backup_paths("a.txt") return "a.txt.backup.003", "a.txt.backup.004" is the last back up is "003".
        
        If path is 'a/b/c/d.txt', and 'a/b/c/d.txt.backup.42' exists and '42'
        is the max, then 'a/b/c/d.txt.backup.42' is returned.
        If there are no backups, then 'a/b/c/d.txt.backup.0' is returned.
        """
        i = 0
        while os.path.exists(os.path.join('%s.backup.%s' % (path, str(i).zfill(3)))):
            i += 1
        if i == 0:
            return None, "%s.backup.%s" % (path, str(i).zfill(3))
        else:
            return "%s.backup.%s" % (path, str(i - 1).zfill(3)), "%s.backup.%s" % (path, str(i).zfill(3))

    a, b = backup_paths(path)
    backup_path = None
    #print("backup_paths:", a, b)
    if a == None:
        #print("no backups found ... backing up ...")
        os.system('cp -r "%s" "%s"' % (path, b))
        backup_path = b
    else:
        #print("backup %s is found ..." % a)
        if diff(path, a):
            #print("%s %s not the same ... backing up" % (path, b))
            os.system('cp -r "%s" "%s"' % (path, b))
            backup_path = b
        else:
            #print("%s %s same ... no new backup" % (path, a))
            backup_path = a

    if verbose:
        print("backup %s ... see %s" % (path, backup_path))
    return backup_path


def fact(n):
    return math.factorial(n)

def c(n,r):
    return scipy.special.comb(n, r, exact=True)


if __name__ == '__main__':
    print("\ntesting dowload_github text data test1 ...")
    download_github(repo='latextool', path='latextool_basic.py', destdir='test1')
    if difffiles('test1/latextool_basic.py', '../latextool/latextool_basic.py'):
        raise Exception("different")
    print("pass")

    print("\ntesting dowload_github text data test2 ...")
    download_github(repo='latextool', path='latextool_basic.py', destdir='test2', chunksize=1)
    if difffiles('test2/latextool_basic.py', '../latextool/latextool_basic.py'):
        raise Exception("different")
    print("pass")
        
    print("\ntesting wget text data test3 ...")
    wget(url='http://yliow.github.io/index.html', dest='test3/index.html')
    if difffiles('test3/index.html', '../yliow.github.io/index.html'):
        raise Exception("different")
    print("pass")
    
    print("\ntesting wget text data stream test4 ...")
    wget(url='http://yliow.github.io/index.html', dest='test4/index.html', chunksize=1, verbose=True)
    if difffiles('test4/index.html', '../yliow.github.io/index.html'):
        raise Exception("different")
    print("pass")
        
    print("\ntesting wget binary data test5 ...")
    wget(url='http://yliow.github.io/pdfs/make/main.pdf', dest='test5/main.pdf')
    if difffiles('test5/main.pdf', '../yliow.github.io/pdfs/make/main.pdf'):
        raise Exception("different")
    print("pass")
        
    print("\ntesting wget binary data stream test6 ...")
    wget(url='http://yliow.github.io/pdfs/make/main.pdf', dest='test6/main.pdf', chunksize=1, verbose=True)
    if difffiles('test6/main.pdf', '../yliow.github.io/pdfs/make/main.pdf'):
        raise Exception("different")
    print("pass")

    print()


def save_json(path, jdata):
    writefile(path, json.dumps(jdata))

def restore_json(path):
    return json.loads(readfile(path))
