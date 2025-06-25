"""
Create the class website and put it in w/

w/
  index.html
  a/    <------ assignment
  c/    <------ course info
  g/    <------ grade report
  n/    <------ notes
  l/    <------ lab
  p/    <------ project
  q/    <------ quizzes
  m/    <------ miscellaneous
  
In the student's location it should look like the above
"""
import os, datetime
now = str(datetime.datetime.now())

def cmd(s):
    print(s)
    #input("continue ...")
    os.system(s)

def writefile(filename, s):
    f = open(filename, 'w'); f.write(s); f.close()
    
def semester():
    SEMESTER = ''
    import datetime
    NOW = datetime.datetime.now()
    YEAR = int(NOW.year)
    MONTH = int(NOW.month)
    if MONTH in [8,9,10,11,12]:
        SEASON = 'FALL'
    elif MONTH in [1,2,3,4,5]:
        SEASON = 'SPRING'
    #else:
    #    raise Exception("no season ... is month incorrect?")
    else:
        print("WARNING: month is incorrect ... defaults to spring")
        SEASON = 'SPRING'
    SEMESTER = "%s%s" % (SEASON, YEAR)
    return SEMESTER

def ahref(BASE, text, from_file=None, to_file=None, url=None):
    """
    copy file with path from_file to to_file and create an a href tag
    If url is None:
        a URL resrouce on the web is used (no local file used) 
    If url is not None:
        a local file is used
    """

    if url == None:
        cmd('cp "%s" "%s"' % (from_file, os.path.join(BASE, to_file)))
        return '<a href="%s">%s</a>' % (to_file, text)
    else:
        return '<a href="%s">%s</a>' % (url, text)


def ul(xs):
    ys = []
    in_ul = 0
    for x in xs:
        if x.startswith('*'):
            if in_ul == 0:
                ys.append("<p>%s</p><ul>" % x[1:])
            else:
                ys.append("</ul><p>%s</p><ul>" % x[1:])
            in_ul += 1
        else:
            ys.append('<li> %s\n' % x)
            #ys = [('<li> %s\n' % x) for x in xs]
    if in_ul > 0:
        ys.append('</ul>')
    z = '\n'.join(ys)
    return '''
<ul>
%s
</ul>''' % z


def get_videos_html(videos):
    if videos:
        return """
<!--
<p>
<a href='%s'>Click here for the class videos</a>.
You will need to log in to youtube using your college email address.
</p>

<p>
The videos are uploaded to youtube and as far as I know
I have turned off advertising.
The videos are set to private and only students in the class can view the
videos (after logging into youtube with their college email address).
The videos are only for class use.
Do not distribute outside the class.
I will record and upload as many class meetings as I can, but
managing the class videos is very time consuming so I will not
        guarantee that all class meetings are recorded and uploaded.
</p>
        -->
<p>
        I will try to turn on zoom recording at the beginning of the class.
        However note that sometimes the camera in the classroom does not
        turn on.
        To view the recordings (if any), go to D2L, look for the class,
        and look for cloud recordings.
        """ % videos
    else:
        return """There are no video recordings for this class."""


