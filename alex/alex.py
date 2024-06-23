import requests, getpass, os, re, sys, traceback, string, random; random.seed()
import shutil, glob
import configparser
import hashlib

CHARS = list(string.ascii_letters + string.digits)

URL    = 'https://yliowsubmit.pythonanywhere.com/doul'
URL2   = 'https://yliowsubmit.pythonanywhere.com/dodl'
URL3   = 'https://yliowsubmit.pythonanywhere.com/'
URL4   = 'https://yliowsubmit.pythonanywhere.com/email_user'

CONFIG = '/home/student/.alex/alex' # the ini file

class InputError(BaseException): pass
class FileNotDownloaded(BaseException): pass

def help():
    input('''
you can run alex from any directory. alex will try to guess the user/course/work/path, but it might be wrong. if you run alex within a "ciss245" directory, then alex will guess you are submitting for "ciss245". if you run alex within directory "q1234", then alex will guess you are submitting for "q1234". if there's a q1234.tar.gz file in the same directory, alex will guess you are submitting q1234.tar.gz.

although you can run alex anywhere, if you are submitting a42 of ciss999, then it's probably best to run alex in /home/student/ciss999/a/a42/ (assuming you have such a directory organization). this way alex can auto find almost all the info. and to be organized, your submit.tar.gz should be /home/student/ciss999/a/a42/submit.tar.gz. likewise if you are working on q1234 of ciss999, you should probably run alex in /home/student/ciss999/q/q1234/ and submit.tar.gz should probably be /home/student/ciss999/q/q1234/submit.tar.gz.

i suggest you organize your directories like this:
student
|
+-- ciss240
|   |
|   +-- a (for assignments)
|   |   |
|   |   +-- a01 (for assignment a01)
|   |   |   |
|   |   |   +-- a01q01 (for assignment a01 question q01
|   |   |   |
|   |   |   +-- a01q02
|   |   |
|   |   +-- a02
|   |       |
|   |       +-- a02q01
|   |
|   +-- q (for quizzes)
|       |
|       +-- q0101
|
+-- ciss245
|   |
|   +-- a
|   |
|   +-- q
    
[u]ser         : select this to change user code or request user code by email
[e]mail        : select this to set your college email address 
[c]ourse       : select this to set course you are submitting for (example: ciss123 or math456)
[w]ork         : select this to set work you are submitting (example: a01 or q1234)
[p]ath         : select this to set path of the *.tar.gz file to submit
[r]eplace email: replace AUTHOR in main.tex with your email address
[s]ubmit       : select this to submit the *.tar.gz file to alex server
[t]ar-gzip     : tar and gzip the currect directory and name it submit.tar.gz
[a]lex update  : update alex (duh)
[D]oom         
[l]aundry
[q]uit         : or Ctrl-C or Ctrl-D to halt

press enter to continue ... ''')
    
def hide(user):
    if user == None:
        return "None"
    else:
        return '%s%s' % (user[:4], len(user[4:]) * '*')
def system(cmd, doprint=True):
    print('> %s' % cmd)
    os.system(cmd)
def randstr(len=32):
    random.shuffle(CHARS)
    return ''.join(CHARS[:len])
def readfile(filename):
    f = open(filename, 'r'); s = f.read().strip(); f.close()
    return s
def writefile(filename, s):
    f = open(filename, 'w'); f.write(s); f.close()
def wget(filename, targetfilename=None):
    #print("filename:", filename)
    #print("targetfilename:", targetfilename)
    if targetfilename == None:
        cmd = 'wget -nv -q https://yliowsubmit.pythonanywhere.com/static/downloads/%s' % filename
    else:
        cmd = 'wget -nv -q -O %s https://yliowsubmit.pythonanywhere.com/static/downloads/%s' % (targetfilename, filename)
    #print("cmd:", cmd)
    os.system(cmd)
    if not os.path.exists(filename):
        #print(filename, 'not downloaded')
        raise FileNotDownloaded()
