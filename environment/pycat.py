import os
import sys


def main(file_name):
    if not os.path.exists(
            file_name
    ):
        print('not found,', file_name)
    with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read())


if __name__ == '__main__':
    main(sys.argv[1])
