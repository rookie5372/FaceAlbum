
import cv2
import numpy as np
from matplotlib import pyplot as plt
from hog import Hog_descriptor
# from ocr import my_ocr
import os, pickle, pprint

svm_params = dict( kernal_type = cv2.SVM_LINEAR,
					svm_type = cv2.SVM_C_SVC,
					C = 2.67, gamma = 5)
SZ = 20
bin_n = 16
affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR
inversehash ={}



def readimages(root):
	folderpaths = os.listdir(root)
	allfortrain = {}
	for folder in folderpaths:
		folderpath = os.path.join(root,folder)
		if os.path.isdir(folderpath) == 0:
			continue
		trainingimages = []
		images = os.listdir(folderpath)
		for image in images:
			print "image",image
			fullfilename=os.path.join(folderpath,image)
			# results = my_ocr(fullfilename)
			img = cv2.imread(fullfilename, cv2.IMREAD_GRAYSCALE)
			# for result in results:
			# 	leftup = result['vertexes_location'][3]
			# 	rightdown = result['vertexes_location'][1]
			# 	pt1 = (leftup['x'],leftup['y'])
			# 	pt2 = (rightdown['x'],rightdown['y'])
			# 	color = np.int0((img[pt1[1],pt1[0]]+img[pt2[1],pt2[0]])/2)
			# 	cv2.rectangle(img, pt1, pt2, color,-1)
			try:
				size = max(img.shape[0],img.shape[1])
			except:
				print "gg"
				continue
			img = cv2.resize(img, (size,size))
			size = int(size/2)
			hog = Hog_descriptor(img, cell_size=size, bin_size=16)
			vector, img = hog.extract()
			vector = vector[0]
			trainingimages.append(vector)
		allfortrain[folder] = trainingimages
	return allfortrain
	  
def trainsvm(materials):
	svm = cv2.SVM()
	# svm.load('svm_image.txt')
	re1 = svm.get_support_vector_count()
	responses = []
	trainData = []
	for label, vectors in materials.items():
		labelhash = hash(label) % 1000000
		inversehash[labelhash] = label
		charact = np.float32(vectors).reshape(-1,64)
		for cha in charact:
			trainData.append(cha)
		for i in range(len(vectors)):
			responses.append(labelhash)

	trainData = np.array(trainData)
	# print "out",trainData
	responses = np.float32((np.array(responses))[:,np.newaxis])
	# print "reout",responses
	# responses =  np.float32((responses)[:,np.newaxis] )
	# print "responses",responses
	svm.train(trainData, responses, params = svm_params)
	re2 = svm.get_support_vector_count()
	print "re1",re1,"re2",re2
	svm.save('svm_face.dat')
	return svm


if __name__ == "__main__":
	trainsvm(readimages('materials'))
	dictoutput = open('classhash.pkl','wb')
	pickle.dump(inversehash, dictoutput)
	dictoutput.close()

