import os
import sys


def parse_ps(line):
    lines = line.split("        ")
    lines = [line.strip() for line in lines if line.strip()]
    if lines:
        return lines[0], lines[1]
    return None, None


def parse(f):
    d = f._stream.buffer.read().decode('utf-8')

    for line in d.split('\n'):
        parse_ps(line)
        c_id, i = parse_ps(line)
        yield c_id, i


def main(image):
    f = os.popen('docker ps')

    for c_id, i in parse(f):
        if image == i:
            os.system(f'docker stop {c_id}')
    f = os.popen('docker ps -a')
    for c_id, i in parse(f):
        if image == i:
            os.system(f'docker rm {c_id}')
    os.system(f'docker rmi {image}')


if __name__ == '__main__':
    images = sys.argv[1:]
    for image in images:
        main(image)
