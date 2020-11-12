import os
import sys
import re

BASE_DIR = os.getcwd()
default_exts = ['txt', 'py', 'yaml', 'json','md']


def list_text_file(exts, root_dir):
    for path in os.listdir(root_dir):
        abs_dir = os.path.join(root_dir, path)
        if os.path.isdir(abs_dir):
            yield from list_text_file(exts, abs_dir)
        else:
            name, ext = os.path.splitext(path)
            if ext.lstrip('.') in exts:
                yield abs_dir


def find_text_in_file(text, path):
    for encoding in ['utf-8', 'gkb']:
        try:
            with open(path, 'r', encoding=encoding) as f:
                for index, line in enumerate(f.readlines(), start=1):
                    if re.search(text, line):
                        print(path, index, ':', line)
            return
        except Exception as e:
            pass


def main():
    arg = sys.argv[1:]
    text, *exts = arg
    if not exts:
        exts = default_exts
    for file in list_text_file(exts, BASE_DIR):
        find_text_in_file(text, file)


if __name__ == '__main__':
    main()
