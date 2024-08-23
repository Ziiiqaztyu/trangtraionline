from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Cho phép tất cả các nguồn gốc

# Khởi tạo cơ sở dữ liệu SQLite
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,   -- ID là khóa chính và duy nhất
            name TEXT,
            weight REAL
        )
    ''')
    conn.close()

# Tạo ID khách hàng duy nhất
def generate_customer_id():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
    last_id = cursor.fetchone()
    conn.close()
    
    if not last_id:
        return 'AA001'
    
    last_id = last_id[0]
    prefix = last_id[:2]
    num = int(last_id[2:]) + 1
    new_id = f"{prefix}{num:03}"
    
    if new_id > 'BB999':
        raise ValueError("ID khách hàng đã đạt giới hạn tối đa.")
    
    return new_id

# Route để xử lý việc lưu thông tin
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    weight = request.form['weight']
    
    new_id = generate_customer_id()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (id, name, weight) VALUES (?, ?, ?)", (new_id, name, weight))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        return jsonify(message="Lỗi khi lưu dữ liệu: " + str(e))
    
    conn.close()

    return jsonify(message="Dữ liệu đã được lưu thành công.", id=new_id)

# Route để xử lý việc tìm kiếm thông tin
@app.route('/search', methods=['GET'])
def search():
    search_name = request.args.get('search_name') #gg

    conn = sqlite3.connect('database.db')
    cursor = conn.execute("SELECT * FROM users WHERE name=? OR id=?", (search_name, search_name))
    data = cursor.fetchone()
    conn.close()

    if data:
        return jsonify(id=data[0], name=data[1], weight=data[2])
    else:
        return jsonify(error="Không tìm thấy thông tin.")

if __name__ == '__main__':
    init_sqlite_db()  
    app.run(debug=True)
