#!/usr/bin/python

import cgi
import os

from md5encry import MyMd5
import db

header = 'Content-Type: text/html\n\n'
url = '/cgi-bin/login.py' 
loginout_url = '/cgi-bin/loginout.py'
logintest_url = '/cgi-bin/logintest.py'

reshtml = '''<HTML><HEAD><TITLE>
Yagra Logining</TITLE></HEAD>
<BODY><H2>Welcome to Yagra</H2>
<H3>Your Login Name is: <B>%s</B></H3>
<H3>Your Login Password is: <B>%s</B></H3>
<H3>Upload Head Photo is: %s.jpg</H3>
<FORM action="/cgi-bin/logintest.py" METHOD=post ENCTYPE="multipart/form-data">
%s
<BR><H3>Change Head Photo:</H3>
<INPUT TYPE="hidden" Name="personName" value="%s" />
<INPUT TYPE="hidden" Name="personPassword" value="%s" />
<INPUT TYPE="file" ACCEPT=image/.jpg id=idChange Name="imageName" \
onchange="showImg(this.id,'idImg')"/>
<BR><INPUT TYPE="submit" VALUE=" SAVE " /></FORM>
Click <A HREF="%s"><B>here</B></A> to return to login.
<FORM METHOD=post ACTION="%s">
<INPUT TYPE=hidden Name="personName" Value="%s">
<BR><INPUT TYPE=submit VALUE="Login Out"></FORM>
%s
</BODY></HTML>'''

scripthtml = '''
<script type="text/javascript">
function Upload(){
    var url = getFileUrl("idChange");
    var dataSend = "image=" + url;
    alert(url)
    $.ajax(
    {
        type: "POST",
        url: "/cgi-bin/upload.py",
        data:dataSend,
        success:function(){
            alert("send success!");
        }
    });
}
function getFileUrl(sourceId){
    var url;
    if(navigator.userAgent.indexOf("MSIE")>=1){ //IE
        url = document.getElementById(sourceId).value;
    }else if(navigator.userAgent.indexOf("Firefox")>0) {
        url = window.URL.createObjectURL(document.getElementById(sourceId).files.item(0));
    }else if(navigator.userAgent.indexOf("Chrome")>0) {
        url = window.URL.createObjectURL(document.getElementById(sourceId).files.item(0));
    }
    return url;
}
function showImg(sourceId, targetId)
{   
    var url = getFileUrl(sourceId);
    var imgPre = document.getElementById(targetId);
    imgPre.src = url;
}
</script>'''

def process():
    form =cgi.FieldStorage()
    if form.has_key('personName'):
        name = form['personName'].value
    else:
        name = ''
    if form.has_key('personPassword'):
        passwd = form['personPassword'].value
    else:
        passwd = ''
    if form.has_key('imageName'):
        upfile = form['imageName']
        if upfile.file:
            pic2 = name + '@' + passwd
            md5 = MyMd5(pic2)
            hash_pic1 = md5.get_hex() 
            path = '/var/www/cgi-bin/image/%s.jpg' % (hash_pic1)
            file = open(path,'wb+')
            file.write(upfile.file.read())
            upfile.file.close()
            file.close() 
    
    python_db = db.MyDB()

    result = python_db.select_user(name, passwd)
    if result == 1:
        python_db.update_status(name,1)
        pic = name + '@' + passwd
        md51 = MyMd5(pic)
        hash_pic = md51.get_hex() 
        image = '<IMG SRC="/cgi-bin/image/%s.jpg" id=idImg width = "256" height = "256" style="display:block;"/>'\
                % (hash_pic) 
        print header + reshtml % (name, passwd, hash_pic, image, name, passwd,\
                                  url, loginout_url, name, scripthtml)
    else:
        print header+"You passwd is error!"

if __name__ == '__main__':
    process()
