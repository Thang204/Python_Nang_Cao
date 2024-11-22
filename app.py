from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import psycopg2
from psycopg2 import Error
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Cấu hình database
DB_CONFIG = {
    "database": "dbtest",
    "user": "postgres",
    "password": "123456",
    "host": "localhost",
    "port": "5432"
}

# Decorator kiểm tra đăng nhập
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Kết nối database
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Tạo bảng cafe nếu chưa tồn tại
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cafe (
                id SERIAL PRIMARY KEY,
                ten_cafe VARCHAR(100),
                xuat_xu VARCHAR(100),
                don_gia DECIMAL(10,2),
                so_luong INTEGER
            )
        """)
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == "admin" and password == "admin":
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    return render_template('login.html', error="Sai tài khoản hoặc mật khẩu!")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# API endpoints
@app.route('/api/cafe', methods=['GET'])
@login_required
def get_cafe():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM cafe")
        cafe_items = cursor.fetchall()
        return jsonify([{
            "id": row[0],
            "ten_cafe": row[1],
            "xuat_xu": row[2],
            "don_gia": float(row[3]),
            "so_luong": row[4]
        } for row in cafe_items])
    finally:
        cursor.close()
        conn.close()

@app.route('/api/cafe', methods=['POST'])
@login_required
def add_cafe():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO cafe (ten_cafe, xuat_xu, don_gia, so_luong) VALUES (%s, %s, %s, %s)",
            (data['ten_cafe'], data['xuat_xu'], data['don_gia'], data['so_luong'])
        )
        conn.commit()
        return jsonify({"message": "Thêm cafe thành công"})
    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/api/cafe/<int:id>', methods=['PUT'])
@login_required
def update_cafe(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE cafe SET ten_cafe = %s, xuat_xu = %s, don_gia = %s, so_luong = %s WHERE id = %s",
            (data['ten_cafe'], data['xuat_xu'], data['don_gia'], data['so_luong'], id)
        )
        conn.commit()
        return jsonify({"message": "Cập nhật cafe thành công"})
    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/api/cafe/<int:id>', methods=['DELETE'])
@login_required
def delete_cafe(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM cafe WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"message": "Xóa cafe thành công"})
    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    init_db()  # Khởi tạo database khi chạy app
    app.run(debug=True)