def submission(course_number):
    course_number = course_number.lower()
    #if course_number in ['ciss145', 'ciss240']:
    if course_number in []:
        if course_number == 'ciss240':
            ext = 'cpp'
        else:
            ext = 'py'
        return '''
<ul>
<li> Email your cpp source files to <a href="mailto:yliow@ccis.edu">yliow@ccis.edu</a>.
     You must email using your college email account because that is how I identify you.
<li> The name of your source files must follow the following format:
     For question 1 of assignment 1, the source file must be named a01q01.%(ext)s.
     For question 2 of assignment 5, the source file must be named a05q02.%(ext)s.
<li> If you are submitting for assignment a01, the subject line of your email must be "%(course_number)s a01".
     If you are submitting for assignment a05, the subject line of your email must be "%(course_number)s a05".
<li> You can submit any number of source files. For instance if the assignment has 5 questions, you can submit
just the first two once you're done with them.
<li> You can submit as many times as you like as long as it is within the deadline. The latest one is used for grading
purposes.
</ul>
It's a good idea to include yourself (as CC) in the email.
''' % {'course_number':course_number, 'ext':ext}
    else:
        return '''
<ul>
<li> I suggest you have the following organization for your assignments.
     For assignment a01,
     create a folder <font face='Courier New, monospace'>a01</font>.   
     In
     <font face='Courier New, monospace'>a01</font>,
     create a folder for each question.
     For Q1, create folder
     <font face='Courier New, monospace'>a01q01</font>
     in
     <font face='Courier New, monospace'>a01</font>.
     Etc.
     Put all your work for Q1 in
     <font face='Courier New, monospace'>a01q01</font>.
     Etc.
     In your laptop, your directory structure for this course might look like
     this:
<pre>
%(course_number)s
|
+--- a
     |
     +--- a01
          |
          +--- a01q01
          |    |
          |    +-- [file(s) for a01q01]
          |
          +--- a01q02
          |    |
          |    +-- [file(s) for a01q02]
          |
     ...     
</pre>
        Do likewise for other assignments (a02, a03,...).
I also suggest you have the same organization for your quizzes:
<pre>
%(course_number)s
|
+--- q
     |
     +--- q0101
     |    |
     |    +-- [file(s) for q0101]
     |     
     +--- q0102
          |
          +-- [file(s) for q0102]
     ...     
</pre>
The number of the quizzes might vary from the above.
For quizzes, there is usually only one folder for each quiz.

<li> There are two ways to submit work (assignments, quizzes, project):

        <ul>

        <li>
        Using <font face='Courier New, monospace'>alex</font>:

            <ul>
                <li> In most cases you will be running 
                <font face='Courier New, monospace'>alex</font>
                in our fedora virtual machine.
                Here's the
                <a href="https://yliowsubmit.pythonanywhere.com/ul">link
                to the instructions on installing and running <font face='Courier New, monospace'>alex</font></a>
                (bottom half of webpage).
                <li>You can also talk to <font face='Courier New, monospace'>alex</font> using a web browser.
                Here's the
                <a href="https://yliowsubmit.pythonanywhere.com/ul">link to the webform</a> (top half of webpage).        
            </ul>
        
        <li>
        By email when your work is rejected by <font face='Courier New, monospace'>alex</font>:
        <ul>
        <li>
        If your work is very huge (example: projects in some higher level classes), 
        <font face='Courier New, monospace'>alex</font>
        might reject it.
        This is not common.
        So you might want to make sure you remove redundant files before you
        try to submit your work.
        Make sure you remove executable files from your directories.
                 You should only have text source files
                 (example: <font face="Courier New, monospace">*.py</font>,
                 <font face="Courier New, monospace">*.cpp</font>,
                 <font face="Courier New, monospace">*.h</font>, etc.)
                 For some projects, you might have image and audio files.

        <li>
        You want to make sure I know you are emailing me your work.

        <li>
        Here are the steps to create <font face='Courier New, monospace'>submit.tar.gz</font>
        for submission by email (or to <font face='Courier New, monospace'>alex</font>).
        Suppose you are submitting directory
        <font face='Courier New, monospace'>a01</font>
                 <ul>
                 <li> Tar your a01 by executing
                 "<font face='Courier New, monospace'>tar -cvf submit.tar a01</font>"
                 in the directory
                 containing
                 <font face="Courier New, monospace">a01</font>
                 (i.e., while you're in directory
                 <font face='Courier New, monospace'>a</font>).
                 This produces the file
                 <font face="Courier New, monospace">submit.tar</font>.
                 
                 <li> Compress your tar file by doing
                 "<font face='Courier New, monospace'>gzip submit.tar</font>".
                 This produces the file
                 <font face="Courier New, monospace">submit.tar.gz</font>.
                 </UL>
        
                 <li> Using your college email account,
                 email
                 <a href="mailto:yliow.submit@gmail.com">yliow.submit@gmail.com</a>
        (check with me if this is the email address to use)
                 with your
                 <font face="Courier New, monospace">submit.tar.gz</font> 
                 as an attachment.
                 The subject line of the email must be
                 "<font face='Courier New, monospace'>%(course_number)s a01</font>".         
                 A copy of your email is probably in your sent folder.
                 If not, then it's a good idea to include yourself (as CC) in the email.
            
            </ul>

        </ul>
</ul>
        
<!--
<p>
[NEW. I've rewritten the submission collector program -- you can now use
bzip2, gzip, or xz for compression:
The attachment can now be
<font face="Courier New, monospace">a01.tar.bz2</font>
or
<font face="Courier New, monospace">a01.tar.gzip</font>
or
<font face="Courier New, monospace">a01.tar.xz</font>
.
On the Windows platform, using 7-zip, you can create
<font face="Courier New">a01.zip</font>.
The ZIP file format is a mess because of patent related issues for
some newer
ZIP versions. If you submit zip files, you are in danger of getting a 0
for your submission.]
</p>
-->
''' % {'course_number': course_number.lower()}


