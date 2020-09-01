import requests
import hashlib
import json
import time
import client_config as cfg
import os
from User import User
from FileInfo import FileInfo
from urllib import parse


class Client:

    def get_cmd_map(self):
        cmd_map = {
            'login': self.login,
            'list': self.query,
            'exit': self.exit,
            'exit_account': self.exit_account,
            'download': self.download,
            # 中英文分界
            '登录': self.login,
            '查询': self.query,
            '退出': self.exit,
            '注销': self.exit_account,
            '下载': self.download,
        }
        return cmd_map

    def login(self, username=None, password=None):
        def judge(txt):
            txt = json.loads(txt)
            if txt['status'] == 0:
                return True
            return False

        # 测试账号
        if username is None and password is None:
            username = 'test'
            password = 'testCyDrive'
        #
        password = password.encode()
        psw_hashed = hashlib.sha256(hashlib.md5(password).digest()).digest()
        psw_str = ''
        for item in psw_hashed:
            psw_str = psw_str + str(int(item))
        # 处理响应
        login_response = requests.post(cfg.URLS['login'], data={'username': username, 'password': psw_str})
        global user_cookie
        user_cookie = login_response.cookies

        login_dict = json.loads(login_response.text)
        if judge(login_response.text):
            if username == 'test':
                return True, '测试账号登陆成功！' + login_dict['message']
            return True, '登陆成功！' + login_dict['message']
        return False, '登陆失败！' + login_dict['message']

    def query(self, path=''):
        global user_cookie
        lists_response = requests.get(cfg.URLS['list'] + '?' + 'path=' + path, cookies=user_cookie)
        # 处理响应
        list_res = json.loads(lists_response.text)
        msg = '查询成功！'
        print(lists_response.text)
        if list_res['status'] != 0:
            msg = '查询失败！' + list_res['message']
        if list_res['status'] == 0:
            for item in list_res['data']:
                print(item)
        return list_res['status'] == 0, msg

    def exit(self):
        print('886')
        exit(0)

    def exit_account(self):
        global user_cookie
        try:
            user_cookie = None
        except Exception as err:
            return False, '注销失败，错误信息：\n' + str(err)
        return True, '注销成功！'

    def download(self, path=''):
        global user_cookie
        global main_user
        if path.strip() == '':
            return False, '请输入下载文件路径！'
        download_response = requests.get(cfg.URLS['download'] + '?' + 'path=' + path, cookies=user_cookie)
        print(download_response.content)
        status = 1
        try:
            response_dict = json.loads(download_response.text)
        except:
            status = 0
            response_dict = {}
        print(response_dict)
        file_content = ''
        if status != 0:
            status = response_dict['status']
        else:
            file_content = download_response.text
            print(file_content)
           # with open(os.path.join())
        if status != 0:
            msg = '下载失败！' + response_dict['message']
        else:
            msg = '下载成功！'
        return status == 0, msg

    def upload(self, path='hello.txt'):
        global user_cookie
        with open(path, 'rb') as upload_file:
            upload_data = upload_file.read()
            file_info = os.stat(path)
        # print(upload_data)
        # print(file_info)
        # return
        cur_file_info = FileInfo(file_info.st_mode, file_info.st_mtime, path, os.path.getsize(path)).json_dump()
        print((cur_file_info))
        cur_file_info = parse.quote(cur_file_info, safe='')
        print((cur_file_info))
        upload_response = requests.post(cfg.URLS['upload'] + '?' + 'fileinfo=' + cur_file_info, data=upload_data,
                                        cookies=user_cookie)
        upload_res = upload_response.text
        print(upload_res)
        return False, '上传失败！'


if __name__ == '__main__':
    c = Client()
    c.login()
    c.upload()