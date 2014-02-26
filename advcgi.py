#!/usr/bin/env python

from cgi import FieldStorage
from os import environ
from cStringIO import StringIO
from urllib import quote, unquote
from string import capwords, strip, split, join

class AdvCGI:

    header = 'Content-Type: text/html\n\n'
    url = '/cgi-bin/advcgi.py'

    formhtml = '''<HTML><HEAD><TITLE>
Welcome to Yagra</TITLE></HEAD>
<BODY><H2>New User Information</H2>
<FORM METHOD=post ACTION="%s" ENCTYPE="multipart/form-data">
<H3>My Cookie Setting</H3>
<LI><CODE><B>CPPuser = %s</B></CODE>
<H3>Enter cookie value<BR>
<INPUT NAME=cookie value="%s">(<I>optional</I>)</H3>
<H3>Enter your name<BR>
<INPUT NAME=person value="%s">(<I>required</I>)</H3>
<H3>What languages can you program in?
(<I>at least one required</I>)</H3>
%s
<H3>Enter file to upload</H3>
<INPUT TYPE=ile NAME=upfile VALUE="%s" SIZE=45>
<P><INPUT TYPE=submit>
</FORM></BODY></HTML>'''

    lang_set = ('Python', 'PERL', 'Java', 'C++', 'PHP', 'C', 'JavaScript')
    lang_item = '<INPUT TYPE=checkbox NAME=lang VALUE="%s"%s> %s\n'

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
            self.who, lang_str, self.fn = split(self.cookies['info'], ':')
            self.langs = split(lang_str, ',')
        else:
            self.who = self.fn = ''
            self.langs = ['Python']

    def show_form(self):
        self.get_cpp_cookies()
        lang_str = ''
        for each_lang in AdvCGI.lang_set:
            if each_lang in self.langs:
                lang_str = lang_str + AdvCGI.lang_item %\
                         (each_lang,' CHECKED', each_lang)
            else:
                lang_str = lang_str + AdvCGI.lang_item %\
                         (each_lang,'', each_lang)

        if not self.cookies.has_key('user') or self.cookies['user'] == '':
            cookie_status = '<I>(cookie has not been set yet)</I>'
            user_cook = ''
        else:
            user_cook = cookie_status = self.cookies['user']

        print AdvCGI.header + AdvCGI.formhtml % (AdvCGI.url,\
                  cookie_status, user_cook, self.who, lang_str, self.fn)

    errhtml = '''<HTML><HEAD<TITLE>
Welcome to Yagra</TITLE></HEAD>
<BODY><H3>ERROR</H3>
<B>%s</B><P>
<FORM><INPUT TYPE=button VALUE=Back ONCLICK="window.history.back()"></FORM>
</BODY></HTML>'''

    def show_error(self):
        print AdvCGI.header + AdvCGI.errhtml % (self.error)

    reshtml = '''<HTML><HEAD<TITLE>
Welcome to Yagra</TITLE></HEAD>
<BODY><H2>Your Register Informations</H2>
<H3>Your Cookie value is: <B>%s</B></H3>
<H3>Your name is: <B>%s</B></H3>
<H3>Your can program in the following languages:</H3>
<UL>%s</UL>
<H3>Your upload file...<BR>
Name:<I>%s</I><BR>
Contents:</H3>
<PRE>%s</PRE>
Click <A HREF="%s"><B>here</B></A> to return to form.
</BODY></HTML>'''

    def set_cpp_cookies(self):
       for each_cookies in self.cookies.keys():
           print 'Set-Cookie: CPP%s=%s; path=/' % \
               (each_cookies, quote(self.cookies[each_cookies]))

    def do_results(self):
        MAXBYTES = 1024
        lang_list = ''
        for each_lang in self.langs:
            lang_list = lang_list + '<LI>%s<BR>' % each_lang

        file_data = ''
        while len(file_data) < MAXBYTES:
            data = self.fp.readline()
            if data == '':
                break
            file_data = file_data + data
        else:
            file_data = file_data + '...<B><I>(file truncated due to size)</I></B>'
        self.fp.close()
        if file_data == '':
            file_data = file_data + '...<B><I>(file upload error or file not given)</I></B>'
        file_name = self.fn

        if not self.cookies.has_key('user') or self.cookies['user'] == '':
            cookie_status = '<I>(cookie ha not been set yet)</I>'
            user_cook = ''
        else:
            user_cook = cookie_status = self.cookies['user']

        self.cookies['info'] = join([self.who, join(self.langs, ','), file_name], ':')
        self.set_cpp_cookies()
        print AdvCGI.header + AdvCGI.reshtml % (cookie_status, self.who, lang_list,\
                                          file_name, file_data, AdvCGI.url)

    def go(self):
        self.cookies = {}
        self.error = ''
        form = FieldStorage()
        if form.keys() == []:
            self.show_form()
            return
       
        if form.has_key('person'):
            self.who = capwords(strip(form['person'].value))
            if self.who == '':
                self.error = 'Your name is required. (blank)'
        else:
            self.error = 'Your name is required. (missing)'

        if form.has_key('cookie'):
            self.cookies['user'] = unquote(strip(form['cookie'].value))
        else:
            self.cookies['user'] = ''

        self.langs = []
        if form.has_key('lang'):
            lang_data = form['lang']
            if type(lang_data) == type([]):
                for each_lang in lang_data:
                    self.langs.append(each_lang.value)
            else:
                self.langs.append(lang_data.value)
        else:
            self.error = 'At least one language required.'

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
