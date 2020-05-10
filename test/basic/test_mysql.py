import pymysql

# 连接database
conn = pymysql.connect(
    host="157.245.218.27",
    user="root",
    password="mytaraxa2019",
    database="ontherecord",
    charset="utf8")
print(conn)
