#!/usr/bin/env python

import cgi

import db

url = '/cgi-bin/login.py'
header = 'Content-Type: text/html\n\n'
reshtml = '''<HTML><HEAD><TITLE>
Yagra Loginout</TITLE></HEAD>
<BODY><H2>Welcome to Yagra</H2>
<H3><B>%s</B>&nbspis loginouted!</H3>
<BR>Click <A HREF="%s"><B>here</B></A> to return to login.
</BODY></HTML>'''
print header
form = cgi.FieldStorage()
if form.has_key('personName'):
    name = form['personName'].value
    python_db = db.MyDB()
    python_db.update_status(name,0)
    print reshtml % (name, url)
