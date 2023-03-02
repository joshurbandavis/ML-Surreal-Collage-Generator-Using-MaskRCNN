import numpy as np
import cv2
from SilhouetteMatcher import *


images = np.load('Imcrop.npy',allow_pickle=True)
masks = np.load('Maskcrop.npy',allow_pickle=True)

search_index = SilhouetteMatcher()
search_index.construct_index(images, masks)


query_masks = []
for img, msk in zip(images, masks):
	for cropped_image, cropped_mask in zip(img, msk):
		query_masks.append(cropped_mask)


for query_mask in query_masks:
	query_mask.astype(np.uint8)
	return_values = search_index.query(query_mask)
	# return_values is a list of tuples: (image, alpha channel)
	cv2.imshow("original",query_mask.astype(np.uint8)*255)
	for i in range(len(return_values)):
		cv2.imshow("match-"+str(i),return_values[i][0])

	cv2.waitKey()

