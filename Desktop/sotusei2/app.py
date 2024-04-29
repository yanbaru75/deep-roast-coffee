from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# データベース接続とカーソルの取得
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('management_app.db')
        g.db.row_factory = sqlite3.Row
    return g.db

# データベース初期化
def init_db():
    with app.app_context():
        get_db()

# ダッシュボード
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ユーザー登録ページ
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        manager = request.form['manager']
        entry_date = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            conn.execute("INSERT INTO projects (title, description, manager, entry_date) VALUES (?, ?, ?, ?)",
                         (title, description, manager, entry_date))
            conn.commit()
        return redirect(url_for('list_projects'))
    return render_template('register.html')

# 管理者用案件登録ページ
@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        manager = request.form['manager']
        entry_date = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            conn.execute("INSERT INTO projects (title, description, manager, entry_date) VALUES (?, ?, ?, ?)",
                         (title, description, manager, entry_date))
            conn.commit()
        return redirect(url_for('list_projects'))
    return render_template('admin_register.html')

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with get_db() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=True)
    return render_template('login.html', error=False)

# ログアウト
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# 案件一覧ページ
@app.route('/list_projects')
def list_projects():
    with get_db() as conn:
        projects = conn.execute("SELECT * FROM projects").fetchall()
    return render_template('list_projects.html', projects=projects)

# 進捗入力ページ
@app.route('/input_progress', methods=['GET', 'POST'])
def input_progress():
    if request.method == 'POST':
        project_id = request.form['project_id']
        staff_id = request.form['staff_id']
        status = request.form['status']
        progress_date = request.form['progress_date']
        with get_db() as conn:
            conn.execute("INSERT INTO progress (project_id, staff_id, status, progress_date) VALUES (?, ?, ?, ?)",
                         (project_id, staff_id, status, progress_date))
            conn.commit()
        return redirect(url_for('dashboard'))
    return render_template('input_progress.html')

# 備考入力ページ
@app.route('/input_remarks', methods=['GET', 'POST'])
def input_remarks():
    if request.method == 'POST':
        project_id = request.form['project_id']
        remark = request.form['remark']
        remark_date = request.form['remark_date']
        with get_db() as conn:
            conn.execute("INSERT INTO remarks (project_id, remark, remark_date) VALUES (?, ?, ?)",
                         (project_id, remark, remark_date))
            conn.commit()
        return redirect(url_for('dashboard'))
    return render_template('input_remarks.html')

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