def quiz(course_number):
    course_number = course_number.lower()
    ret = r'''
Quizzes might be numbered with two numbers where the first refers to the notes.
For instance quiz q0102 is the second (02) quiz on the first
(01) set of notes.
Quizzes are usually printed and handed out in class.
<br><br>
    '''
    if course_number in []: # ['ciss145', 'ciss240']:
        if course_number == 'ciss240':
            ext = 'cpp'
        else:
            ext = 'py'
        return '''
Suppose the link is of the form q*.tar.gz, say q1201.tar.gz. Do the following:
    <ul>
    <li> Run firefox in your virtual machine and download the file from
    the class website.
    q1201.tar.gz will probably be downloaded into your Downloads directory.
    Execute "cp ~/Downloads/q1201.tar.gz ~/ciss240/q/" if your ciss240 is in your home directory.
    Go to your ciss240/q/ directory.
    <li> Execute "gunzip q1201.tar.gz" to get q1201.tar.
    <li> Execute "tar -xvf q1201.tar" to get directory q1201.
    <li> Go into directory q1201.
    <li> Execute "make" to compile and view the pdf.
        Enter your answer(s) in main.tex and execute "make" to recompile and view the pdf.
        (There are instructions in the pdf.)
    <li>Run
    <a href='https://docs.google.com/document/d/1KeA5yUidxdIbImR7OlvEChweyhMuuBdIyv9NSUxuLoI/edit?usp=sharing'>alex</a>
    to submit your work.
        (Click on the alex link to see alex page for installation and usage example.) 
    </ul>
''' % {'course_number': course_number.lower()}
    else:
        return '''
Suppose the link is of the form q*.tar.gz, say q1201.tar.gz. Do the following:
    <ul>
    <li> Run firefox in your virtual machine and download the file from
    the class website.
    q1201.tar.gz will probably be downloaded into your Downloads directory.
    Move q1201.tar.gz to your quiz folder by 
    executing "mv ~/Downloads/q1201.tar.gz ~/%(course_number)s/q/" 
        if your %(course_number)s directory is in your home directory.
        Go to your %(course_number)s/q directory
    <li> Execute "gunzip q1201.tar.gz" to get q1201.tar.
    <li> Execute "tar -xvf q1201.tar" to get directory q1201.
    <li> Go into directory q1201.
    <li> Execute "make" to compile and view the pdf.
        Enter your answer(s) in main.tex.
        (There are instructions in the pdf.)
        Execute "make" to recompile and view the pdf.        
    <li>
    Run
    <a href='https://docs.google.com/document/d/1KeA5yUidxdIbImR7OlvEChweyhMuuBdIyv9NSUxuLoI/edit?usp=sharing'>alex</a>
    to submit your work.
    </ul>
''' % {'course_number': course_number.lower()}



