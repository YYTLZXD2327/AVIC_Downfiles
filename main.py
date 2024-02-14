import subprocess
import requests
import os

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
            base_url = 'https://github.23.yytlzxd.bf/https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master'  # 加速服务器URL
        else:
            print("您的IP地址位于中国以外。")
            base_url = 'https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master'  # GitHub URL
    else:
        print("无法确定IP地址的位置，默认为中国。")
        base_url = 'https://github.23.yytlzxd.bf/https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master'  # 默认为中国

else:
    print("无法获取公网IP地址，默认为中国。")
    base_url = 'https://github.23.yytlzxd.bf/https://raw.githubusercontent.com/YYTLZXD2327/AVIC_Downfiles/master'  # 默认为中国

def get_config_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            config_data = response.text
            return config_data
        else:
            print(f"无法获取配置文件。状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"发生错误: {e}")

# 指定配置文件的URL
config_url = f'{base_url}/version.txt'
config_data = get_config_from_url(config_url)

# 获取version.txt中的内容
with open("version.txt", "r") as file:
    version_content = file.read()

# 判断是否删除app.py文件
if config_data != version_content:
    print("配置文件与version.txt内容不同。")
    if os.path.exists("app.py"):
        os.remove("app.py")
        print("app.py 文件已删除.")
        os.remove("version.txt")
        print("version.txt 文件已删除.")

    # 处理 'static/' 目录下的文件
    directory_path = 'static/'
    files = os.listdir(directory_path)
    for file in files:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path) and file not in ['favicon.ico', 'config.yml']:
            os.remove(file_path)
            print(f"文件 '{file_path}' 已成功删除.")
        else:
            if os.path.isfile(file_path):
                print(f"文件 '{file_path}' 被保留.")
    print("除了 'favicon.ico' 和 'config.yml' 文件之外的 'static/' 目录下的文件已删除.")

    # 处理 'templates/' 目录下的文件
    directory_path = 'templates/'
    files = os.listdir(directory_path)
    for file in files:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path) and file not in ['favicon.ico', 'config.yml']:
            os.remove(file_path)
            print(f"文件 '{file_path}' 已成功删除.")
    print("除了 'favicon.ico' 和 'config.yml' 文件之外的 'templates/' 目录下的文件已删除.")

# 下载并运行app.py文件
url = f'{base_url}/version.txt'
response = requests.get(url)
if response.status_code == 200:
    with open("version.txt", "wb") as file:
        file.write(response.content)
    print("version.txt 文件下载成功.")

url = f'{base_url}/app.py'
response = requests.get(url)
if response.status_code == 200:
    with open("app.py", "wb") as file:
        file.write(response.content)
    print("app.py 文件下载成功.")
    subprocess.run(["python", "app.py"])
else:
    print("无法下载app.py文件.")

# 如果配置文件与version.txt内容相同，则运行app.py文件
if config_data == version_content:
    subprocess.run(["python", "app.py"])

print("批量处理完成.")