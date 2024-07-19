import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
#from email.mime.image import MIMEImage
from email import encoders # 2021/3/17: python 3
#import mimetypes
import datetime

#from util import cstdatetimestr

def sendgmail(to_='yliow@ccis.edu',
              from_='yliow.submit@gmail.com',
              subject='[NO SUBJECT]',
              text='this is a test',
              html='',
              attach=None, # list of paths or path or None
              ):

    try:
        if isinstance(attach, str):
            attaches = [attach]
        elif attach == None:
            attaches = []
        elif isinstance(attach, list): 
            attaches = attach

        sender_pass = 'mteazcfrizcrlnco' # app pwd

        msg = MIMEMultipart()
        msg['From'] = from_
        msg['Subject'] = subject
        alternative = MIMEMultipart('alternative')
        msg.attach(alternative)
        if text: alternative.attach(MIMEText(text))
        if html: alternative.attach(MIMEText(html, 'html'))

        # attachments
        for path in attaches:
            if not os.path.isfile(path):
                raise BaseException("email ERROR: path %s cannot be found" % path)
            ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            part = MIMEBase(maintype, subtype)
            part.set_payload(open(path, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment',
                            filename=os.path.split(path)[-1])
            msg.attach(part)
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(from_, sender_pass)
        session.sendmail(from_, to_, msg.as_string())
        session.quit()
        return ('email sent to %s' % to_)
    except Exception as e:
        print(e)
        NOW = datetime.datetime.now()
        raise Exception("ERROR: Please report error  %s" % NOW)

if __name__ == '__main__':
    NOW = datetime.datetime.now()
    sendgmail(to_=['yliow@yahoo.com'],
              from_='yliow.submit@gmail.com',
              subject='this is a test %s' % NOW,
              text='this is a test',
              html='<html><body><h1>This is a test</h1>This is a test</body></html>',
              attach=['myemail.py',
                      '/home/student/yliow/Documents/work/cc/courses/cpp-book/n/01-print-strings/01-print-strings.pdf']
              )