#==============================================================================
# Create class website
#==============================================================================
def classwebsite(BASE,
                 COURSE_NUMBER,
                 COURSE_NAME,
                 GOOGLE_GROUP,
                 courseinfo,
                 notes,
                 assignments,
                 quizzes,
                 projects,
                 announcements,
                 miscellaneous=[],
                 copy_website=True,
                 diary=None,
                 calendar='',
                 videos=None
                 ):

    title = '%s %s' % (COURSE_NUMBER, COURSE_NAME)

    if diary == None:
        diary = 'http://github.com/yliow/%s-github' % (COURSE_NUMBER.lower())
    import os
    if os.path.isdir(BASE):
        print("%s exists ... moving it to %s-old" % (BASE, BASE))
        if os.path.isdir('%s-old' % BASE):
            cmd("rm -rf '%s-old'" % BASE)
        cmd('mv %s %s-old' % (BASE, BASE))
    cmd('rm -rf %s' % BASE)
    cmd('mkdir %s' % BASE)
    cmd('mkdir %s/c' % BASE)
    cmd('mkdir %s/n' % BASE)
    cmd('mkdir %s/a' % BASE)
    cmd('mkdir %s/q' % BASE)
    cmd('mkdir %s/p' % BASE)
    cmd('mkdir %s/m' % BASE)

    xs = [ahref(BASE, a, b, c) for a,b,c in courseinfo]
    courseinfo_html = ul(xs)

    diary_html = ''

    print("notes:")
    for x in notes: print(x)
    #xs = [ahref(BASE, a, b, c) for a,b,c in notes]
    xs = []
    for note in notes:
        print("note:", note, len(note))
        if len(note) == 1:
            xs.append('*' + note[0]) # * means do not <li> in a <p>
        elif len(note) == 3:
            a,b,c = note
            xs.append(ahref(BASE, a, b, c))
        elif len(note) == 6:
            # ADDED 2020/09/24
            a,b,c,d,e,f = note
            xs.append(ahref(BASE, a, b, c) + ' | ' + ahref(BASE, d, e, f))
        else:
            print(note)
            raise Exception("note length not 1 or 3 or 6")
    notes_html = ul(xs)

    videos_html = get_videos_html(videos) # ???

    # check ...
    for _ in assignments:
        if len(_) != 7:
            print("assignment does not have length 7")
            print(_)
            raise ValueError
    xs = ['%s | %s. %s' % (ahref(BASE, a, b, c), ahref(BASE, d, e, f), g) \
          for a,b,c,d,e,f,g in assignments]
    assignments_html = ul(xs)

    submission_html = submission(COURSE_NUMBER)

    xs = ['%s | %s. %s' % (ahref(BASE, a, b, c), ahref(BASE, d, e, f), g) \
          for a,b,c,d,e,f,g in quizzes]
    quizzes_html = ul(xs)

    xs = ['%s | %s. %s' % (ahref(BASE, a, b, c), ahref(BASE, d, e, f), g) \
          for a,b,c,d,e,f,g in projects]
    projects_html = ul(xs)

    xs = [ahref(BASE, 'Class google group', url=GOOGLE_GROUP)]
    announcements_html = ul(xs)

    xs = [ahref(BASE, a, b, c) for a,b,c in miscellaneous]
    miscellaneous_html = ul(xs)

    website = '''
<html>
<body style="font-family: arial">


<a name="top"></a>
<h1>%(title)s</h1>

[Build: %(now)s]

<br><br>
    
<hr>
Quicklinks:
<a href='#diary'>Github</a> | 
<a href='#notes'>Notes</a> | 
<a href='#videos'>Videos</a> | 
<a href='#assignments'>Assignments</a> | 
<a href='#quizzes'>Quizzes</a> |
<a href='#project'>Project</a> |
<a href='#calendar'>Calendar</a> |
<a href='#submission'>Submission</a> |    
<hr>
    
<h2>Important</h2>

Under no circumstances are you allowed to share any information
on this webpage with anyone not in this class.
If you do so, I will consider your act as helping someone plagiarize.

Furthermore, if you are retaking this class, then all the work submitted
must be your work done during the current semester.
Using for instance solutions obtained from the last time(s) you took
this class is considered plagiarism.

<h2>General Course Information</h2>
%(courseinfo_html)s

<h2>Announcements</h2>

I create a google group for each class.
This allows the class (instructor and students) to communicate quickly.
Messages are set to immediate delivery so that you can get messages from me
or your classmates right away.
The messages are sent to your college email account.
You can also access the google group to read messages or search for previous
messages -- you will need to login using your
college email account information.
%(announcements_html)s
If you prefer to manage messages your way, you can do the following:
<ul>
<li> Login to google.
Go to the class's google group, change your settings for the group.
You can for instance set your email delivery to none and check the google
group's website for messages. 
<li> Set filters in your email account.
For instance you can create a folder in your email account and have
email from
the google group auto-moved from inbox to this folder.
</ul>
If you want to do any of the two above but have problems or questions on
how to do that, just talk to me.
                                        

<a name="diary"></a>
<h2>Github <a href="#top">[goto top]</a> </h2>
    
Miscellaneous notes, code, etc. from class meetings (if any) are stored
in a github repo (repository).
    
<ul>
<li> <a href='%(diary)s'>%(diary)s</a>
</ul>


<a name="notes"></a>
<h2>Notes <a href="#top">[goto top]</a> </h2>
%(notes_html)s

<a name="videos"></a>
<h2>Videos <a href="#top">[goto top]</a> </h2>
%(videos_html)s



<a name="assignments"></a>
<h2>Assignments <a href="#top">[goto top]</a> </h2>

%(assignments_html)s

For higher level classes:
For some classes the links above might point to a tar-zipped file with a filename such as a01.tar.gz
Download the file in the virtual macbine, unzip the file by executing "gunzip a01.tar.gz".
This gives you a file named "a01.tar". Execute "tar -xvf a01.tar" to get an a01 directory.


<a name="submission"></a>    
<h2>Submission  <a href="#top">[goto top]</a></h2>
%(submission_html)s

<a name="quizzes"></a>
<h2>Quizzes <a href="#top">[goto top]</a> </h2>

%(quiz_html)s

%(quizzes_html)s


    
<a name="project"></a>
<h2>Project <a href="#top">[goto top]</a> </h2>

%(projects_html)s

<h2>Miscellaneous</h2>
%(miscellaneous_html)s



    
<a name="calendar"></a>
<h2>Calendar, etc. <a href="#top">[goto top]</a> </h2>

<ul>
<li><a href="http://yliow.github.io">Dr.Liow's website</a>
</ul>

%(calendar)s
</body>
</html>
''' % \
{
    'now': now,
    'title':title,
    'announcements_html':announcements_html,
    'submission_html': submission_html,
    'diary':diary,
    'notes_html':notes_html,
    'assignments_html':assignments_html,
    'quiz_html': quiz(COURSE_NUMBER),
    'quizzes_html':quizzes_html,
    'projects_html':projects_html,
    'courseinfo_html':courseinfo_html,
    'miscellaneous_html':miscellaneous_html,
    'calendar':'<center>%s</center>'  % calendar,
    'videos_html': videos_html,
}

    writefile('%s/index.html' % BASE, website)

    if copy_website:
        course_number = COURSE_NUMBER.lower()
        print("building %s.tar.bz2 ..." % course_number)
        import os
        cwd = os.getcwd()
        print("cwd:", cwd)

        # WHY index.html empty???
        cmd('rm -rf %s' % course_number)
        cmd('cp -r w %s' % course_number)

        cmd('rm -rf %s.tar' % course_number)
        cmd('tar -cvf %s.tar %s' % (course_number, course_number))
        
        cmd('rm -rf %s.tar.bz2' % course_number)
        cmd('bzip2 %s.tar' % course_number)
        
        #os.system('rm -rf %s' % course_number)
