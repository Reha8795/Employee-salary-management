from flask import Flask, render_template, request, redirect, url_for
import sqlite3

conn = sqlite3.connect('esd.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS esd (id INTEGER PRIMARY KEY, fname TEXT, lname TEXT, phone INTEGER, job TEXT, dept TEXT, salary INTEGER, date TEXT, status TEXT)''')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        job = request.form['job']
        dept = request.form['dept']
        salary = request.form['salary']
        date = request.form['date']
        status = request.form['status']
        conn = sqlite3.connect('esd.db')
        c = conn.cursor()
        c.execute("INSERT INTO esd (fname, lname, phone, job, dept, salary, date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (fname, lname, phone, job, dept, salary, date, status))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        current_date = datetime.now().strftime('%Y-%m-%d')
        return render_template('add.html', current_date=current_date)


@app.route('/view')
def view():
    conn = sqlite3.connect('esd.db')
    c = conn.cursor()
    c.execute("SELECT * FROM esd")
    data = c.fetchall()
    conn.close()
    return render_template('view.html', data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        conn = sqlite3.connect('esd.db')
        c = conn.cursor()
        c.execute("SELECT * FROM esd WHERE fname LIKE ?", ('%'+search_term+'%',))
        data = c.fetchall()
        conn.close()
        return render_template('search_result.html', data=data, search_term=search_term)
    else:
        return render_template('search.html')


@app.route('/search_result')    
def search_result():
    search_term = request.args.get('search_term')
    conn = sqlite3.connect('esd.db')
    c = conn.cursor()
    c.execute("SELECT * FROM esd WHERE fname LIKE ?", ('%'+search_term+'%',))
    data = c.fetchall()
    conn.close()
    return render_template('search_result.html', data=data, search_term=search_term)

    
@app.route('/delete', methods=['POST'])
def delete():
    search_term = request.form['search_term']
    id = request.form['id']
    conn = sqlite3.connect('esd.db')
    c = conn.cursor()
    c.execute("DELETE FROM esd WHERE id=?", (id,))
    conn.commit()
    c.execute("SELECT * FROM esd WHERE name LIKE ?", ('%'+search_term+'%',))
    data = c.fetchall()
    conn.close()
    return render_template('view.html', data=data)

@app.route('/delete_form')
def delete_form():
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)
