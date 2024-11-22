from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
app.secret_key = '3824'  

# Kết nối cơ sở dữ liệu
def get_db_connection():
    conn = psycopg2.connect(
        dbname='dbtest',  
        user='postgres',  
        password='382004',  
        host='localhost',  
        port='5432'  
    )
    return conn

# Trang đăng nhập
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'tkien3318' and password == '123': 
            return redirect(url_for('dashboard'))
        else:
            flash('Tên người dùng hoặc mật khẩu không đúng!', 'danger1')
    return render_template('login.html')

# Trang quản lý sinh viên
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM sinhvien')
    students = cur.fetchall()
    conn.close()
    return render_template('dashboard.html', students=students)

# Thêm sinh viên
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        mssv = request.form['mssv']
        hoten = request.form['hoten']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO sinhvien (mssv, hoten) VALUES (%s, %s)', (mssv, hoten))
        conn.commit()
        conn.close()
        flash('Thêm sinh viên thành công!', 'success1')
        return redirect(url_for('dashboard'))
    return render_template('add_students.html')

# Xóa sinh viên
@app.route('/delete/<string:mssv>', methods=['POST'])
def delete_student(mssv):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM sinhvien WHERE mssv = %s', (mssv,))
    conn.commit()
    conn.close()
    flash('Xóa sinh viên thành công!', 'success2')
    return redirect(url_for('dashboard'))

# Tìm kiếm sinh viên
@app.route('/search', methods=['GET', 'POST'])
def search_student():
    student = None
    if request.method == 'POST':
        mssv = request.form['mssv']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM sinhvien WHERE mssv = %s', (mssv,))
        student = cur.fetchone()
        conn.close()
        if not student:
            flash('Không tìm thấy sinh viên với MSSV đã nhập.', 'danger2')
    return render_template('search_students.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)
