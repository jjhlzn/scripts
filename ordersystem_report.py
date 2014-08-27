# coding:UTF-8
import _mssql
import time
from  database import *

def daily_report_using_order_date(date):
    daily_report('OrderDate', date)

def daily_report_using_come_date(date):
    daily_report('ComeDate', date)

def daily_report(datetype, date):
    dateField = ''
    table = ''
    if datetype == 'OrderDate':
        dateField = 'DDate'
        table = 't_ordersystem_dailyorder'
    else:
        dateField = 'DComeDate'
        table = 't_ordersystem_dailyorder_comedate'
    sql = "select COUNT(*) from  hdbusiness.dbo.view_visitorok where "+dateField+" = %s and substring(sellid,0,2) = 'V'"
    total_order_count = get_value_from_order(sql, date)
    print "total_order_count = %d" % total_order_count
    sql = "select COUNT(*) from  hdbusiness.dbo.view_visitorok where "+dateField+" = %s and substring(sellid,0,2) = 'V' and Flag in (0, 1)"
    success_order_count = get_value_from_order(sql, date)
    sql = "select SUM(DDjNumber) from  hdbusiness.dbo.view_visitorok where "+dateField+" = %s and substring(sellid,0,2) = 'V' and Flag in (0, 1)"
    total_people_count = get_value_from_order(sql, date)
    if total_people_count is None:
        total_people_count = 0
    sql = "select SUM(DAmount) from  hdbusiness.dbo.view_visitorok where "+dateField+" = %s and substring(sellid,0,2) = 'V' and Flag in (0, 1)"
    total_money = get_value_from_order(sql, date)
    if total_money is None:
        total_money = 0
    sql = "select COUNT(*) from  hdbusiness.dbo.view_visitorok where "+dateField+" = %s and substring(sellid,0,2) = 'V' and Flag in (0, 1) and device = 1"
    mobile_order_count = get_value_from_order(sql, date)
    sql = "select sType, COUNT(*) as order_count, SUM(DDjNumber) as people_num, SUM(DAmount) as total_money \
		   from  hdbusiness.dbo.view_visitorok where "+dateField+" = %s and substring(sellid,0,2) = 'V' and Flag in (0, 1) group by sType"
    data = get_rows_from_orders(sql, date)
    ticket_order_count = 0
    ticket_people_num = 0
    ticket_total_money = 0

    hotel_order_count = 0
    hotel_people_num = 0
    hotel_total_money = 0

    package_order_count = 0
    package_people_num = 0
    package_total_money = 0
    for item in data:
        if item['sType'] == u'门票':
            ticket_order_count = item['order_count']
            ticket_people_num = item['people_num']
            ticket_total_money = item['total_money']
        elif item['sType'] == u'酒店':
            hotel_order_count = item['order_count']
            hotel_people_num = item['people_num']
            hotel_total_money = item['total_money']
        elif item['sType'] == u'套餐':
            package_order_count = item['order_count']
            package_people_num = item['people_num']
            package_total_money = item['total_money']
    sql = "select COUNT(*) from  hdbusiness.dbo.view_visitorok a where "+dateField+" = %s and substring(sellid,0,2) = 'V' \
	      and Flag in (0, 1) and sType = '套餐' and exists (select * from hdbusiness.dbo.tbdVisitorOkHotel b where b.DHotelNight >= 2 and b.SellID = a.SellID)"
    package_order_hotelnights_morethan2_count = get_value_from_order(sql, date)
    #print 'package_order_hotelnights_morethan2_count = %d' % package_order_hotelnights_morethan2_count

    sql = "select COUNT(*) from  hdbusiness.dbo.view_visitorok where "+dateField+" = %s and DAdvanceAmount = 0 and \
         substring(sellid,0,2) = 'V' and Flag in (0, 1)"
    paywhencome_order_count = get_value_from_order(sql, date)

    sql = "select COUNT(*) from  hdbusiness.dbo.view_visitorok where "+dateField+" = %s and substring(sellid,0,2) = 'V' \
          and Flag in (0, 1) and DMemo like '%订单来自接口同步%'"
    interface_order_count = get_value_from_order(sql, date)

    sql = "select COUNT(*) from  hdbusiness.dbo.view_visitorok a where "+dateField+" = %s and \
		   substring(sellid,0,2) = 'V' and Flag in (0, 1) and a.SellID in (select SellID from  hdbusiness.dbo.tbdVisitorOkOther b \
		   where b.DBookType in (2, 3))"
    backend_order_count = get_value_from_order(sql, date)

    sql = "select COUNT(*) from  hdbusiness.dbo.view_visitorok a where "+dateField+" = %s and  \
		  substring(sellid,0,2) = 'V' and Flag in (0, 1) and DTravelNo in ('330783018100')"
    officialsite_order_count = get_value_from_order(sql, date)

    sql = "select COUNT(*) from  hdbusiness.dbo.view_visitorok a where "+dateField+" = %s and  \
           substring(sellid,0,2) = 'V' and Flag in (0, 1) and DTravelNo in ( '330783021600', '333100070900','330101068700','3307JH001200')"
    taobao_order_count = get_value_from_order(sql, date)

    sql = "select COUNT(*) from  hdbusiness.dbo.view_visitorok a where "+dateField+" = %s and \
		   substring(sellid,0,2) = 'V' and Flag in (0, 1) and DTravelNo not in ( '330783021600', '333100070900','330101068700','3307JH001200', '330783018100')"
    agent_order_count = get_value_from_order(sql, date)



    sql = "insert into report.dbo."+ table +" (order_date, total_order_count, success_order_count, people_count, total_money, \
		   mobile_order_count, ticket_order_count, hotel_order_count, package_order_count, package_order_hotelnights_morethan2_count, \
		   paywhencome_order_count, interface_order_count, backend_order_count, officialsite_order_count, agent_order_count, taobao_order_count, \
		   favor_order_count, total_favor_money) values ('%s', %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)" % \
          (date, total_order_count, success_order_count, total_people_count, total_money, mobile_order_count,
           ticket_order_count, \
           hotel_order_count, package_order_count, package_order_hotelnights_morethan2_count, paywhencome_order_count,
           interface_order_count, \
           backend_order_count, officialsite_order_count, agent_order_count, taobao_order_count, 0, 0)
    conn = get_connection()
    conn.execute_non_query(sql)
    conn.close()

def next_day(d):
    return time.localtime(time.mktime(d) + 24 * 60 * 60)


def init(from_date, enddate=time.mktime(time.localtime())):
    d = time.strptime(from_date, '%Y-%m-%d')
    while time.mktime(d) <= enddate:
        print time.strftime('%Y-%m-%d', d)
        daily_report_using_order_date(time.strftime('%Y-%m-%d', d))
        daily_report_using_come_date(time.strftime('%Y-%m-%d', d))
        d = next_day(d)

init('2012-1-1','2012-12-31')
