# coding:UTF-8
import _mssql
import time
from  database import *

COME_DATE = 'ComeDate'
ORDER_DATE = 'OrderDate'

def daily_report(datetype, dbname, start_date, end_date):
    dateField = ''
    table = ''
    if datetype == ORDER_DATE:
        dateField = 'DDate'
        table = 't_ticketsystem_network_dailyreport_orderdate'
    else:
        dateField = 'DComeDate'
        table = 't_ticketsystem_network_dailyreport_comedate'

    sql = """select %s [date], COUNT(*) order_number, SUM(DDjNumber) order_people_number, SUM(DAmount) order_money
            from %s.dbo.v_tbdTravelOk a
            where
            Flag in (0,1) and %s >= '%s' and %s <= '%s' and
            exists(select * from %s.dbo.tbdGroupType b where a.DGroupType = b.DName and a.DGroupTypeAssort = b.sType and DGroupRoomType = '网络用房')
            group by %s order by %s""" % (dateField, dbname, dateField, start_date, dateField, end_date, dbname, dateField, dateField)
    print sql
    rows = get_rows_from_orders(sql)
    for row in rows:
        sql = """insert into report.dbo.%s (date, success_order_number, order_people_number, order_money)
                  values ('%s', %d, %d, %d) """ % \
              (table, str(row['date']), row['order_number'], row['order_people_number'], row['order_money'])
        print sql
        exec_no_query(sql)

def next_day(d):
    return time.localtime(time.mktime(d) + 24 * 60 * 60)


def init(from_date, enddate=time.mktime(time.localtime())):
    d = time.strptime(from_date, '%Y-%m-%d')
    while time.mktime(d) <= enddate:
        print time.strftime('%Y-%m-%d', d)
        #daily_report_using_order_date(time.strftime('%Y-%m-%d', d))
        #daily_report_using_come_date(time.strftime('%Y-%m-%d', d))
        d = next_day(d)

#daily_report(COME_DATE, 'iccard14', '2014-1-1', '2014-9-3')
#daily_report(COME_DATE, 'iccard13', '2013-1-1', '2013-12-31')

daily_report(ORDER_DATE, 'iccard14', '2014-1-1', '2014-9-3')
daily_report(ORDER_DATE, 'iccard13', '2013-1-1', '2013-12-31')
