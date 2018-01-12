# -*- coding: utf-8 -*-
import os, sys
import os.path
import shutil, random
import numpy as np

reload(sys)
sys.setdefaultencoding('utf-8')

def classify(indexfile, inputdir):
	urldict = {}
	file = open(indexfile)
	for line in file:
		try:
			elements = line.strip().split('\t')
			# print "elements", elements
			try:
				imagename = elements[1]
			except:
				continue
			imageurl = elements[0]
			imagefullname = os.path.join(inputdir,imagename)
			# print 'imagefullname', imagefullname
			if imagefullname[-3:] != 'jpg' or random.random() > 0.3:
				continue
			urldict[imagename] = imageurl
			for i in elements[2].split(' '):
				# label = i.decode('gbk')
				# label.encode('utf-8')
				label = i
				labelpath = os.path.join('materials', label)
				isexists = os.path.exists(labelpath)
				if not isexists:
					os.makedirs(labelpath)
				try:
					shutil.copy(imagefullname, labelpath)
				except:
					pass

		except:
				continue


classify('index.txt', 'share_folder')