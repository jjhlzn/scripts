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
            (select top 1 1 from iccard14.dbo.v_tbdTravelOkPro b inner join iccard14.dbo.tbdProduction c on b.CurID = c.CurID where a.sellid = b.SellID and c.sTicketType = '单票') as is_signleticket,
            (select top 1 1 from iccard14.dbo.v_tbdTravelOkPro b inner join iccard14.dbo.tbdProduction c on b.CurID = c.CurID where a.sellid = b.SellID and c.sTicketType = '联票') as is_unionticket,
            (select top 1 1 from iccard14.dbo.v_tbdTravelOkPro b inner join iccard14.dbo.tbdProduction c on b.CurID = c.CurID where a.sellid = b.SellID and c.sTicketType not in ('联票', '单票')) as is_other,
            (select COUNT(distinct b.CurID) from iccard14.dbo.v_tbdTravelOkPro b left join iccard14.dbo.tbdProduction c on b.CurID = c.CurID where a.sellid = b.SellID) as pro_count
            from iccard14.dbo.v_tbdTravelOk a where  Flag in (1) and
            exists(select * from iccard14.dbo.tbdGroupType b where a.DGroupType = b.DName and a.DGroupTypeAssort = b.sType and DGroupRoomType = '网络用房')
            and not exists(select * from iccard14.dbo.v_tbdTravelOkHotel b where a.SellID = b.SellID)
            order by DComeDate"""
    rows = get_rows_from_orders(sql)
    datasets = defaultdict(list)
    for row in rows:
        datasets[row['DComeDate']].append(row)

    keys = datasets.keys()
    keys.sort()
    for key in keys:
        orders = datasets[key]
        stat_data = {'single': [0,0,0], 'union':[0,0,0], 'combine':[0,0,0], 'other':[0,0,0]}
        for

ticketorder_type_dailyreport()
