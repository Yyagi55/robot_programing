#!/usr/bin/env python3
from flask import *
import pymysql
import matplotlib.pyplot
import matplotlib.dates

connector = pymysql.connect(host='localhost',db='webapp_db',user='root',passwd='halfmoon',\
                            charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor);
cursor = connector.cursor()

app = Flask(__name__)

sql = "show tables";
a = cursor.execute(sql)
if a == 0:
  sql = "create table object (id int,name varchar(100),quantity smallint unsigned, dt date,state int)";
  cursor.execute(sql)
  connector.commit()
  sql = "insert into object (id, name, quantity, dt, state) values (%s, %s, %s, %s, 0)";
  cursor.execute(sql,(0,'dummy',0,'2020-01-01'))
  connector.commit()

# title_page
@app.route("/", methods=["GET", "POST"])
def title_page():
  return render_template('title_page.html')

# main_page
@app.route("/main", methods=["GET", "POST"])
def main_page():
  return render_template('main_page.html')

# 操作選択
@app.route("/inventory_control", methods=["GET", "POST"])
def inventory_control_page():
  return render_template('inventory_control_page.html')

# 新規登録_情報入力
@app.route("/new_registration", methods=["GET", "POST"])
def new_registration_page():
  return render_template('new_registration_page.html')

# 新規登録_処理確認
@app.route("/new_registration_confirmation", methods=["GET", "POST"])
def new_registration_confirmation_page():
  name = request.form.get('name')
  quantity = request.form.get('quantity')
  dt = request.form.get('date')
  sql = "select id from object";
  id = cursor.execute(sql)
  sql = "insert into object (id, name, quantity, dt, state) values (%s, %s, %s, %s, 1)";
  cursor.execute(sql,(id,name,quantity,dt))
  sql = "create table " + name + " (quantity smallint unsigned, dt date)";
  cursor.execute(sql)
  sql = "insert into " + name + " (quantity, dt) values (%s, %s)";
  cursor.execute(sql,(quantity,dt))
  connector.commit()
  return render_template('new_registration_confirmation_page.html',name=name,quantity=quantity,date=dt)

# 入庫_情報入力
@app.route("/add", methods=["GET", "POST"])
def add_page():
  return render_template('add_page.html')

# 入庫_処理確認
@app.route("/add_confirmation", methods=["GET", "POST"])
def add_confirmation_page():
  name = request.form.get('name')
  quantity = request.form.get('quantity')
  dt = request.form.get('date')
  sql = "select * from object where name=%s";
  cursor.execute(sql,(name))
  result = cursor.fetchall()
  data = result[0]
  n = int(data['quantity']) + int(quantity)
  sql = "update object set quantity=%s,dt=%s where name=%s";
  cursor.execute(sql,(n,dt,name))
  sql = "insert into " + name + " (quantity, dt) values (%s, %s)";
  cursor.execute(sql,(n,dt))
  connector.commit()
  return render_template('add_confirmation_page.html',name=name,quantity=quantity,date=dt)

# 出庫_情報入力
@app.route("/consumption", methods=["GET", "POST"])
def consumption_page():
  return render_template('consumption_page.html')

# 出庫_処理確認
@app.route("/consumption_confirmation", methods=["GET", "POST"])
def consumption_confirmation_page():
  name = request.form.get('name')
  quantity = request.form.get('quantity')
  dt = request.form.get('date')
  sql = "select * from object where name=%s";
  cursor.execute(sql,(name))
  result = cursor.fetchall()
  data = result[0]
  n = int(data['quantity']) - int(quantity)
  sql = "update object set quantity=%s,dt=%s where name=%s";
  cursor.execute(sql,(n,dt,name))
  sql = "insert into " + name + " (quantity, dt) values (%s, %s)";
  cursor.execute(sql,(n,dt))
  connector.commit()
  return render_template('consumption_confirmation_page.html',name=name,quantity=quantity,date=dt)

# 削除_情報入力
@app.route("/delete", methods=["GET", "POST"])
def delete_page():
  return render_template('delete_page.html')

# 削除_処理確認
@app.route("/delete_confirmation", methods=["GET", "POST"])
def delete_confirmation_page():
  name = request.form.get('name')
  sql = 'update object set state=0 where name=%s';
  cursor.execute(sql,(name))
  connector.commit()
  return render_template('delete_confirmation_page.html',name=name)

# グラフ化ルート
@app.route("/graph_select", methods=["GET", "POST"])
def graph_select_page():
  return render_template('graph_select_page.html')

@app.route("/total_stoc", methods=["GET", "POST"])
def total_stoc_page():
  sql = "select name,quantity from object where id > 0";
  cursor.execute(sql)
  result = cursor.fetchall()
  left = list(range(1,len(result)+1))
  height = []
  label = []
  for i in range(len(result)):
    height.append(result[i]['quantity'])
    label.append(result[i]['name'])
  matplotlib.pyplot.rcParams["font.size"] = 18
  matplotlib.pyplot.tight_layout()
  matplotlib.pyplot.bar(left,height,width=0.5,color='b',tick_label=label)
  matplotlib.pyplot.savefig('static/total_stoc.png')
  return render_template('total_stoc_page.html')

@app.route("/inventory_change", methods=["GET", "POST"])
def inventory_change_page():
  return render_template('inventory_change_page.html')

@app.route("/inventory_change_confirmation", methods=["GET", "POST"])
def inventory_change_confirmation_page():
  name = request.form.get('name')
  sql = "select * from " + name;
  cursor.execute(sql)
  result = cursor.fetchall()
  x = []
  y = []
  for i in range(len(result)):
    y.append(result[i]['quantity'])
    x.append(result[i]['dt'])
  fig = matplotlib.pyplot.figure()
  ax = fig.add_subplot(1,1,1)
  fig.suptitle(name)
  matplotlib.pyplot.rcParams["font.size"] = 18
  matplotlib.pyplot.tight_layout()
  ax.plot(x,y,color='b')
  ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%y\n%m/%d'))
  matplotlib.pyplot.savefig('static/inventory_change.png')
  return render_template('inventory_change_confirmation_page.html')

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=8080)
