# coding: UTF-8

from  database import *
from _collections import defaultdict

def dailyreport_network_use_orderdate(date):
    """
     select DDate, COUNT(*) as order_number, SUM(DDjNumber) as people_number, SUM(DAmount) as total_money from v_tbdTravelOk a where DDate >= '2013-1-1' and Flag in (1) and
exists(select * from tbdGroupType b where a.DGroupType = b.DName and a.DGroupTypeAssort = b.sType and DGroupRoomType = '网络用房') group by DDate
order by DDate
    :param date:
    :return:
    """
    pass

def ticketorder_type_dailyreport():
    sql = """select CONVERT(varchar(100), DComeDate, 23) as comedate, SellID, DDjNumber, DAmount,
            (select top 1 1 from iccard14.dbo.v_tbdTravelOkPro b inner join iccard14.dbo.tbdProduction c on b.CurID = c.CurID where a.sellid = b.SellID and c.sTicketType = '单票') as is_single,
            (select top 1 1 from iccard14.dbo.v_tbdTravelOkPro b inner join iccard14.dbo.tbdProduction c on b.CurID = c.CurID where a.sellid = b.SellID and c.sTicketType = '联票') as is_union,
            (select top 1 1 from iccard14.dbo.v_tbdTravelOkPro b inner join iccard14.dbo.tbdProduction c on b.CurID = c.CurID where a.sellid = b.SellID and c.sTicketType not in ('联票', '单票')) as is_other,
            (select COUNT(distinct b.CurID) from iccard14.dbo.v_tbdTravelOkPro b left join iccard14.dbo.tbdProduction c on b.CurID = c.CurID where a.sellid = b.SellID) as pro_count
            from iccard14.dbo.v_tbdTravelOk a where  Flag in (1) and
            exists(select * from iccard14.dbo.tbdGroupType b where a.DGroupType = b.DName and a.DGroupTypeAssort = b.sType and DGroupRoomType = '网络用房')
            and not exists(select * from iccard14.dbo.v_tbdTravelOkHotel b where a.SellID = b.SellID)
            order by DComeDate"""
    rows = get_rows_from_orders(sql)
    datasets = defaultdict(list)
    for row in rows:
        datasets[row['comedate']].append(row)

    keys = datasets.keys()
    keys.sort()
    for key in keys:
        print key
        orders = datasets[key]
        stat_data = {'single': [0,0,0], 'union':[0,0,0], 'combine':[0,0,0], 'other':[0,0,0]}  #order_count, people_number, total_money
        for order in orders:
            if order['is_union']:
               data = stat_data['union']
            elif order['is_single'] and order['pro_count'] > 1:
                data = stat_data['combine']
            elif order['is_single']:
                data = stat_data['single']
            else:
                data = stat_data['other']
            data[0] += 1
            data[1] += order['DDjNumber']
            data[2] += order['DAmount']
        sql = """INSERT INTO [report].[dbo].[t_ticketsystem_network_ticketorder_type_dailyreport]
                   ([comedate]
                   ,[singleticket_order_count]
                   ,[singleticket_people_number]
                   ,[singleticket_money]
                   ,[combineticket_order_count]
                   ,[combineticket_people_number]
                   ,[combineticket_money]
                   ,[unionticket_order_count]
                   ,[unionticket_people_number]
                   ,[unionticket_money]
                   ,[otherticket_order_count]
                   ,[otherticket_people_number]
                   ,[otherticket_money])
             VALUES
                   ('%s' ,%d ,%d,%d ,%d ,%d ,%d,%d,%d,%d,%d,%d,%d)""" % (key, stat_data['single'][0], stat_data['single'][1], stat_data['single'][2], \
                   stat_data['combine'][0], stat_data['combine'][1], stat_data['combine'][2], stat_data['union'][0], stat_data['union'][1], stat_data['union'][2], \
                   stat_data['other'][0], stat_data['other'][1], stat_data['other'][2])
        print sql
        exec_no_query(sql)

ticketorder_type_dailyreport()
