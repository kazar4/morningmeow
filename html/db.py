#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('../test2.db')
print "Opened database successfully";

conn.execute('''CREATE TABLE DATABASE
         (PHONE_NUMBER TEXT,
         NAME           TEXT,
         MESSAGE            TEXT,
         TIMEZONE        TEXT,
         Carrier         TEXT,
         PREMIUM TEXT,
         CAN_SEND TEXT);''')
print "Table created successfully";

conn.close()