def rm(filename):
    try: os.remove(filename)
    except: pass
def mv(f0, f1): shutil.move(f0, f1)
def cp(f0, f1):
    if os.path.exists(f0): shutil.copy2(f0, f1)
def makedirs(path):
    if not os.path.exists(path): os.makedirs(path)
    
def readwget(filename):
    """ wget, read the download, remove the download """
    wget(filename)
    s = readfile(filename)
    rm(filename)
    return s

def targzip():
    """
    0. rm -rf submit/
    1. create directory submit/
    2. cp -r current directory into submit/
    3. tar -cvf submit.tar submit
    4. gzip submit.tar
    """
    print("""
i'm going to execute the following:

find . -name 'a.out' -delete
... and various other useless files ...
rm -rf submit
rm -f submit.tar.gz
mkdir submit
rsync -av . submit --exclude submit
tar -cvf submit.tar submit
gzip submit.tar
""")
    option = input("continue? (y/n) ")
    if option == 'y':
        fs = ['a.out', '*.exe', 'main.aux', 'main.idx', 'main.log', 'main.out',
              'makefile.old', 'main.py.err', 'main.py.out', '*.pyc', 'latex.py']
        for f in fs:
            system("find . -name '%s' -delete" % f)
        system('rm -rf submit; mkdir submit; rm -f submit.tar.gz')
        system('rsync -av . submit --exclude submit')
        system('tar -cvf submit.tar submit')
        system('gzip submit.tar')
        print()
        print("done!!! contents of submit.tar.gz below. you might want to check submit/ too.")
        system("tar --list --verbose --file submit.tar.gz")
        print()
        input("press enter to continue ... ")
    else:
        print("submit.tar.gz not created")
        
def replaceemail(filename='main.tex'):
    config = readconfig()
    try:
        email = config['DEFAULT']['email']
    except KeyError as e:
        print('\nalex cannot find your email address')
        return
    if not os.path.exists(filename):
        print("\nERROR: %s not found" % filename)
        return
    
    s = readfile(filename)
    i = s.find(r'\renewcommand\AUTHOR{')
    if i == -1:
        print(r'\nERROR: "\renewcommand\AUTHOR{" not found in %s ... file is not changed' % filename)
        return
    j = s.find('}', i + len(r'\renewcommand\AUTHOR'))
    if j == -1:
        print(r'\nERROR: "}" not found in %s ... file is not changed' % filename)
        return
    
    old_email = s[i+len(r'\renewcommand\AUTHOR{'):j]
    t = s[:i+len(r'\renewcommand\AUTHOR{')] + email + s[j:]
    writefile('%s.old' % filename, s)
    writefile(filename, t)
    print("\ndone ... %s replaced with %s" % (old_email, email))
    print("%s backup is %s.old" % (filename, filename))
    #s = s.replace(r'\renewcommand\AUTHOR{jdoe5@cougars.ccis.edu}',
    #          r'\renewcommand\AUTHOR{%s}' % email)
    
