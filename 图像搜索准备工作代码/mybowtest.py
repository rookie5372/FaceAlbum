import cv2
# import imutils 
import numpy as np
import os, pickle, re
from scipy.cluster.vq import *
from sklearn.externals import joblib

from sklearn import preprocessing


def search(image_path, candidatenum):
	pklfile = open('bof.pkl','rb')
	im_features, true_paths, idf, numWords, voc = joblib.load(pklfile)

	fea_det = cv2.FeatureDetector_create('SIFT')
	des_ext = cv2.DescriptorExtractor_create('SIFT')

	des_list = []

	im = cv2.imread(image_path)
	kpts = fea_det.detect(im)
	kpts, des = des_ext.compute(im, kpts)

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
		print "imagename", imagename
		print urldict[imagename]
		urllist.append(urldict[imagename])

	return urllist




search('589.jpg', 6)