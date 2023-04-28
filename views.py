from flask import Flask, redirect, render_template, request, url_for  
from flask_mysqldb import MySQL  
from datetime import datetime
from datetime import date


app = Flask(__name__)   
app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = '123456789'  
app.config['MYSQL_DB'] = 'myapp'

mysql = MySQL(app)   

@app.route('/', methods=['GET', 'POST'])   
def index():
    if request.method == 'POST':         
        #date = request.form['date']  
        #names = request.form['names'].split() 

        date = request.form['date'].strip() # 去除日期首尾空格
        date = date.replace(' ', '')       # 替换日期中的空格 

        names = request.form['names']
        names = names.strip()             # 去除名称字段首尾空格 
        names = names.replace(' ', '')    # 替换名称字段中的空格
        names = names.split()             # 拆分名称字段为列表            

        cur = mysql.connection.cursor()
        for name in names:    
            cur.execute("INSERT INTO records (date, name) VALUES (%s, %s)", (date, name))
        mysql.connection.commit()
        cur.close()  
        return redirect('/')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM records")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', data=data)  

@app.route('/clear_all', methods=['POST'])
def clear_all():
  cur = mysql.connection.cursor()
  cur.execute("DELETE FROM records") # 删除records表中所有记录
  mysql.connection.commit()
  cur.close()
  return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM records WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
         name = request.form['name']
         cur = mysql.connection.cursor()
         cur.execute("UPDATE records SET name=%s WHERE id=%s", (name, id))  
         mysql.connection.commit()
         cur.close()
         return redirect('/')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM records WHERE id=%s", (id,))
    data = cur.fetchall()
    cur.close() 
    return render_template('edit.html', data=data)
        
@app.route('/stats')
def db_stats():
    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM records")
    names = cur.fetchall()
    set_names = set(names)
    name_counts = {}
    for name in set_names:
        name_counts[name] = names.count(name)
    sorted_counts = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)
    cur.close()  

    return render_template('stats.html', **{
        'sorted_counts': sorted_counts  
    })

@app.route('/last')
def db_last():
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, MAX(date) FROM records GROUP BY name")
    data = cur.fetchall()
    today = date.today()
    results = []
    for name, max_date in data:
        delta = today - max_date
        results.append({'name': name, 'max_date': max_date, 'days': delta.days})
    cur.close()  

    # 实现排序
    results.sort(key=lambda x: x['days'], reverse=True)  

    return render_template('last.html', **{
        'results': results
    }) 

if __name__ == '__main__':      
    app.run(debug=True) 