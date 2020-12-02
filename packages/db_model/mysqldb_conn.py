import pymysql

MYSQL_HOST = 'us-cdbr-east-02.cleardb.com'
MYSQL_CONN = pymysql.connect(
    host=MYSQL_HOST,
    port=3306,
    user='bb2facf27e42f1',
    passwd='a79d859a',
    db='heroku_f88b2724b4668f3',
    charset='utf8'
)

def conn_mysqldb():
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN