# 导入模块
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import math
import yaml
import time
from datetime import datetime
import requests
from tqdm import tqdm
import requests

# 获取公网IP地址
def get_public_ip():
    try:
        response = requests.get('http://httpbin.org/ip')
        if response.status_code == 200:
            data = response.json()
            return data['origin']
    except Exception as e:
        print(f"发生错误: {e}")
    return None

def check_ip_location(ip):
    try:
        response = requests.get(f'http://ipinfo.io/{ip}/json')
        if response.status_code == 200:
            data = response.json()
            country = data.get('country', '')
            return country
    except Exception as e:
        print(f"发生错误: {e}")
    return None

# 获取公网IP地址和IP地址所在国家
public_ip = get_public_ip()
if public_ip:
    print(f"您的公网IP地址是: {public_ip}")
    country = check_ip_location(public_ip)
    if country:
        if country == 'CN':
            print("您的IP地址位于中国。")
            base_url = 'https://github.moeyy.xyz/https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master'  # 加速服务器URL
        else:
            print("您的IP地址位于中国以外。")
            base_url = 'https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master'  # GitHub URL
    else:
        print("无法确定IP地址的位置，默认为中国。")
        base_url = 'https://github.moeyy.xyz/https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master'  # 默认为中国

else:
    print("无法获取公网IP地址，默认为中国。")
    base_url = 'https://github.moeyy.xyz/https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master'  # 默认为中国

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

# 下载文件并显示下载进度、文件大小和下载时间
def download_file(url, file_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    start_time = time.time()

    progress = tqdm(total=total_size, unit='B', unit_scale=True, desc=f'Downloading', bar_format='{l_bar}{bar}', colour='red')
    with open(file_path, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            progress.update(len(data))
            file.write(data)
    progress.close()

    end_time = time.time()
    download_time = end_time - start_time
    file_size = os.path.getsize(file_path)
    
    print(f"Download complete: {file_path.split('/')[-1]}")
    print(f"文件大小/File size: {file_size} bytes")
    print(f"下载时间/Download time: {download_time:.2f} seconds")

# 加载static文件夹中的文件
static_files = {
    'index.js': f'{base_url}/static/index.js',
    'index.css': f'{base_url}/static/index.css',
    'favicon.ico': f'{base_url}/static/favicon.ico',
    'bootstrap.min.css': f'{base_url}/static/bootstrap.min.css',
    'bootstrap.bundle.min.js': f'{base_url}/static/bootstrap.bundle.min.js'
}

for file_name, url in static_files.items():
    file_path = os.path.join(static_folder_path, file_name)
    if not os.path.exists(file_path):
        download_file(url, file_path)

# 加载templates文件夹中的文件
templates_files = {
    'login.html': f'{base_url}/templates/login.html',
    'index.html': f'{base_url}/templates/index.html',
    'control.html': f'{base_url}/templates/control.html',
    '404.html': f'{base_url}/templates/404.html'
}

for file_name, url in templates_files.items():
    file_path = os.path.join(templates_folder_path, file_name)
    if not os.path.exists(file_path):
        download_file(url, file_path)
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

app.secret_key = key

login_manager = LoginManager()
login_manager.init_app(app)

# 模拟用户数据库
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# 未经授权处理函数
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

# 用户认证
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# 登录页面
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
            return '错误: 您输入的用户名或密码无效'
    
    return render_template('login.html')

# 注销功能
@app.route('/logout', endpoint='logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 管理页面
@app.route('/admin', endpoint='admin')
@login_required
def admin():
    return render_template('control.html')
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