import subprocess
import requests
import os
import time
import threading

# 获取公网IP地址和IP地址所在国家
def get_public_ip():
    try:
        response = requests.get('http://httpbin.org/ip')
        if response.status_code == 200:
            data = response.json()
            return data.get('origin')
    except Exception as e:
        print(f"发生错误: {e}")
    return None

def check_ip_location(ip):
    try:
        response = requests.get(f'http://ipinfo.io/{ip}/json')
        if response.status_code == 200:
            data = response.json()
            return data.get('country', '')
    except Exception as e:
        print(f"发生错误: {e}")
    return None

# 获取版本文件内容
def get_config_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"无法获取配置文件。状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"发生错误: {e}")

def input_with_timeout(prompt, timeout):
    print(prompt, end='', flush=True)
    user_input = [None]

    def get_input():
        user_input[0] = input()

    input_thread = threading.Thread(target=get_input)
    input_thread.start()
    input_thread.join(timeout)

    if input_thread.is_alive():
        print('超时，自动选择"y"')
        user_input[0] = 'y'  # 设置默认值为 'y'

    return user_input[0].lower() if user_input[0] else 'y'  # 返回小写的用户输入，如果没有输入则返回默认值 'y'

# 确保 'templates/' 目录存在
if not os.path.exists('templates'):
    os.makedirs('templates')

# 确保 'static/' 目录存在
if not os.path.exists('static'):
    os.makedirs('static')

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

config_url = f'{base_url}/version.txt'
config_data = get_config_from_url(config_url)

# 获取version.txt中的内容
version_content = ""
if os.path.exists("version.txt"):
    with open("version.txt", "r") as file:
        version_content = file.read()

# 判断是否需要更新文件
if config_data and (not os.path.exists("version.txt") or config_data != version_content):
    print("当前版本为旧版本或版本文件不存在。")
    
    # 提示用户是否更新
    update_choice = input_with_timeout("有新版本，是否更新版本？(Y/N): ", 3)
    if update_choice not in ['y', 'n']:
        update_choice = 'y'  # 默认选择更新

    if update_choice == 'y':
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
        print('static目录下的文件已处理.')

        # 处理 'templates/' 目录下的文件
        directory_path = 'templates/'
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path) and file not in ['favicon.ico', 'config.yml']:
                os.remove(file_path)
                print(f"文件 '{file_path}' 已成功删除.")
        print('templates目录下的文件已处理.')

        url = f'{base_url}/version.txt'
        response = requests.get(url)
        if response.status_code == 200:
            with open("version.txt", "wb") as file:
                file.write(response.content)
            print("version.txt 文件下载成功.")
        else:
            print("无法下载version.txt文件.")

        url = f'{base_url}/app.py'
        response = requests.get(url)
        if response.status_code == 200:
            with open("app.py", "wb") as file:
                file.write(response.content)
            print("app.py 文件下载成功.")
        else:
            print("无法下载app.py文件.")
        
        print("版本已更新。")
        time.sleep(1)
        subprocess.run(["python", "app.py"])
    else:
        print("用户选择不更新版本，将直接运行app.py.")
        subprocess.run(["python", "app.py"])
else:
    if not os.path.exists("version.txt"):
        print("version.txt文件不存在，视为与旧版本。")
    else:
        print("本版本为最新版本，将直接运行app.py.")
    subprocess.run(["python", "app.py"])
