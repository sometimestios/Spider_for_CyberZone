import requests
import json
import os
import csv
import threading
from urllib.request import urlretrieve
from urllib.request import quote

import urllib
# 全局取消证书验证
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
csv_path = 'tool_src.csv'

url_root='https://223.129.86.3'
des_root="/home/wang2/data/"

class FetchThread(threading.Thread):
    def __init__(self, threadID, name, url):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.url=url
    def run(self):
        print ("开始线程：" + self.name)
        fetch(self.name, self.url)
        print ("退出线程：" + self.name)
def fetch(threadName,feature):
    print(feature)

def fetch(url_path, des_path):
    def reporthook(a, b, c):
        """
        显示下载进度
        :param a: 已经下载的数据块
        :param b: 数据块的大小
        :param c: 远程文件大小
        :return: None
        """
        print("\rdownloading: %5.1f%%" % (a * b * 100.0 / c), end="")
    # 判断文件是否存在，如果不存在则下载
    if not os.path.isfile(des_path):
        print('Downloading data from %s' % url_path)
        dir_path,file_name=os.path.split(des_path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        try:
            urlretrieve(url_path, des_path, reporthook=reporthook)
        except urllib.error.HTTPError:
            print("Failed downloading{}".format(url_path))
        else:
            print('\nDownload finished!')
    else:
        print('File already exsits!')



def generate_path(feature_lsit):
    global url_root,des_root
    url_path=url_root+quote(feature_lsit[4])
    print(url_path)
    des_path=os.path.join(des_root,feature_lsit[5],feature_lsit[1],feature_lsit[2],feature_lsit[0])
    return url_path,des_path

def write_csv(src_f, csv_path):
    with open(csv_path, 'a', encoding='utf-8-sig',newline='')as csv_f:
        key_feature = ['tool_name', 'system_environment', 'system_type', 'tool_file_size', 'tool_path',
                       'dict_data_name']
        L=len(key_feature)
        writer = csv.writer(csv_f)
        #writer.writerow(key_feature)
        js_file = json.load(src_f)
        for line in js_file:
            write_info = list()
            for i in range(L-1):
                write_info.append(line[key_feature[i]])
            print(line)
            if line['tool__classify']:
                write_info.append(line['tool__classify']['dict_data_name'])
            else:
                write_info.append('其他')
            writer.writerow(write_info)

def scan_json(json_path):
    with open(json_path, 'r', encoding='utf-8')as f:
        write_csv(f, csv_path)


for i in range(1,10):
    json_path = 'json_src0{}.json'.format(i)
    scan_json(json_path)
x=input("是否继续下载？y/n")
if x!='y':
    exit(1)
for i in range(1,10):
    with open(csv_path, 'r', encoding='utf-8-sig')as f:
        reader = csv.reader(f)
        for line in reader:
            url_path, des_path = generate_path(line)
            print(line)
            print(url_path, des_path)
            fetch(url_path, des_path)
            # urlretrieve(url_path,des_path)
