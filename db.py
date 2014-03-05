#!/usr/bin/env python

import os

import MySQLdb

from md5encry import MyMd5


class MyDB(object):
    'class defination for using MySql'

    def __init__(self): 
        "init Mysql and choose database python"
        try:
            f = open('mysql.txt', 'r')
            (username, password, database) = f    
            f.close()
            username = username.strip('\n')
            password = password.strip('\n')
            database = database.strip('\n')
            self.conn = MySQLdb.connect(host='localhost', user=username, passwd=password, port=3306)
            self.cur = self.conn.cursor()
            self.conn.select_db(database)

        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def insert_user(self, user, passwd):
        "insert user passwd into the Table User"
        try:
            md5 = MyMd5(passwd)
            hash_passwd = md5.get_hex() 
            pic_name = user + '@' + passwd
            md52 = MyMd5(pic_name)
            hash_pic = md52.get_hex() 
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
        "delete from the Table User"
        try:
            md5 = MyMd5(passwd)
            hash_passwd = md5.get_hex()
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
        "update the Table User for the user status"
        try:
            value = []
            if status ==1:
                value.append(1)
                value.append(user)
            #    print 'update status %d,value is %s' % (value[0], value[1])
                count = self.cur.execute('update User set login_status=%s,\
                                     login_time=now() where user=%s',value) 
                if count != 1: 
                #    print "Change User Status Error!"
                    pass
                else:
                    self.conn.commit()
            else:
                value.append(0)
                value.append(user)
                count = self.cur.execute('update User set login_status=%s \
                                        where user=%s',value)
                if count != 1: 
                    pass
                else:
                    self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def select_user(self, user, passwd):
        'return the number of user for search'
        try:
            md5 = MyMd5(passwd)
            hash_passwd = md5.get_hex()
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