def update(config):
    """ update """
    print("\ngimme a sec ...")
    version = readwget('alexversion.txt')
    print("your version is %s" % config['DEFAULT'].get('version', None))
    print("alex server version is %s" % version)
    if version == config['DEFAULT'].get('version', 'xyz'):
        print("whoopie ... no alex update needed ... saved some electrons")
        return

    print("updating version %s -> version %s" % \
          (config['DEFAULT'].get('version', 'None'), version))
    os.system('whoami > whoami.txt')
    user = readfile('whoami.txt')
    rm('whoami.txt')
    if user == 'root':
        print('ERROR: run this as a regular user and not as root ... halting')
        sys.exit()

    makedirs('/home/%s/.alex/' % user)

    # make a temporary download directory
    makedirs('alexupdate')
    cwd = os.getcwd()
    os.chdir('alexupdate')
    
    print("0/3 ...")
    wget('alex.cpython-37.pyc')
    mv('alex.cpython-37.pyc', '/home/%s/.alex/alex.pyc' % user)
    
    print("1/3 ...")
    wget('alexrunner.py')
    mv('alexrunner.py', '/home/%s/.alex/alexrunner.py' % user)
    
    print("2/3 ...")
    cp('/home/%s/.bashrc' % user, '/home/%s/.bashrc.backup' % user)
    s = readfile('/home/%s/.bashrc' % user)
    t = "alias alex='python /home/%s/.alex/alexrunner.py'" % user
    if t not in s:
        s += '\n' + t + '\n'
        f = open('/home/%s/.bashrc' % user, 'w'); f.write(s); f.close()

    print("3/3 ...")
    try:
        wget('main.tar.gz')
        if os.path.exists('main.tar.gz'):
            os.system('gunzip main.tar.gz; tar -cvf main.tar; cd main; python main.py')
        else:
            pass
    except:
        pass
    
    os.chdir(cwd)
    os.system('rm -rf alexupdate')

    config['DEFAULT']['version'] = version
    writeconfig(config)
    
    print("done ... halting ... run alex again for new alex to take effect")
    sys.exit()

    
def submit_form(url, data, files=None):
    '''
    url: url string
    data: dictionary of key value pairs
    files: dictionary of (filename, filepath)
    '''
    if files != None:
        try:
            resp = requests.post(url, files=files, data=data)
            return resp
        except requests.exceptions.ConnectionError:
            print("ConnectionError: internet connection problem. If problem persists, let dr liow know.")
            sys.exit()
        except Exception as e:
            print("Exception: %s. If problem persists, let dr liow know." % e)
            sys.exit()            
    else:
        try:
            resp = requests.post(url, data=data)
            return resp
        except requests.exceptions.ConnectionError:
            print("ConnectionError: internet connection problem. If problem persists, let dr liow know.")
            sys.exit()
            
def submit_assessment(user,
                      course,
                      assessment,
                      action,
                      path):
    url = URL
    # ADDED 2022/1/8
    md5 = hashlib.md5(open(path,'rb').read()).hexdigest()
    data = {'user':user,
            'course':course,
            'assessment':assessment,
            'action':action,
            'md5':md5}
    files = {'file': open(path,'rb')}
    return submit_form(url=url, data=data, files=files)

def getdefaultuser(config):
    try:
        return config['DEFAULT']['user']
    except:
        return None
    
def getdefaultemail(config):
    try:
        return config['DEFAULT']['email']
    except:
        return None
def getemail(config):
    try:
        email = getdefaultemail()
        print("email:", email)
    except: # email not in config
        print("enter your college email address carefully because i will not check for correctness!")
        email = input("email (example: jdoe42@cougars.ccis.edu): ").strip()
        if email.endswith('@cougars.ccis.edu') or \
           email == 'yliow@ccis.edu':
            config['DEFAULT']['email'] = email
            writeconfig(config)
            config = readconfig()
            return email
        else:
            print('ERROR: email does not end with "@cougars.ccis.edu"')
            return None

def getuser(config):
    try:
        user = getdefaultuser()
        print("user:", user)
    except: # user not in config
        user = input("user (if you don't remember your user code enter your email addr): ").strip()
        if user != '':
            if '@' not in user:
                config['DEFAULT']['user'] = user
                writeconfig(config)
                config = readconfig()
            else:
                print("emailing your user code ...")
                url = URL4
                data = {'email':user}
                text = submit_form(url=url, data=data).text
                print("response:", text)
                if "not found" in text:
                    print("if your email was not found then the email address was entered incorrect or not recognized")
                else:
                    print("done. it might take 1-2 minutes for email to arrive (gmail can be fickle). run alex when you have your user code.")
                user = None
    return user

