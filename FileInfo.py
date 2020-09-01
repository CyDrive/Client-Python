import requests
import hashlib
import json
import client_config as cfg


class FileInfo:
    def __init__(self, filemode=1, modifytime=0, filepath='', size=0, isdir=False):
        self.file_mode = filemode
        self.modify_time = int(modifytime)
        self.file_path = filepath
        self.size = size
        self.is_dir = isdir
        # self.IsCompressed = self.Size>
        self.is_compressed = False

    def json_dump(self):
        instance_map = {}
        for item in vars(self).items():
            instance_map[item[0]] = item[1]
        return json.dumps(instance_map)


if __name__ == '__main__':
    s = FileInfo()
    print(s.json_dump())
    print(type(s.json_dump()))