import cv2
# import imutils 
import numpy as np
import os, pickle
from scipy.cluster.vq import *
from sklearn.externals import joblib

from sklearn import preprocessing



def train(train_path):
	training_names = os.listdir(train_path)
	# 200 may cause memory error
	numWords = 100
	image_paths = []
	for training_name in training_names:
		image_path = os.path.join(train_path, training_name)
		image_paths += [image_path]


	fea_det = cv2.FeatureDetector_create("SIFT")
	des_ext = cv2.DescriptorExtractor_create("SIFT")

	des_list = []
	appendcount = 0
	true_paths = []
	for i, image_path in enumerate(image_paths):

		try:
			im = cv2.imread(image_path)
			print "EXTRACT SIFT OF %s image, %d of %d images" % (training_names[i], i, len(image_paths))
			kpts = fea_det.detect(im)
			kpts, des = des_ext.compute(im, kpts)
			print "dees", len(des)
			des_list.append((image_path, des))
			true_paths.append(image_path)
			appendcount += 1
			print "complete",appendcount
		except Exception, e:
			print "error: ",str(e)
			continue


	descriptors = des_list[0][1]
	for image_path, descriptor in des_list[1:]:
		print "descriptor", len(descriptor)
		descriptors = np.vstack((descriptors, descriptor))

	print "start k-means: %d words, %d keypoints" % (numWords, descriptors.shape[0])
	voc, variance = kmeans(descriptors, numWords, 1)

	im_features = np.zeros((appendcount, numWords), "float32")
	for i in xrange(appendcount):
		try:
			words, distance = vq(des_list[i][1], voc)
		except Exception, e:
			print str(e),"i", i
			continue

		for w in words:
			im_features[i][w] += 1

	nbr_occurences = np.sum((im_features>0) * 1, axis = 0)
	idf = np.array(np.log((1.0*appendcount+1)/(1.0*nbr_occurences + 1)), 'float32')

	im_features = im_features * idf
	im_features = preprocessing.normalize(im_features, norm = 'l2')
	# outfeature = []
	# for feature in im_features:
	# 	isum = np.sum(feature**2) ** 0.5
	# 	feature = feature / isum
	# 	print "feature", feature
	# 	outfeature.append(feature)
	# outfeature = np.array(outfeature)
	# im_features = outfeature
	# print "imfeature", im_features

	joblib.dump((im_features, true_paths, idf, numWords, voc),"bof.pkl", compress = 3)
	# dictoutput = open('bof.pkl','wb')
	# pickle.dump((im_features, image_paths, idf, numWords, voc), dictoutput)
	# dictoutput.close()
	


train('bowtrain')