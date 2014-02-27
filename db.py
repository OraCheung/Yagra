#!/usr/bin/env python

import hashlib

import MySQLdb


class MyDB(object):
    'class defination for using MySql'

    def __init__(self): #init Mysql
        try:
            self.conn = MySQLdb.connect(host='localhost', user='root', passwd='orange', port=3306)
            self.cur = self.conn.cursor()
            self.conn.select_db('python')

        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def insert_user(self, user, passwd):
        try:
            md = hashlib.md5()
            md.update(passwd)
            hash_passwd = md.hexdigest()
            pic_name = user + '@' + passwd
            md2 = hashlib.md5()
            md2.update(pic_name)
            hash_pic = md2.hexdigest()
            value = [user, hash_passwd, hash_pic]
            count = self.cur.execute('insert into User (user, passwd, \
                     create_time, login_time, login_status, pic_name) VALUES \
                     (%s, %s, now(), now(), 0, %s)',value)
            if count != 1: 
                print "Insert New User Error!"
            else:
                self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def delete_user(self, user, passwd):
        try:
            md = hashlib.md5()
            md.update(passwd)
            hash_passwd = md.hexdigest()
            value = [user, hash_passwd]
            count = self.cur.execute('delete from User Where user = %s \
                       and passwd = %s', value) 
            if count != 1: 
                print "Delete User Error!"
            else:
                self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def __del__(self):
        try:
            self.cur.close()
            self.conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def update_status(self, user, status):
        try:
            value = []
            if status ==1:
                value.append(1)
                value.append(user)
            #    print 'update status %d,value is %s' % (value[0], value[1])
                count = self.cur.execute('update User set login_status=%s,login_time=now() where user=%s',value) 
                if count != 1: 
                    print "Change User Status Error!"
                else:
                    self.conn.commit()
            else:
                value.append(0)
                value.append(user)
                count = self.cur.execute('update User set login_status=%s where \
                                      user=%s',value)
                if count != 1: 
                    print "Change User Status Error!"
                else:
                    self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def select_user(self, user, passwd):
        'return the number of user for search'
        try:
            md = hashlib.md5()
            md.update(passwd)
            hash_passwd = md.hexdigest()
            value = [user, hash_passwd]
            self.cur.execute('select count(*) from User where user=%s \
                                       and passwd=%s', value)
            result = self.cur.fetchone()
            return result[0]
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def check_name(self, user):
        'check Tabler User whether the name is exist' 
        try:
            self.cur.execute('select count(*) from User where user=%s',user) 
            result = self.cur.fetchone()
            return result[0]
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
    db = MyDB()
    print db
    print db.select_user('ora','ora')
    print db.select_user('ora','oid')
    print db.delete_user('ki2', 'ki2')
    print db.insert_user('ki2', 'ki2')
    print db.update_status('ki',0)
    print db.check_name('ora3')
    print db.check_name('ora')
