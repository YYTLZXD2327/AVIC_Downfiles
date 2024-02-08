from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import math
from datetime import datetime

app = Flask(__name__)

upload_folder = 'downloads'
admin_username = 'admin'
admin_password = 'Yang1027'  # 设置用户密码

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2) if i > 0 else size_bytes
    return "%s %s" % (s, size_name[i])

def get_file_info(file_path):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_size = convert_size(file_size)
    file_last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
    return (file_name, file_size, file_last_modified)

def require_auth(func):
    def wrapper(*args, **kwargs):
        if 'username' in session and session['username'] == admin_username:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

@app.route('/')
@require_auth
def index():
    files_info = []

    for file_name in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, file_name)
        if os.path.isfile(file_path):
            file_info = get_file_info(file_path)
            files_info.append(file_info)

    # 根据文件的修改时间对文件信息进行排序
    sorted_files_info = sorted(files_info, key=lambda x: x[2], reverse=True)

    return render_template('index.html', files_info=sorted_files_info)

# 登录页面
@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            # 登录成功，重定向到管理页面
            return redirect(url_for('admin'))
        else:
            return 'Invalid username or password'
    
    return render_template('login.html')

# 管理页面，需要登录后才能访问
@app.route('/admin')
def admin():
    return render_template('control.html')

@app.route('/upload', methods=['POST'], endpoint='upload_file')
@require_auth
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    file.save(os.path.join(upload_folder, file.filename))
    return redirect(url_for('index'))

@app.route('/delete/<path:filename>', methods=['POST'], endpoint='delete_file')
@require_auth
def delete_file(filename):
    file_path = os.path.join(upload_folder, filename)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        return redirect(url_for('index'))
    else:
        return "File not found", 404

@app.route('/api/files', methods=['GET'], endpoint='files')
@require_auth
def get_files_info():
    files_info = []

    for file_name in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, file_name)
        if os.path.isfile(file_path):
            file_info = get_file_info(file_path)
            files_info.append({
                'file_name': file_info[0],
                'file_size': file_info[1],
                'last_modified': str(file_info[2])
            })

    return jsonify(files_info)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    app.run(host='0.0.0.0', port=5000)
