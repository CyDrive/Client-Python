import requests
import hashlib
import json
import client_config as cfg
from User import User
from Client import Client
import ast


def execute(cur_client, args=''):
    if '，' in args:
        args = args.replace('，', ',')
    args = args.split()

    cmd_map = cur_client.get_cmd_map()
    if args[0] not in cmd_map:
        return False, 'No such Command!'
    cmd_func = cmd_map[args[0]]

    parser_args = []
    for item in args[1:]:
        try:
            item = ast.literal_eval(item)
            parser_args.append(item)
        except ValueError as err:
            parser_args.append(item)

    try:
        status, msg = cmd_func(*parser_args)
        return status, msg
    except Exception as err:
        return False, err


if __name__ == '__main__':
    main_user = User()
    main_client = Client()
    while True:
        cmd_str = input()
        if cmd_str == '':
            continue
        status, msg = execute(main_client, cmd_str)
        print(status, msg)