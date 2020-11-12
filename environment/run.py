import os
import sys
import json
from collections import defaultdict

CMD_SAVE_PATH = r'C:\Users\yangyu\.run.json'

if not os.path.exists(CMD_SAVE_PATH):
    data = {}
else:
    try:
        with open(CMD_SAVE_PATH, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
    except Exception as e:
        data = {}


def save():
    with open(CMD_SAVE_PATH, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(data))


def join_cmd(cmd):
    data = ' '.join(cmd)
    lines = data.split('\\\\')
    return [line.strip() for line in lines]


def check_name(name):
    return name in ['set', 'del', 'exit']


def run_cmd(cmd, args=None):
    if args:
        cmd_str = '\\\\'.join(cmd)
        cmd_str = cmd_str % tuple(args)
        cmd = cmd_str.split('\\\\')
    for c in cmd:
        print('>> ',c)
        os.system(c)


def has_args(cmd):
    for c in cmd:
        if "%s" in c:
            return True
    return False


def main(args):
    action = args[0]
    if action == 'set':
        name = args[1]
        cmd = join_cmd(args[2:])
        if check_name(name):
            print(name, 'can not use')
            return
        data[name] = {}
        data[name]['cmds'] = cmd
        data[name]['args'] = has_args(cmd)
        save()
        print(name, ' : ', cmd)
    elif action == 'del':
        name = args[1]
        data.pop(name, None)
        save()
    else:
        cmds = join_cmd(args)
        for cmd in cmds:
            if cmd in data:
                run_cmd(data[cmd]['cmds'])
            else:
                name = args[0]
                if name in data:
                    if data[name]['args']:
                        run_cmd(data[name]['cmds'], args[1:])
                        return
                print(cmd, 'not found')


def input_args():
    while True:
        x = input('>')
        if x == 'exit':
            return
        main(x.split(' '))


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        input_args()
    else:
        main(args)
