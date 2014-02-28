#!/usr/bin/env python

from cgi import FieldStorage
from os import environ
from cStringIO import StringIO
from urllib import quote, unquote
from string import capwords, strip, split, join
import hashlib

import db

class AdvCGI:

    header = 'Content-Type: text/html\n\n'
    url = '/cgi-bin/advcgi.py'
    login_url = '/cgi-bin/login.py'

    formhtml = '''<HTML><HEAD><TITLE>
Welcome to Yagra</TITLE></HEAD>
<BODY><H2>New User Information</H2>
<FORM METHOD=post ACTION="%s" ENCTYPE="multipart/form-data">
<H3>Enter Your Name:<BR>
<INPUT NAME=personName value="%s">(<I>required</I>)</H3>
<H3>Enter Your Password<BR>
<INPUT NAME=personPassword value="%s" TYPE=password>(<I>required</I>)</H3>
<H3>Enter Your Password Again<BR>
<INPUT NAME=personPassword2 value="%s" TYPE=password>(<I>required</I>)</H3>
<H3>Enter file to upload</H3>
<INPUT TYPE=file NAME=upfile VALUE="%s" SIZE=45>
<P><INPUT TYPE=submit>
</FORM></BODY></HTML>'''


    def get_cpp_cookies(self):
        if environ.has_key('HTTP_COOKIE'):
            for each_cookie in map(strip, split(environ['HTTP_COOKIE'], ';')):
                if len(each_cookie) > 6 and each_cookie[:3] == 'CPP':
                    tag = each_cookie[3:7]
                    try:
                        self.cookies[tag] = eval(unquote(each_cookie[8:]))
                    except (NameError, SyntaxError):
                        self.cookies[tag] = unquote(each_cookie[8:])
        else:
            self.cookies['info'] = self.cookies['user'] = ''

        if self.cookies['info'] != '':
            self.passwd, self.fn = split(self.cookies['info'], ':')
            self.passwd2 = ''
        else:
            self.passwd = self.passwd2 = self.fn = ''

    def show_form(self):
        self.get_cpp_cookies()

        if not self.cookies.has_key('user') or self.cookies['user'] == '':
            cookie_status = '<I>(cookie has not been set yet)</I>'
            user_cook = ''
        else:
            user_cook = cookie_status = self.cookies['user']

        print AdvCGI.header + AdvCGI.formhtml % (AdvCGI.url,\
                   user_cook, self.passwd, self.passwd2, self.fn)

    errhtml = '''<HTML><HEAD><TITLE>
Welcome to Yagra</TITLE></HEAD>
<BODY><H3>ERROR</H3>
<B>%s</B><P>
<FORM><INPUT TYPE=button VALUE=Back ONCLICK="window.history.back()"></FORM>
</BODY></HTML>'''

    def show_error(self):
        print AdvCGI.header + AdvCGI.errhtml % (self.error)

    reshtml = '''<HTML><HEAD><TITLE>
Welcome to Yagra</TITLE></HEAD>
<BODY><H2>Your Register Informations</H2>
<H3>Your name is: <B>%s</B></H3>
<H3>Your password is: <B>%s</B></H3>
<IMG SRC="/cgi-bin/image/%s.jpg" width = '256' height = '256'>
<H3>Your upload file...<BR>
Name:<I>%s</I><BR></H3>
Click <A HREF="%s"><B>here</B></A> to return to login.
</BODY></HTML>'''

    def set_cpp_cookies(self):
       for each_cookies in self.cookies.keys():
           print 'Set-Cookie: CPP%s=%s; path=/' % \
               (each_cookies, quote(self.cookies[each_cookies]))

    def do_results(self):
        m = hashlib.md5()
        image_name = self.user + '@' + self.passwd
        m.update(image_name)
        hash_image = m.hexdigest() 
        path = '/var/www/cgi-bin/image/%s.jpg' % (hash_image)
        file = open(path, 'wb+')
        file.write(self.fp.read())
        self.fp.close()
        file.close()
        file_name = self.fn

        if not self.cookies.has_key('user') or self.cookies['user'] == '':
            cookie_status = '<I>(cookie ha not been set yet)</I>'
            user_cook = ''
        else:
            user_cook = cookie_status = self.cookies['user']

        self.cookies['info'] = join([self.passwd, file_name], ':')
        self.set_cpp_cookies()
        self.insertDB()
        print AdvCGI.header + AdvCGI.reshtml % (cookie_status, self.passwd,\
                                     hash_image, file_name,  AdvCGI.login_url)

    def insertDB(self):
        python_db = db.MyDB()
        python_db.insert_user(self.user, self.passwd) 

    def checkDB(self):
        python_db = db.MyDB()
        result = python_db.check_name(self.user)
        return result

    def go(self):
        self.cookies = {}
        self.error = ''
        form = FieldStorage()

        if form.keys() == []:
            self.show_form()
            return
       
        if form.has_key('personName'):
            self.cookies['user'] = unquote(strip(form['personName'].value))
            self.user = strip(form['personName'].value)
            result = self.checkDB()
            if result > 0:   #greater than 0 mean name had exist
                self.error = 'Your name %s is exist!' % (self.user)
            if self.user == '':
                self.error = 'Your name is required. (blacnk)'
        else:
            self.cookies['user'] = ''
            self.error = 'Your name is required. (missing)'

        if form.has_key('personPassword'):
            self.passwd = strip(form['personPassword'].value)
            if self.passwd == '':
                self.error = 'Your password is required. (blank)'
        else:
            self.error = 'Your password is required. (missing)'
        if form.has_key('personPassword2'):
            self.passwd2 = strip(form['personPassword2'].value)
            if self.passwd2 == '':
                self.error = 'Your password is required to input again. (blank)'
        else:
            self.error = 'Your password is required to input again. (missing)'

        if len(self.passwd) > 0 and len(self.passwd2) > 0:
            if self.passwd != self.passwd2: 
                self.error = 'Your passwords are not the same!'

        if form.has_key('upfile'):
            upfile = form['upfile']
            self.fn = upfile.filename or ''
            if upfile.file:
                self.fp = upfile.file
            else:
                self.fp = StringIO('(no data)')
                self.fn = ''
        else:
            self.fp = StringIO('(no file)')
            self.fn = ''

        if not self.error:
            self.do_results()
        else:
            self.show_error()
if __name__ == '__main__':
    page = AdvCGI()
    page.go()
