#coding:UTF-8
import httplib
import datetime
import time
import urllib2
import json

import smtplib  
from email.mime.text import MIMEText  

import sqlite3 as lite
import sys

TIME_OUT_SECOND = 1
SEND_INTERVAL = 10 * 60   #单位秒
WEB_NAME = '官网'
HOST = "218.244.149.169"

def init():
	#判断发送表是否存在
	try:
		con = lite.connect('monitor.db')
		cur = con.cursor()  
		cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='SEND_RECORD'")
		rows = cur.fetchall()
		is_table_exist = rows[0][0] > 0
		if not is_table_exist:
			 cur.executescript("""
				CREATE TABLE SEND_RECORD(Id INTEGER PRIMARY KEY, HOST_NAME TEXT, REPORT_TIME timestamp, TYPE TEXT, CONTENT TEXT);
				""")
		cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='PROBLEM'")
		rows = cur.fetchall()
		is_table_exist = rows[0][0] > 0
		if not is_table_exist:
			 cur.executescript("""
				CREATE TABLE PROBLEM(Id INTEGER PRIMARY KEY, HOST_NAME TEXT, HAPPEN_TIME timestamp, CONTENT TEXT);
				""")
		con.commit()
	except lite.Error, e:
		if con:
			con.rollback()
		print "Error %s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close() 
			
init()

mailto_list=['jinjunhang@hotmail.com'] 
mail_host="smtp.163.com"  #设置服务器
mail_user="hengdianworld1"    #用户名
mail_pass="abc123"   #口令 
mail_postfix="163.com"  #发件箱的后缀

def log_problem(content):
	sql = "insert into PROBLEM (HOST_NAME, HAPPEN_TIME, CONTENT) values ('"+HOST+WEB_NAME+"', '"+str(datetime.datetime.now())+"','"+content+"')"
	con = lite.connect('monitor.db')
	with con:
		cur = con.cursor()    
		cur.execute(sql)

def log_send_record(type,content):
	sql = "insert into SEND_RECORD (HOST_NAME, REPORT_TIME, TYPE, CONTENT) values ('"+HOST+WEB_NAME+"', '"+str(datetime.datetime.now())+"', '"+type+"', '"+content+"')"
	con = lite.connect('monitor.db')
	with con:
		cur = con.cursor()    
		cur.execute(sql)
		
def can_send(type):
	now = datetime.datetime.now()
	today6am = now.replace(hour=6,minute=0,second=0,microsecond=0)
	today0am = now.replace(hour=0,minute=0,second=0,microsecond=0)
	if now > today0am and now < today6am:
		return False
	sql = "select REPORT_TIME from SEND_RECORD where HOST_NAME='"+HOST+WEB_NAME+"' and TYPE ='"+type+"' order by REPORT_TIME desc"
	con = lite.connect('monitor.db')
	with con:
		cur = con.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if len(rows) == 0:
			return True
		last_time = rows[0][0]
		seconds = (datetime.datetime.now() -  datetime.datetime.strptime( last_time[0:last_time.find('.')].encode(),'%Y-%m-%d %H:%M:%S')).total_seconds()
		print 'last send time: ' + str(seconds)+"s ago"
		if seconds < SEND_INTERVAL:
			return False
		return True;

def send_sms(contents):
	if not can_send('SMS'):
		return;
	url = 'http://e.hengdianworld.com/sendsms.aspx?phone=13706794299&content='+contents+'&sc=hengdian86547211jjh'
	#print url
	js = json.load(urllib2.urlopen(url))
	if js['status'] != 0:
		print 'sms send fail'
	else:
		log_send_record('SMS',contents)

def send_mail(to_list,sub,content): 
	if not can_send('EMAIL'):
		return;
	me="hengdianworld1"+"<"+mail_user+"@"+mail_postfix+">"  
	msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
	msg['Subject'] = sub  
	msg['From'] = me  
	msg['To'] = ";".join(to_list)  
	try:  
		server = smtplib.SMTP()  
		server.connect(mail_host)  
		server.login(mail_user,mail_pass)  
		server.sendmail(me, to_list, msg.as_string())
		server.close()
		log_send_record('EMAIL',content)
		return True  
	except Exception, e:  
		print str(e)  
		return False  
		
def send_report(to_list,sub,content):  
	send_mail(to_list,sub,content)
	#send_sms(content)

has_exception = False
begin_time = datetime.datetime.now()
conn = httplib.HTTPConnection(HOST)
try:
	conn.request("GET", "/")
	res = conn.getresponse()
except Exception, e:
	print e
	has_exception = True
	
end_time = datetime.datetime.now()
second = (end_time - begin_time).total_seconds()
if not has_exception:
	print "status code: "+ str(res.status)
print "get response time is "+str(second)+"s"

has_error = False
if has_exception or (res.status != 200):
	#服务器有异常
	sms_contents = WEB_NAME+'('+HOST+')无法服务'
	sub = WEB_NAME+'无法服务'
	has_error = True
elif second > TIME_OUT_SECOND:
	#服务器有性能问题
	sms_contents = WEB_NAME+'('+HOST+')性能有问题，响应时间>'+str(TIME_OUT_SECOND)+'s'
	sub = WEB_NAME+'性能有问题'
	has_error = True

if has_error:
	log_problem(sms_contents)
	send_report(mailto_list,sub,sms_contents)
	




	