def getcourses(config):
    #print("Reading courses ...")
    if len(config.sections()) == 0:
        print("no courses yet")
        while 1:
            course = getcourse(config)
            if course == '': break
    for course in sorted(config.sections()):
        print(course)
        print("    path:", config[course]['path'])
        if not os.path.exists(config[course]['path']):
            print("path above is incorrect")
            path = input("path: ")

            
def getdefaultcourse(config):
    # get ciss??? or math??? from path
    p = re.compile(r'/((ciss|math)\d\d\d)(/|$)')
    s = os.getcwd()
    srch = p.search(s)
    if srch != None:
        return srch.group(1)
    else:
        return None
    
def isvalidcourse(course):
    p = re.compile(r'(ciss|math)\d\d\d$')
    return p.search(course) != None    
    
def getcourse(config):
    """
    NOTE: either course entered exists or not.
    return None -- there's an invalid entry
    return ''   -- quit loop
    """
    t = getdefaultcourse(config) # find course in cwd
    if t != None:
        course = input('course (example ciss240; default is %s): ' % t)
        if course.strip() == '': course = t
    else:
        course = input('course (example ciss240): ')
    course = course.lower().strip()
    if course == '': return ''

    if not isvalidcourse(course):
        print("ERROR: invalid course")
        return None
    return course

    '''
    else:
        # Check if course is in config
        # if in config, ask if user wants to change path
        if course not in config:
            config[course] = {}
        if 'path' not in config[course]:
            path = input('path for %s (example /home/student/%s): ' % \
                         (course, course))
            if not os.path.exists(path):
                print("path does not exist ... creating path ...")
                os.makedirs(path)
            config[course]['path'] = path
        path = config[course]['path']
        print("path of %s:" % course, path)
        writeconfig(config)
    return course
    '''
    
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
    
def getassessment():
    '''
    For say q01, user might have current working direction q01 or q.
    So search for q* in cwd or in the tree by during os.walk
    '''
    t = getdefaultassessment()
    if t != None:
        ret = input('work (example q42; default is %s): ' % t)
        if ret.strip() == '':
            ret = t
    else:
        ret = input('work (example: q00): ')
    ret = ret.strip()
    if ret == '':
        print("ERROR: no work entered")
        ret = None
    elif not (ret[0] in 'aqtpf'):
        print("ERROR: does not start with a or q or t or f or p")
        ret = None
    elif not (ret[1:].isdigit()):
        print("ERROR: a/q/t/f/p must be followed by digits")
        ret = None
    return ret

def getaction():
    ret = input('action (press enter for submit): ').strip()
    if ret == '':
        ret = 'submit'
    if ret not in ['submit', 'grades', 'grade']:
        print("invalid action ... halting ...")
        raise InputError()
    return ret

def findpath(assessment):
    for root, dirs, files in os.walk('.'):
        path = os.path.abspath(root)
        part = os.path.split(path)[-1]
        if part == assessment:
            return path
    
def getdefaultassessmentpath(assessment):
    fs = glob.glob("*.tar.gz")
    if len(fs) == 1:
        return fs[0]
    else:
        if 'submit.tar.gz' in fs:
            return 'submit.tar.gz'
        else:
            return None
    """
    for root, dirs, files in os.walk('.'):
        for filename in files:
            path = os.path.join(root, filename)
            if os.path.split(path)[-1].endswith('.tar.gz'):
                if path.startswith('./'):
                    path = path[2:]
                    return path
    return None
    """
    
def getassessmentpath(assessment):
    t = getdefaultassessmentpath(assessment)
    if t not in [None, '']:
        path = input('path (example %s.tar.gz; default is %s): ' % (assessment, t)).strip()
        if path == '':
            path = t
    else:
        path = input('path (example q00.tar.gz): ').strip()
        
    if not os.path.exists(path):
        print("ERROR: path does not exist")
        path = None
    # The makefile for quizzes creates "submit.tar.gz"
    #if not (os.path.split(path)[-1]).startswith(assessment):
    #    print("path does not start with %s" % assessment)
    #    sys.exit()
    elif not (os.path.split(path)[-1]).endswith('.tar.gz'):
        print("ERROR: path does not end with .tar.gz")
        path = None
    return path
    
