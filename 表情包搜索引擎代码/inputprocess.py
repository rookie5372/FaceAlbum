# -*- coding=utf-8 -*-
import cv2
import numpy as np
from math import *
import base64
import urllib, urllib2, sys
import os, pickle, re
from scipy.cluster.vq import *
from sklearn.externals import joblib

from sklearn import preprocessing
from svmtest import *


# at the beginning of web.py
pklfile = open('urltolabel.pkl','rb')
urltolabeldict = pickle.load(pklfile)

def my_ocr(filename):
	myaccesstoken  = "24.9011b0eb3441015717516710bd7a729e.2592000.1516807360.282335-10583245"
	ocr_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"

	img = open(filename, "rw")
	img = img.read()
	img = base64.b64encode(img)

	#得到结果字典
	options = {}
	options['image'] = img
	options["vertexes_location"] = "true"
	options['access_token'] = myaccesstoken
	mydata = urllib.urlencode(options)
	req = urllib2.Request(ocr_url, data = mydata)
	req.add_header("Content-Type", "application/x-www-form-urlencoded")

	content = urllib2.urlopen(req).read()
	content = eval(content)
	#词-words 矩形框-vertexes_location 
	if not 'words_result' in content.keys():
		return []
	return content['words_result']


def search(image_path, candidatenum):
	pklfile = open('bof.pkl','rb')
	im_features, true_paths, idf, numWords, voc = joblib.load(pklfile)

	fea_det = cv2.FeatureDetector_create('SIFT')
	des_ext = cv2.DescriptorExtractor_create('SIFT')

	des_list = []

	img = cv2.imread(image_path)

	allwords = []
	results = my_ocr(image_path)
	for result in results:
		allwords.append(result['words'])
		leftup = result['vertexes_location'][3]
		rightdown = result['vertexes_location'][1]
		pt1 = (leftup['x'],leftup['y'])
		pt2 = (rightdown['x'],rightdown['y'])
		color = np.int0((img[pt1[1],pt1[0]]+img[pt2[1],pt2[0]])/2)
		cv2.rectangle(img, pt1, pt2, color,-1)

	kpts = fea_det.detect(img)
	kpts, des = des_ext.compute(img, kpts)

	des_list.append((image_path, des))

	descriptors = des_list[0][1]

	test_features = np.zeros((1, numWords), 'float32')
	words, distance = vq(descriptors, voc)
	for w in words:
		test_features[0][w] += 1
	
	test_features = test_features * idf
	test_features = preprocessing.normalize(test_features, norm = 'l2')


	# distances = []
	# test_vector = np.array(test_features[0])
	# for imvector in im_features:
	# 	imvector = np.array(imvector)
	# 	dis = np.linalg.norm(test_vector - imvector)
	# 	distances.append(dis)
	# distances = np.array(distances)
	
	score = np.dot(test_features, im_features.T)
	rank_ID = np.argsort(-score)

	pklfile = open('urldict.pkl','rb')
	urldict = pickle.load(pklfile)
	urllist = []

	for i , ID in enumerate(rank_ID[0][0:candidatenum]):
		# if image_paths[ID] == "bowtrain/1.jpg":
		# 	print "that is", i
		path = true_paths[ID]
		imagename = re.findall('/(.*)', path)[0]

		urllist.append(urldict[imagename])

	return urllist, allwords

def elementsinput(image_path, candidatenum):
	urllist, allwords = search(image_path, candidatenum)
	label = svmmainsearch(image_path)
	return urllist, label, allwords

# print elementsinput('test.jpg', 5)
