import _mssql

__server = '127.0.0.1'
__user = 'sa'
__password = '123456'

def get_connection():
    conn = _mssql.connect(server=__server, user=__user, password=__password, database='hdbusiness', charset="utf8")
    return conn

def get_one_row_from_order(sql, params):
    data = {}
    conn = get_connection()

    row = conn.execute_row(sql, params)
    if row is not None:
        data = row
    conn.close()
    return data

def get_value_from_order(sql, params):
    row = get_one_row_from_order(sql, params)
    return row[0]

def get_rows_from_orders(sql, params=[]):
    data = []
    conn = get_connection()
    conn.execute_query(sql, params)
    for row in conn:
        data.append(row)
    conn.close()
    return data