import numpy as np
import cv2


class SilhouetteMatcher():
	"""SilhouetteMatcher manages all steps associated with image matching"""
	def __init__(self):

		self.collection_src = []
		self.collection_internal_mask = []
		self.internal_representation_size = (128,128)

	def add_to_index(self, image_src, mask):
		# image: image matrix, filename, or other identifier for a source image
		# mask: binary mask (1s and 0s) with 1s wherever mask is TRUE
		self.collection_src.append((image_src,mask))
		self.collection_internal_mask.append(self.preprocess_mask(mask))
		return

	def construct_index(self, image_set, mask_set):
		for images, masks in zip(image_set, mask_set):
			for cropped_image, cropped_mask in zip(images, masks):
				self.add_to_index(cropped_image, cropped_mask.astype(np.uint8))

	def query(self, query_mask, k = 3):
		# query mask: binary mask from target image, that we want to find matches for
		# k: number of top matches to return
		query_mask_internal = self.preprocess_mask(query_mask.astype(np.uint8))

		iou_scores = np.zeros(len(self.collection_internal_mask), dtype = float)
		for idx, mask_internal in enumerate(self.collection_internal_mask):
			iou_scores[idx] = self.IOU_metric(mask_internal, query_mask_internal)

		# get indices of top-k scores
		idx = np.argpartition(iou_scores, -k)[-k:]
		# sort index by iou score
		idx = idx[np.argsort(iou_scores[idx])]
		print(idx)
		return_images = []
		for i in reversed(idx):
			return_images.append(self.collection_src[i])
		return return_images

	def IOU_metric(self, mask_a, mask_b):
		# masks are numpy 1/0 arrays
		intersection = mask_a * mask_b
		union = np.clip(mask_a + mask_b, 0, 1)
		
		union_count = np.sum(union)
		intersection_count = np.sum(intersection)

		if union_count <= 0:
			return 0
		else: 
			return float(intersection_count)/union_count

	def preprocess_mask(self, mask):
		# preprocess mask so that we can add it to the search index

		# 1. resize mask so that dimensions of bounding box are <= self.internal_representation_size

		scale_factor = 1
		if mask.shape[0] > self.internal_representation_size[0]:
			scale_factor = min(scale_factor, self.internal_representation_size[0]/(mask.shape[0]+10))

		if mask.shape[1] > self.internal_representation_size[1]:
			scale_factor = min(scale_factor, self.internal_representation_size[1]/(mask.shape[1]+10))

		scaled_mask = cv2.resize(mask, None, fx=scale_factor, fy=scale_factor)


		# 2. create the internal mask representation of size equal to self.internal_representation_size
		internal_representation = np.zeros(self.internal_representation_size, dtype=np.uint8)

		# 3. find the offset value by 95th percentile mean
		# HAHA NOPE NAH HA! JUST PUT IT IN THE MIDDLE

		offset_y = int( (self.internal_representation_size[0] - scaled_mask.shape[0])/2 )
		offset_x = int( (self.internal_representation_size[1] - scaled_mask.shape[1])/2 )
		offset_x = max(0,offset_x)
		offset_y = max(0,offset_y)
	
		internal_representation[offset_y:offset_y+scaled_mask.shape[0],offset_x:offset_x+scaled_mask.shape[1]] = scaled_mask

		return internal_representation
