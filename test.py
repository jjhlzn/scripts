# coding:UTF-8
import httplib
import datetime
import time
import urllib
import json
import threading
from time import ctime,sleep
import smtplib
from email.mime.text import MIMEText

import sys

HOST = "115.29.199.187:8888"

def send_get_live_request():
    conn = httplib.HTTPConnection(HOST)
    jsondata = {"userInfo": {
                 "token": "xxxxxxxxxx",
                 "userid": "13706794299"},
			"client": {
                 'appversion': "1.0.3",
                 'model': "iPhone6s",
                 'osversion': "9.3",
                 'platform': "iPhone",
                 'screensize': "375*667"},
            "request": {
                 'song': {'id': 10},
                 'lastId': -1}				 }
 
    try:
        conn.request("POST", "/song/livecomments", json.dumps(jsondata), {"Content-type": "application/json"})
		
        res = conn.getresponse()
        data = res.read()
        print data
        print "success!\n"
    except Exception, e:
        print e
		
def send_add_live_request():
    conn = httplib.HTTPConnection(HOST)
    jsondata = {"userInfo": {
                 "token": "xxxxxxxxxx",
                 "userid": "13706794299"},
			"client": {
                 'appversion': "1.0.3",
                 'model': "iPhone6s",
                 'osversion': "9.3",
                 'platform': "iPhone",
                 'screensize': "375*667"},
            "request": {
                 'song': {'id': 10},
                 'comment': 'D',
				 'lastId': -1}				 }
 
    try:
        conn.request("POST", "/song/livecomments", json.dumps(jsondata), {"Content-type": "application/json"})
		
        res = conn.getresponse()
        data = res.read()
        print data
        print "success!\n"
    except Exception, e:
        print e

def main():
    conn = httplib.HTTPConnection(HOST)
    try:
		send_add_live_request()
		send_get_live_request()
    except Exception, e:
        print e
        return

main()