#coding:UTF-8
import httplib
import time
import json
from database import *

def _main():
    #获取需要解析的手机号码
    unhandled_phonenumbers = get_unhandled_phonenumbers()
    if unhandled_phonenumbers is None:
        return

    conn = httplib.HTTPConnection('api.showji.com')
    #查询手机号码的信息
    for phonenumber in unhandled_phonenumbers:
        print phonenumber
        phonenumber_info = search_phonenumber_info(conn, phonenumber)
        if phonenumber_info['QueryResult']:
            save_phonenumber_info(phonenumber_info)
        time.sleep(2)

def get_unhandled_phonenumbers():
    sql = """select  * from (
            select distinct SUBSTRING(DTel,0,8) as mobile7 from (
            select distinct SellID, DTel from iccard14.dbo.v_tbdTravelOkCustomer where DTel != ''
            and SellID in (select a.SellID from iccard14.dbo.v_tbdTravelOk a left outer join iccard14.dbo.tbdGroupType b
            on a.DGroupType = b.DName and a.DGroupTypeAssort = b.sType where
            a.DGroupTypeAssort = b.sType and DGroupRoomType = '网络用房')
            union
            select distinct SellID, DTel from iccard13.dbo.v_tbdTravelOkCustomer where DTel != ''
            and SellID in (select a.SellID from iccard13.dbo.v_tbdTravelOk a left outer join iccard13.dbo.tbdGroupType b
            on a.DGroupType = b.DName and a.DGroupTypeAssort = b.sType where
            a.DGroupTypeAssort = b.sType and DGroupRoomType = '网络用房')) as a ) as a where a.mobile7 not in (select phonenumber from report.dbo.t_phonenumber)
            """
    rows = get_rows_from_orders(sql)
    return [row['mobile7'] for row in rows]


def search_phonenumber_info(conn, phonenumber):
    phonenumber_info = {'Mobile': phonenumber, 'QueryResult': False}
    phonenumber = phonenumber.strip()
    #print "len(phonenumber) = " + str(len(phonenumber))
    if len(phonenumber) != 7:
        print "ignore"
        return phonenumber_info
    #通过第三方网站查询手机信息

    #http://api.showji.com/Locating/www.show.ji.c.o.m.aspx?m=1370659&output=json&callback=querycallback&timestamp=1410160943169
    timestamp = str(int(time.time() * 1000))
    #print '/Locating/www.show.ji.c.o.m.aspx?m='+phonenumber+'&output=json&callback=querycallback&timestamp='+timestamp
    conn.request('GET', '/Locating/www.show.ji.c.o.m.aspx?m='+phonenumber+'&output=json&callback=querycallback&timestamp='+timestamp)
    res = conn.getresponse()

    #通过解析请求结果，获得手机号码的信息
    if res.status == 200:
        res_txt = res.read()
        res_json = res_txt[14:-2]
        print res_json
        phonenumber_info = json.loads(res_json)
    else:
        phonenumber_info = {'Mobile': phonenumber, 'QueryResult': False}

    return phonenumber_info

def save_phonenumber_info(info):

    """INSERT INTO report.dbo.t_phonenumber
            (phonenumber,province,city,areacode,corp,card)
            VALUES
            ('%s','%s','%s','%s','%s','%s')""" % (info['Mobile'], info['Province'], info['City'], info['AreaCode'], info['Corp'], info['Card'])
    sql = """INSERT INTO report.dbo.t_phonenumber
            (phonenumber,province,city,areacode,corp,card)
            VALUES
            (%s,%s,%s,%s,%s,%s)"""
    #print sql
    exec_no_query(sql, tuple([info['Mobile'], info['Province'], info['City'], info['AreaCode'], info['Corp'], info['Card']]))

if __name__ == "__main__":
    while(1):
        try:
            _main()
        except Exception:
            pass
    #search_phonenumber_info('1370679')