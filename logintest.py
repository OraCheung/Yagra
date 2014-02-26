#!/usr/bin/python

import cgi
import os

import db

os.environ['PYTHON_EGG_CACHE'] = '/tmp/'

print "Content-type:text/html\n\n"
print "Hello,World."

form =cgi.FieldStorage()
if form.has_key('personName'):
    name = form['personName'].value
    print form['personName'].value
else:
    name = ''
if form.has_key('personPassword'):
    passwd = form['personPassword'].value
    print form['personPassword'].value
else:
    passwd = ''

python_db = db.MyDB()
result = python_db.select_user(name,passwd)
if result == 1:
    print "You are login"
else:
    print "You passwd is error!"
