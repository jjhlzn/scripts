#coding:UTF-8
import httplib
import datetime
import time
import urllib2
import json

import smtplib  
from email.mime.text import MIMEText  

import sys

HOST = "127.0.0.1:8888"

mailto_list=['jinjunhang@hotmail.com'] 
mail_host="smtp.163.com"  #设置服务器
mail_user="hengdianworld1"    #用户名
mail_pass="abc123"   #口令 
mail_postfix="163.com"  #发件箱的后缀

def send_mail(to_list,sub,content): 
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
		return True  
	except Exception, e:  
		print str(e)  
		return False  
		
def get_unsendsms_order_count():
	conn = httplib.HTTPConnection(HOST)
	try:
		conn.request("GET", "/Interface/service.aspx?action=GetUnsendSmsOrderCount&data={}")
		res = conn.getresponse()
		data = res.read()
		json_obj = json.loads(data)
		print "count = %s" % json_obj['Count']
		return json_obj['Count']
	except Exception, e:
		print e
		return 0

def send_digitalticket():
	conn = httplib.HTTPConnection(HOST)
	try:
		conn.request("GET", "/Interface/service.aspx?action=ResendDigitalTicketForRecentlyOrders&data={}")
		res = conn.getresponse()
		data = res.read()
		print data
	except Exception, e:
		print e
	
def main():
	conn = httplib.HTTPConnection(HOST)
	try:
		count = get_unsendsms_order_count()
		if count == 0:
			print "all orders has sent sms"
		else:
			print "there is %d order not send sms" % count
			if count > 10:
				send_mail(['jinjunhang@hotmail.com'], u'预定系统：大量订单电子门票重新发送提醒！', u"有%d个订单的电子票需要重新发送！" % count)
			send_digitalticket()
			count = get_unsendsms_order_count()
			if count > 0:
				send_mail(['jinjunhang@hotmail.com'], u'预定系统：电子门票发送失败！', u"有%d个订单的电子票发送失败！" % count)
	except Exception, e:
		print e
		return

main()




	
