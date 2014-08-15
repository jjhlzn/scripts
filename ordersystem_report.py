#coding:UTF-8
import _mssql 

server = '127.0.0.1'
user = 'sa'
password = '123456'

def get_connection():
	conn = _mssql.connect(server=server, user=user, password=password, database='hdbusiness', charset="utf8")
	return conn
	
def get_one_row_from_order(sql, parameter):
	data = {}
	conn = get_connection()
	row = conn.execute_row(sql, parameter)
	if row is not None:
		data = row
	conn.close()
	return data
	
def get_value_from_order(sql, parameter):
	row = get_one_row_from_order(sql, parameter)
	return row[0]
	
def get_rows_from_orders(sql, parameter):
	data = []
	conn = get_connection()
	conn.execute_query(sql, parameter)
	for row in conn:
		data.append(row)
	conn.close()
	return data
	
def daily_report(date):
	sql = "select COUNT(*) from  hdbusiness.dbo.tbdVisitorOk where DDate = %s and substring(sellid,0,2) = 'V'"
	total_order_count = get_value_from_order(sql, date)
	print "total_order_count = %d" % total_order_count
	sql = "select COUNT(*) from  hdbusiness.dbo.tbdVisitorOk where DDate = %s and substring(sellid,0,2) = 'V' and Flag in (0, 1)"
	success_order_count = get_value_from_order(sql, date)
	sql = "select COUNT(*) from  hdbusiness.dbo.tbdVisitorOk where DDate = %s and substring(sellid,0,2) = 'V' and Flag in (0, 1) and device = 1"
	mobile_order_count = get_value_from_order(sql, date)
	sql = "select sType, COUNT(*) as order_count, SUM(DDjNumber) as people_num, SUM(DAmount) as total_money \
		   from  hdbusiness.dbo.tbdVisitorOk where DDate = %s and substring(sellid,0,2) = 'V' and Flag in (0, 1) group by sType"
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
	sql = "select COUNT(*) from  hdbusiness.dbo.tbdVisitorOk a where DDate = %s and substring(sellid,0,2) = 'V' \
	      and Flag in (0, 1) and sType = '套餐' and exists (select * from hdbusiness.dbo.tbdVisitorOkHotel b where b.DHotelNight >= 2 and b.SellID = a.SellID)"
	package_order_hotelnights_morethan2_count = get_value_from_order(sql, date)
	sql = "select COUNT(*) from  hdbusiness.dbo.tbdVisitorOk where DDate = %s and DAdvanceAmount = 0 and \
         substring(sellid,0,2) = 'V' and Flag in (0, 1)"
	paywhencome_order_count = get_value_from_order(sql, date)
   
	sql = "select COUNT(*) from  hdbusiness.dbo.tbdVisitorOk where DDate = %s and substring(sellid,0,2) = 'V' \
          and Flag in (0, 1) and DMemo like '%订单来自接口同步%'"
	interface_order_count = get_value_from_order(sql, date)
	
   
   
   

daily_report('2014-7-1')
