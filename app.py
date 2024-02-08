from flask import Flask, render_template, send_from_directory, request, jsonify, session, redirect, url_for
import os
import math
from datetime import datetime

app = Flask(__name__)

download_folder = 'download'
app.secret_key = 'YYTLZXD_CZX10325'  # 设置一个密钥用于加密session数据
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

def check_password(password):
    return password == admin_password

@app.route('/')
def index():
    files_info = []

    for file_name in os.listdir(download_folder):
        file_path = os.path.join(download_folder, file_name)
        if os.path.isfile(file_path):
            file_info = get_file_info(file_path)
            files_info.append(file_info)

    # 根据文件的修改时间对文件信息进行排序
    sorted_files_info = sorted(files_info, key=lambda x: x[2], reverse=True)

    return render_template('index.html', files_info=sorted_files_info)

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(download_folder, filename)

@app.route('/login', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == admin_username and password == admin_password:
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return "Invalid credentials"

    return render_template('admin_login.html')

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))

    return render_template('control.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if not session.get('logged_in'):
        return "Unauthorized", 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    file.save(os.path.join(download_folder, file.filename))

    return jsonify({'message': 'File uploaded successfully'})

@app.route('/delete', methods=['POST'])
def delete_file():
    if not session.get('logged_in'):
        return "Unauthorized", 401

    filename = request.form.get('filename')
    file_path = os.path.join(download_folder, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'})
    else:
        return jsonify({'error': 'File not found'})



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    app.run(host='0.0.0.0', port=5000)
