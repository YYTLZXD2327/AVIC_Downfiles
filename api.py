import tkinter as tk
from tkinter import filedialog
import requests
import os
import yaml
import json

config_path = 'config.yml'
if not os.path.exists(config_path):
    config = {
        'URL': '127.0.0.1:5000',
        'password': 'password',
    }
    with open(config_path, 'w') as f:
        yaml.dump(config, f)

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
url = config['URL']
password = config['password']
protocol = 'http://'  # 默认协议为http

if 'protocol' in config:
    protocol = config['protocol'] + '://'

def delete_file():
    global url, password, protocol
    url = config['URL']  
    if not url.startswith('http://') and not url.startswith('https://'):
        url = protocol + url
    file_to_delete = file_to_delete_entry.get()
    endpoint = f'delete/{file_to_delete}'
    response = requests.post(f'{url}/{endpoint}', data={'password': password})
    
    if response.status_code == 200:
        result_text.insert(tk.END, "文件删除成功\n")
    else:
        result_text.insert(tk.END, f"删除文件失败，状态码: {response.status_code}\n")

def upload_file():
    global url, password, protocol
    url = config['URL']  
    if not url.startswith('http://') and not url.startswith('https://'):
        url = protocol + url
    file_path = filedialog.askopenfilename()
    files = {'file': open(file_path, 'rb')}
    response = requests.post(f'{url}/upload', files=files, data={'password': password})
    
    if response.status_code == 200:
        result_text.insert(tk.END, "文件上传成功\n")
    else:
        result_text.insert(tk.END, f"上传文件失败，状态码: {response.status_code}\n")

def get_file_list(file_list_text):
    global url, password, protocol
    url = config['URL']  
    if not url.startswith('http://') and not url.startswith('https://'):
        url = protocol + url
    response = requests.post(f'{url}/api/files', data={'password': password})
    
    if response.status_code == 200:
        file_list_text.delete('1.0', tk.END)  
        file_list_text.insert(tk.END, "当前文件列表:\n")
        
        try:
            data = json.loads(response.content)
            for item in data:
                file_list_text.insert(tk.END, f"文件名: {item['文件名']}\n")
                file_list_text.insert(tk.END, f"文件大小: {item['文件大小']}\n")
                file_list_text.insert(tk.END, f"最后修改时间: {item['最后修改时间']}\n\n")
        except json.JSONDecodeError:
            file_list_text.insert(tk.END, "无法解析JSON响应内容")
    else:
        file_list_text.delete('1.0', tk.END)  
        file_list_text.insert(tk.END, f"获取文件列表失败，状态码: {response.status_code}")

# 创建GUI窗口
root = tk.Tk()
root.title("文件管理应用")
root.geometry("800x600")
root.configure(bg='#f0f0f0')

# 添加文件名输入框
file_to_delete_label = tk.Label(root, text="要删除的文件名:", bg='#f0f0f0', font=("Arial", 12))
file_to_delete_label.pack()

file_to_delete_entry = tk.Entry(root, width=60, font=("Arial", 12))
file_to_delete_entry.pack(pady=10)

delete_file_button = tk.Button(root, text="删除文件", command=delete_file, bg='#FF5733', fg='white', font=("Arial", 12))
delete_file_button.pack(pady=10)

upload_button = tk.Button(root, text="上传文件", command=upload_file, bg='#33FF57', fg='white', font=("Arial", 12))
upload_button.pack(pady=10)

# 添加文本框来显示操作结果
result_text = tk.Text(root, height=5, width=100)
result_text.pack()

# 添加按钮来触发获取文件列表操作
get_file_list_button = tk.Button(root, text="获取文件列表", command=lambda: get_file_list(file_list_text), font=("Arial", 12))
get_file_list_button.pack()

# 创建文本框用于显示文件列表
file_list_text = tk.Text(root, height=20, width=100)
file_list_text.pack()

root.mainloop()