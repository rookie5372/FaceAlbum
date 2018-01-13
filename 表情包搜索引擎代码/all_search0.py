#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys

reload(sys)
sys.setdefault
encoding('utf-8')

import envir

import base64

import urllib, urllib2, sys

from math import *

from inputprocess import *


#返回值[[url,[tag1, tag2, ...]], []]

#其中tag和suggest不一定有，记得判断下再显示网页

def text_search(command):
    
envir.vm_env.attachCurrentThread()
    
query = envir.QueryParser(envir.Version.LUCENE_CURRENT, "tag",
                            envir.analyzer).parse(command)

    
scoreDocs = envir.searcher.search(query, 20).scoreDocs
    
res = []

    
suggestions = list(envir.spellchecker.suggestSimilar(command, 5))

    
for scoreDoc in scoreDocs:
        
	doc = envir.searcher.doc(scoreDoc.doc)
  
	temp={}
      
	temp['imgurl'] = doc.get("src")
        
	res.append(temp)
    
return res,suggestions




#
def img_search(filename):
    
#使用bow获取最相似图片 SVM获取最可能标签 OCR获取图中文字
    
pic_res, tag, words = elementsinput(filename, candidatenum = 20)

    
#进行图中文字检索
    
envir.vm_env.attachCurrentThread()
    
querys = envir.BooleanQuery()
    
#图片中的文字选择性出现，因为OCR可能有错
    
for word in words:
        
query = envir.QueryParser(envir.Version.LUCENE_CURRENT, "tag", envir.analyzer).parse(word)
        
querys.add(query, envir.BooleanClause.Occur.SHOULD)
    
    
#SVM中的标签必须出现
    
query = envir.QueryParser(envir.Version.LUCENE_CURRENT, "tag", envir.analyzer).parse(tag)
    
querys.add(query, envir.BooleanClause.Occur.MUST)

   
 #查询
    
scoreDocs = envir.searcher.search(querys, 20).scoreDocs
    word_res = []
    for scoreDoc in scoreDocs:
       
doc = envir.searcher.doc(scoreDoc.doc)
  
temp={}
      
temp['imgurl'] = doc.get("src")
            
word_res.append(temp)


    
return pic_res, word_res