def readconfig():
    """
    TODO: If config not found, create a blank one instead of
    throwing exception.
    """
    config = configparser.ConfigParser()
    try:
        if not os.path.exists(CONFIG):
            raise FileNotFoundError()
        config.read(CONFIG)
    except FileNotFoundError:
        #print("config file not found")
        pass
    return config

def writeconfig(config):
    with open(CONFIG, 'w') as f:
        config.write(f)

def ui_submit_assessment(config, user, course, assessment, path):
    #user = config['DEFAULT']['user']
    #course = getcourse(config)
    #assessment = getassessment()
    #path = getassessmentpath(assessment)
    if user == None:
        print("ERROR: user is None")
        return
    if course == None:
        print("ERROR: course is None")
        return
    if assessment == None:
        print("ERROR: assessment is None")
        return
    if not os.path.exists(path):
        print("ERROR: path %s does not exist")
        return
    print("")
    print("user      : %s" % hide(user))
    print("course    :", course)
    print("assessment:", assessment)
    print("path      :", path)
    option = input('submit (y/n)? ')
    if option in 'yY':
        print("gimme 2 secs ...", flush=True)
        print(submit_assessment(user=user,
                                course=course,
                                assessment=assessment,
                                action='submit',
                                path=path).text)

def getversion(config):
    if 'version' not in config['DEFAULT']:
        return None
    else:
        return config['DEFAULT']['version']

def doom():
    print('''DOOM                         
                                         )  (  (    (                     
                                         (  )  () @@  )  (( (             
                                     (      (  )( @@  (  )) ) (           
                                   (    (  ( ()( /---\   (()( (           
     _______                            )  ) )(@ !O O! )@@  ( ) ) )       
    <   ____)                      ) (  ( )( ()@ \ o / (@@@@@ ( ()( )     
 /--|  |(  o|                     (  )  ) ((@@(@@ !o! @@@@(@@@@@)() (     
|   >   \___|                      ) ( @)@@)@ /---\-/---\ )@@@@@()( )     
|  /---------+                    (@@@@)@@@( // /-----\ \\ @@@)@@@@@(  .  
| |    \ =========______/|@@@@@@@@@@@@@(@@@ // @ /---\ @ \\ @(@@@(@@@ .  .
|  \   \\=========------\|@@@@@@@@@@@@@@@@@ O @@@ /-\ @@@ O @@(@@)@@ @   .
|   \   \----+--\-)))           @@@@@@@@@@ !! @@@@ % @@@@ !! @@)@@@ .. .  
|   |\______|_)))/             .    @@@@@@ !! @@ /---\ @@ !! @@(@@@ @ . . 
 \__==========           *        .    @@ /MM  /\O   O/\  MM\ @@@@@@@. .  
    |   |-\   \          (       .      @ !!!  !! \-/ !!  !!! @@@@@ .     
    |   |  \   \          )      .     .  @@@@ !!     !!  .(. @.  .. .    
    |   |   \   \        (    /   .(  . \)). ( |O  )( O! @@@@ . )      .  
    |   |   /   /         ) (      )).  ((  .) !! ((( !! @@ (. ((. .   .  
    |   |  /   /   ()  ))   ))   .( ( ( ) ). ( !!  )( !! ) ((   ))  ..    
    |   |_<   /   ( ) ( (  ) )   (( )  )).) ((/ |  (  | \(  )) ((. ).     
____<_____\\__\__(___)_))_((_(____))__(_(___.oooO_____Oooo.(_(_)_)((_
    
still in development hell ... ''', end='')
    input("press enter to continue ... ")

def laundry():
    print('''
will get right onto it ... when i have arms
''')

