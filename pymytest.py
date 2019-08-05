#/usr/bin/env python3
import pymysql.cursors
connector = pymysql.connect(host='localhost',user='root',password='halfmoon',db='webapp_db',charset='utf8mb4')

cursor = connector.cursor()
sql = "insert into object (id, name, quantity, date) values (1, 'ますい', 5, 20190715)";
cursor.execute(sql)
sql = "insert into object (id, name, quantity, date) values (2, 'へっどぽすと', 1, 20190715)";
cursor.execute(sql)
sql = "insert into object (id, name, quantity, date) values (3, 'こていぐ', 10, 20190715)";
cursor.execute(sql)
connector.commit()
cursor.close()
connector.close()
