from  database import *

get_connection()

def dailyreport_network_use_orderdate(date):
    """
     select DDate, COUNT(*) as order_number, SUM(DDjNumber) as people_number, SUM(DAmount) as total_money from v_tbdTravelOk a where DDate >= '2013-1-1' and Flag in (1) and
exists(select * from tbdGroupType b where a.DGroupType = b.DName and a.DGroupTypeAssort = b.sType and DGroupRoomType = '网络用房') group by DDate
order by DDate
    :param date:
    :return:
    """