def download(config, course, assessment):
    print("\ndownloading ...")
    print("user  :", hide(config['DEFAULT']['user']))
    print("course:", course)
    print("work  :", assessment)
    if assessment in ['', None]:
        assessment = input("work: ")
    print("gimme 2-4 secs ...")
    action = 'download'
    url = URL2
    data = {'user':user,
            'course':course,
            'assessment':assessment,
            'action':action}
    resp = submit_form(url=url, data=data)
    if 'ERROR' in resp.text:
        print(resp.text)
    else:
        #print(resp.text)
        #resp.text is URL example http://a.b/static/zzzzz
        #on server side:
        # * zzzzz is computed using
        #   hash of user + course + assessment?
        # * if static/zzzzz does not exist, copy over
        # * zzzzz is removed once it's >= 1 hour old?
        wget(resp.text)
        randstr = os.path.split(resp.text)[-1]
        shutil.move(randstr, assessment + '.tar.gz')
        print("%s downloaded" % (assessment + '.tar.gz'))
        # gunzip and untar and move to appropriate dir

def hi():
    xs = ['hi', 'hello',
          'bonjour', 'hola', 'zdravstvuyte', 'nin hao', 'salve',
          'konnichiwa', 'guten tag', 'ola', 'anyoung haseyo', 
          'goddag', 'shikamoo', 'goedendag', 'yassas', 'dzien dobry',
          'selamat siang', 'merhaba', 'shalom', 'god dag']
    return random.choice(xs)

def main__():
    config = readconfig()
    user = getdefaultuser(config)    
    email = getdefaultemail(config)    
    course = getdefaultcourse(config)
    assessment = getdefaultassessment()
    assessmentpath = getdefaultassessmentpath(assessment)

    while 1:
        # 2023-09-02 copy this from above
        config = readconfig()
        user = getdefaultuser(config)    
        email = getdefaultemail(config)    
        course = getdefaultcourse(config)
        assessment = getdefaultassessment()
        assessmentpath = getdefaultassessmentpath(assessment)

        print()
        print("%s this is alex" % hi())
        print("[u]ser  : %s" % hide(user))
        print("[e]mail : %s" % email)
        print("[c]ourse:", course)
        print("[w]ork  :", assessment)
        print("[p]ath  :", assessmentpath)
        print("[s]ubmit    [a]lex update")
        print("[t]ar-gzip  ")
        print("[h]elp      [D]oom")
        print("[q]uit")
        #print("[L]aundry")
        #print("[d]ownload")
        #print("[t]ar (and gzip)")
        print("report bugs to dr.liow")
        option = input('option: ').strip()
        if option in ['','q']: sys.exit()
        elif option == 'u': user = getuser(config)
        elif option == 'e': email = getemail(config)
        elif option == 'c': course = getcourse(config)
        elif option == 'w': assessment = getassessment()
        elif option == 'p': assessmentpath = getassessmentpath(assessment)
        elif option == 'r': replaceemail()
        elif option in '?hH': help()
        elif option in 'lL': laundry()
        elif option == 'a': update(config)
        elif option == 'D': doom()
        elif option == 's': ui_submit_assessment(config, user, course, assessment, assessmentpath)
        elif option in 'd': download(config, course, assessment)
        elif option in 'tT': targzip()
        else: print("\nincorrect option\n")

def main():
    
    if len(sys.argv) > 1:
        commandline()

    try:
        main__()
    except KeyboardInterrupt:
        print("\nCtrl-C ... halting ...")
    except EOFError:
        print("\nCtrl-D ... halting ...")
    except Exception as e:
        print("")
        print(60*"=")
        print("help ... send this to dr.liow ...\n")
        traceback.print_exc(file=sys.stdout)
        print(60*"=")
        
def commandline():
    if sys.argv[1] == 'replaceemail':
        if len(sys.argv) > 2:
            filename = sys.argv[2]
            replaceemail(filename)
        else:
            replaceemail()
    sys.exit()
if __name__ == '__main__':

    main()

    
