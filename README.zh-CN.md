**v0.1.0** | [🌏English](https://github.com/YYTLZXD2327/AVIC_Downfiles/blob/master/README.md) | 简体中文

# AVIC_Downfiles
> 用 Python语言 搭建简单且稳定的文件下载网页

## 使用方法

### Python

1. 下载本仓库的源代码或使用 `git clone` 指令克隆至本地。
https://github.com/YYTLZXD2327/AVIC_Downfiles/archive/refs/heads/master.zip
2. 解压压缩包（git用户可省略该步骤）并打开源码文件夹。
3. 在文件夹目录下打开终端，执行`pip install flask` `pip install flask_login` `pip install apscheduler` `pip install datetime` `pip install collections` `pip install tqdm`指令。
4. 注意: 一定要记得将`static`中的`config.yml`的默认密码进行修改！！！
5. 继续在终端执行 `python app.py` 指令，启动成功！


### Docker
1. 下载镜像 `docker pull yytlzxd/avic_dwonfiles`
2. 注意: 一定要记得将`static`中的`config.yml`的默认密码进行修改！！！
3. 简单运行 `docker run -d -p 5000:5000 yytlzxd/avic_dwonfiles`

## API
此部分尚未完成，不予展示。