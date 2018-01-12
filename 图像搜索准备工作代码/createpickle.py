# -*- coding: utf-8 -*-
import os, sys
import os.path
import shutil, pickle

reload(sys)
sys.setdefaultencoding('utf-8')

def classify(indexfile, inputdir):
	urldict = {}
	file = open(indexfile)
	for line in file:
		try:
			elements = line.strip().split('\t')
			# print "elements", elements
			imageurl = elements[0]
			labellist = elements[2].split(' ')
			urldict[imageurl] = labellist
		except:
				continue
	dictoutput = open('urltolabel.pkl','wb')
	pickle.dump(urldict, dictoutput)
	dictoutput.close()



classify('index.txt', 'img')