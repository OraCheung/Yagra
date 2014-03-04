#!/usr/bin/env python

import hashlib


class MyMd5(object):
    "a new class for md5 encrypting "

    def __init__(self,input):
        self.md5 = hashlib.md5()
        self.md5.update(input)

    def get_hex(self):
        return self.md5.hexdigest()

if __name__ == '__main__':
    my_md5 = MyMd5("test")
    print my_md5.get_hex()
