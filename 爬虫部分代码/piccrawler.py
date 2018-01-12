# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import urlparse
import os
import urllib
import sys

def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s

def get_page(page):
    content = ''
    try:
        content=urllib2.urlopen(page,timeout=10).read()
    except:
        pass
    return content

def get_srcandtag(content):
    soup=BeautifulSoup(content)
    picdiv=soup.find('div',{'class':'panel panel-default panel-body'})
    thepic=picdiv.find('img')
    src=thepic.get('src','')
    tag=thepic.get('alt','')
    return src,tag

def add_page_to_folder(page, content,i): #将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'    #index.txt中每行是'网址 对应的文件名'
    folder = 'img'                 #存放网页的文件夹

    index = open(index_filename, 'a')
    src,tag=get_srcandtag(content)

    splitPath = src.split('.')
    fTail = splitPath.pop()
    filename=str(i) + "." + fTail
    index.write(src+'\t'+"img/"+filename+'\t'+tag+'\n')
    index.close()
    
    if not os.path.exists(folder):  #如果文件夹不存在则新建
        os.mkdir(folder)
    u = urllib2.urlopen(src)
    thepic = u.read()
    f = open(filename,'wb+')
    f.write(thepic)


for i in range(665,10001):
    page="http://www.youbiaoqing.com/biaoqingbao/"+str(i)
    content = get_page(page)
    try:
        add_page_to_folder(page, content,i)
    except:
        pass
