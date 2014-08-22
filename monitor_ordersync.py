# coding:UTF-8
import httplib
import datetime
import time
import urllib2
import json

import smtplib
from email.mime.text import MIMEText

import sys

HOST = "e.hengdianworld.com"

mailto_list = ['jinjunhang@hotmail.com']
mail_host = "smtp.163.com"  #设置服务器
mail_user = "hengdianworld1"  #用户名
mail_pass = "abc123"  #口令
mail_postfix = "163.com"  #发件箱的后缀


def send_mail(to_list, sub, content):
    me = "hengdianworld1" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain', _charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


def get_unsync_order_count():
    conn = httplib.HTTPConnection(HOST)
    try:
        conn.request("GET", "/Interface/service.aspx?action=GetUnsyncOrders&data={}")
        res = conn.getresponse()
        data = res.read()
        json_obj = json.loads(data)
        print "sellids = %s" % json_obj['SellIds']
        return len(json_obj['SellIds'])
    except Exception, e:
        print e
        return 0


def sync_orders():
    conn = httplib.HTTPConnection(HOST)
    try:
        conn.request("GET", "/Interface/service.aspx?action=SyncOrders&data={}")
        res = conn.getresponse()
        data = res.read()
        print data
    except Exception, e:
        print e


def main():
    conn = httplib.HTTPConnection(HOST)
    try:
        count = get_unsync_order_count()
        if count == 0:
            print "all orders have synced"
        else:
            print "there is %d order not synced" % count
            sync_orders()
            count = get_unsync_order_count()
            if count > 0:
                send_mail(['jinjunhang@hotmail.com'], u'预定系统：同步订单失败！', u"有%d个订单同步失败！" % count)
    except Exception, e:
        print e
        return


main()




	
