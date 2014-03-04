#!/usr/bin/python

import cgi

header = 'Content-Type: text/html\n\n'

formhtml = '''<HTML><HEAD><TITLE>
Ora CGI Demo</TITLE></HEAD>
<BODY><H3>Welcome to Yagra: </H3> 
<FORM ACTION="/cgi-bin/logintest.py">
<B>Enter your Name:&nbsp&nbsp&nbsp&nbsp&nbsp</B><BR>
<INPUT TYPE=hidden NAME=action VALUE=edit>
<INPUT TYPE=text NAME=personName VALUE="" SIZE=15><BR>
<B>Enter your Password:</B><BR>
<INPUT TYPE=hidden NAME=action VALUE=edit>
<INPUT TYPE=password NAME=personPassword VALUE="" SIZE=15><BR>
<P><B>If you are new user,please first </B><a href="/cgi-bin/advcgi.py">REGISTER</a>
%s
<p><INPUT TYPE=submit VALUE="login" ></FORM></BODY></HTML>'''

fradio = '<INPUT TYPE=radio NAME=howmany VALUE="%s" %s> %s\n'

def show_form():
    friends = ''
    for i in [0, 10, 25, 50, 100]:
        checked = ''
        if i == 0:
            checked = 'CHECKED'
        friends = friends + fradio % (str(i), checked, str(i))
    friends = ''
    print header + formhtml % (friends)

reshtml = '''<HTML><HEAD><TITLE>
Ora CGI Demo</TITLE></HEAD>
<BODY><H3>Friends list for: <I>%s</I></H3>
Your name is: <B>%s</B><p>
You have <B>%s</B>friends.
</BODY></HTML>'''

def do_results(who, howmany):
    print header + reshtml % (who, who, howmany)
    print who,howmany

def process():
    form = cgi.FieldStorage()
    if form.has_key('personName'):
        who = form['personName'].value
    else:
        who = 'NEW ORA'

    if form.has_key('personPassword'):
        howmany = form['personPassword'].value
    else:
        howmany = 0

    if form.has_key('action'):
        do_results(who, howmany)
    else:
        show_form()

if __name__ == '__main__':
    process() 

