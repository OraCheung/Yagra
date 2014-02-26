#!/usr/bin/python

import cgi
import os

import db

header = 'Content-Type: text/html\n\n'
url = '/cgi-bin/login.py' 
reshtml = '''<HTML><HEAD><TITLE>
Yagra Logining</TITLE></HEAD>
<BODY><H2>Welcome to Yagra</H2>
<H3>Your Login Name is: <B>%s</B></H3>
<H3>Your Login Password is: <B>%s</B></H3>
<H3>Upload Head Photo is:</H3>
%s
<BR>Click <A HREF="%s"><B>here</B></A> to return to login.
</BODY></HTML>'''


form =cgi.FieldStorage()
if form.has_key('personName'):
    name = form['personName'].value
else:
    name = ''
if form.has_key('personPassword'):
    passwd = form['personPassword'].value
else:
    passwd = ''

python_db = db.MyDB()

result = python_db.select_user(name, passwd)
if result == 1:
    python_db.update_status(name,1)
    image = '<IMG SRC="/cgi-bin/image/%s.jpg" width = "256" height = "256" >' % (name)
    print header + reshtml % (name, passwd, image, url)
else:
    print header+"You passwd is error!"
