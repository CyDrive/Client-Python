import requests
import hashlib
import json
import client_config as cfg
import django


class User:
    def __init__(self, user_id=-1, username='', password='', work_dir='', root_dir='download', remote_dir=''):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.work_dir = work_dir
        self.root_dir = root_dir
        self.remote_dir = remote_dir
        # self.cookie = ''

    def print(self):
        print(self.username)
        print(self.password)

    def json_load(self, src_json):
        user_dict = json.loads(src_json)
        for item in vars(self).items():
            if item[0] in user_dict and hasattr(self, item[0]):
                setattr(self, item[0], user_dict[item[0]])

    def json_dump(self, path='userinfo'):
        user_dict = {}
        for item in vars(self).items():
            user_dict[item[0]] = item[1]
        print(user_dict)


main_user = User()

if __name__ == '__main__':
    print(main_user.username, main_user.password)
    js = '{"username": "111", "password": "222"}'
    main_user.json_load(js)
    print(main_user.username, main_user.password)
    main_user.json_dump()