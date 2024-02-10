# 导入模块
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import os
import math
import yaml
import time
from datetime import datetime
import requests
from tqdm import tqdm

# 获取当前文件所在目录的绝对路径
current_folder_path = os.path.dirname(os.path.abspath(__file__))

# 定义static文件夹和templates文件夹的绝对路径
static_folder_path = os.path.join(current_folder_path, 'static')
templates_folder_path = os.path.join(current_folder_path, 'templates')

# 创建static文件夹和templates文件夹（如果不存在）
if not os.path.exists(static_folder_path):
    os.makedirs(static_folder_path)

if not os.path.exists(templates_folder_path):
    os.makedirs(templates_folder_path)

# 加载static文件夹中的文件
static_files = {
    'index.js': 'https://github.moeyy.xyz/https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master/static/index.js',
    'index.css': 'https://github.moeyy.xyz/https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master/static/index.css',
    'favicon.ico': 'https://github.moeyy.xyz/https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master/static/favicon.ico',
    'bootstrap.min.css': 'https://github.moeyy.xyz/https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master/static/bootstrap.min.css',
    'bootstrap.bundle.min.js': 'https://github.moeyy.xyz/https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master/static/bootstrap.bundle.min.js'
}

for file_name, url in static_files.items():
    file_path = os.path.join(static_folder_path, file_name)
    if not os.path.exists(file_path):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        progress = tqdm(total=total_size, unit='B', unit_scale=True)
        with open(file_path, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                progress.update(len(data))
                file.write(data)
        progress.close()

# 加载templates文件夹中的文件
templates_files = {
    'login.html': 'https://github.moeyy.xyz/https://github.com/YYTLZXD2327/AVIC_Downfiles/blob/master/templates/login.html',
    'index.html': 'https://github.moeyy.xyz/https://github.com/YYTLZXD2327/AVIC_Downfiles/blob/master/templates/index.html',
    'control.html': 'https://github.moeyy.xyz/https://github.com/YYTLZXD2327/AVIC_Downfiles/blob/master/templates/control.html',
    '404.html': 'https://github.moeyy.xyz/https://github.com/YYTLZXD2327/AVIC_Downfiles/blob/master/templates/404.html'
}

for file_name, url in templates_files.items():
    file_path = os.path.join(templates_folder_path, file_name)
    if not os.path.exists(file_path):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        progress = tqdm(total=total_size, unit='B', unit_scale=True)
        with open(file_path, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                progress.update(len(data))
                file.write(data)
        progress.close()

# 配置文件
config_path = 'static\\config.yml'
if not os.path.exists(config_path):
    config = {
            'Savepath': 'download',
            'password': 'password',
            'username': 'admin',
            'key': '1234567890',
            'host': '0.0.0.0',
            'port': '5000'
            }
    os.makedirs('static', exist_ok=True)
    with open(config_path, 'w') as f:
        yaml.dump(config, f)
time.sleep(1)
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
savepath = config['Savepath']
admin_username = config['username']
admin_password = config['password']
key = config['key']
host = config['host']
port = config['port']
# 保存文件
download_folder = savepath
os.makedirs(download_folder, exist_ok=True)
print('初始化完成，正在启动...')
print('Initialization completed, starting...')

# 开始创建网站
app = Flask(__name__)

# 模拟用户数据库
app.secret_key = key
login_manager = LoginManager()
login_manager.init_app(app)
class User(UserMixin):
    def __init__(self, id):
        self.id = id
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
        auth = request.authorization
        if not auth or not (auth.password == admin_password):
            return '未经授权', 401
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
def index():
    files_info = []

    for file_name in os.listdir(savepath):
        file_path = os.path.join(savepath, file_name)
        if os.path.isfile(file_path):
            file_info = get_file_info(file_path)
            files_info.append(file_info)

    # 根据文件的修改时间对文件信息进行排序
    sorted_files_info = sorted(files_info, key=lambda x: x[2], reverse=True)

    return render_template('index.html', files_info=sorted_files_info)

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    if request.method == 'GET' or request.method == 'POST':
        return send_from_directory(download_folder, filename)
    else:
        return "不允许的方法", 405

# 用户认证
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            # 登录成功
            user = User(1)  # 模拟用户
            login_user(user)
            return redirect(url_for('admin'))
        else:
            return '错误:您输入的用户名或密码无效'
    
    return render_template('login.html')

# 管理界面
@app.route('/admin', endpoint='admin')
@login_required
def admin():
    return render_template('control.html')

# 未登录时的处理
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

# 上传文件
@app.route('/upload', methods=['POST'], endpoint='upload_file')
@require_auth
def upload_file():
    if 'file' not in request.files:
        return "无文件部分", 400

    file = request.files['file']

    if file.filename == '':
        return "没有选定的文件", 400

    file.save(os.path.join(savepath, file.filename))
    return redirect(url_for('index'))


# 删除文件
@app.route('/delete/<path:filename>', methods=['POST'], endpoint='delete_file')
@require_auth
def delete_file(filename):
    file_path = os.path.join(savepath, filename)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        return redirect(url_for('index'))
    else:
        return "未找到文件", 404
# 文件列表
@app.route('/api/files', methods=['POST'], endpoint='files')
def get_files_info():
    files_info = []

    for file_name in os.listdir(savepath):
        file_path = os.path.join(savepath, file_name)
        if os.path.isfile(file_path):
            file_info = get_file_info(file_path)
            files_info.append({
                '文件名': file_info[0],
                '文件大小': file_info[1],
                '最后修改时间': str(file_info[2])
            })


    return jsonify(files_info)

# 404界面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    app.run(host=host, port=port)