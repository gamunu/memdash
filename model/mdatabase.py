#!/usr/bin/env python3
'''Database handling functions'''

import MySQLdb
from config import Config

class MDatabase(object):
    '''Database handling functions'''

    @staticmethod
    def connect():
        return MySQLdb.Connection(user=Config.DB_USER, passwd=Config.DB_PASSWORD, db=Config.DB_NAME)
