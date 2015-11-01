# -*- coding: utf-8 -*-
from gevent import monkey

monkey.patch_all()

from gevent.pool import Pool
import urllib2
import re
import os

all_pic_urls = []

base_url = "http://iconmatrix.sharpmark.net"
pic_save_path = './icons'


def get_page_count():
    f = urllib2.urlopen(base_url)
    content = f.read()
    result = re.findall('([0-9]+)\/\"\>尾页', content)
    pc = result[0]
    if pc[0].isalnum():
        return int(pc)
    return 0


def download_pic(pic_url):
    f = urllib2.urlopen(pic_url)
    name = os.path.basename(pic_url)
    with open(pic_save_path + name, "wb") as code:
        code.write(f.read())


def get_pic_urls(page_url):
    global all_pic_urls
    f = urllib2.urlopen(page_url)
    content = f.read()
    m = re.findall('\<img\sclass=\"redraw-icon\sicon-shadow\"\ssrc="(.*?)\"', content)
    all_pic_urls += m


if __name__ == '__main__':
    page_count = get_page_count()

    p = Pool(20)
    for i in xrange(1, page_count + 1):
        page_url = base_url + '/apps/page/%d/' % i
        p.spawn(get_pic_urls, page_url)
    p.join()

    jobs = []
    for pic_url in all_pic_urls:
        url = base_url + pic_url
        p.spawn(download_pic, url)
    p.join()