# coding:utf-8

import urllib2
import os
from multiprocessing import Pool
import bsddb


# sketch56494.zip
# http://www.openprocessing.org/sketch/56533/download/sketch.zip
target = 'openprocessing'
db = bsddb.btopen('openprocessing-log/log.db', 'c')


def download(number):
    file_path = os.path.join(target, 'sketch%s.zip' % number)
    url = 'http://www.openprocessing.org/sketch/%s/download/sketch.zip' % number
    u = urllib2.urlopen(url)
    f = open(file_path, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_path, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print status,

    f.close()


def download10files(number):
    ###
    # 下载10个文件
    # number = 0, 0-9
    # number = 1, 10-19
    ###
    for i in range(number * 10, number * 10 + 10):
        file_name = 'sketch%s.zip' % i
        file_path = get_target(i)
        if not os.path.exists(file_path):
            url = 'http://www.openprocessing.org/sketch/%s/download/sketch.zip' % number
            try:
                http_file = urllib2.urlopen(url)
                output = open(file_path, 'wb')
                output.write(http_file.read())
                output.close()
                db[file_name] = '0'
                print('succ %s' % i)
            except:
                db[file_name] = '1'
                print('fail %s' % i)
                ''
        else:
            print('pass %s' % i)


def get_target(number, base='processing-group'):
    sub_folder = str(number / 1000)
    target_dir = os.path.join(base, sub_folder)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    res = os.path.join(target_dir, ('sketch%s.zip' % number))
    return res


if __name__ == '__main__':
    p = Pool(32)
    # p.map(download10files, range(0, 1000))  # 1-10,000
    # p.map(download10files, range(1000, 2000))  # 1-10,000
    # p.map(download10files, range(2000, 3000))  # 1-10,000
    # p.map(download10files, range(3000, 4000))  # 1-10,000
    # p.map(download10files, range(4000, 5000))  # 1-10,000
    # p.map(download10files, range(5000, 6000))  # 1-10,000
    # p.map(download10files, range(6000, 7000))  # 1-10,000
    # p.map(download10files, range(7000, 8000))  # 1-10,000
    # p.map(download10files, range(8000, 9000))  # 1-10,000
    # p.map(download10files, range(9000, 10000))  # 1-10,000

    def get_range(base_number, step=1000, multi=1000):
        return range(base_number * multi, base_number * multi * 10 + step)

    # p.map(download10files, get_range(10))  # 100000-110000
    for i in (range(10, 20)):
        p.map(download10files, get_range(11))
