import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2
from SilhouetteMatcher import *

class Synthesizer:

    def __init__(self, target, source_list, locations_list, bounds_list):
        self.target = target
        self.source_list = source_list
        self.locations_list = locations_list
        self.bounds_list = bounds_list
        #self.img = np.array(Image.fromarray(self.target))
        self.img = np.array(Image.open(self.target))
        print(self.img)
        self.img = self.img[:, :, :3].copy()
        
    def overlay_all(self):
    #overlay each source png onto target image
        for i in range(len(self.source_list)):      
            self.overlay_img(i)
        plt.imshow(np.asarray(self.img))
        plt.show()
        Image.fromarray(self.img).save("result.png")
        
    def overlay_img(self, idx):
    #overlay source at index idx onto target image
        
        #retrieve source, location and bounds
        source = self.source_list[idx]
        x, y = self.locations_list[idx]
        bound_width, bound_height = bounds_list[idx]
        
        #scale overlay according to bounding box
        #img_overlay = Image.fromarray(source)
        img_overlay = Image.open(source)
        width, height = img_overlay.size
        scale = min(bound_width/width, bound_height/height)
        img_overlay = img_overlay.resize((int(width*scale), int(height*scale)))
        img_overlay = np.array(img_overlay)
        alpha_mask = img_overlay[:, :, 3] / 255.0
        img_overlay = img_overlay[:, :, :3]
    
        #obtain absolute bounds
        y1, y2 = max(0, y), min(self.img.shape[0], y + img_overlay.shape[0])
        x1, x2 = max(0, x), min(self.img.shape[1], x + img_overlay.shape[1])
        y1o, y2o = max(0, -y), min(img_overlay.shape[0], self.img.shape[0] - y)
        x1o, x2o = max(0, -x), min(img_overlay.shape[1], self.img.shape[1] - x)

        #if overlay out of bounds, do nothing
        if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
            return

        #crop and synthesize images
        img_crop = self.img[y1:y2, x1:x2]
        img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
        alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis]
        alpha_inv = 1.0 - alpha
        img_crop[:] = alpha * img_overlay_crop + alpha_inv * img_crop
        return(self.img)


    
'''

get_topk(target, sources):
    for each source image:
        get_sim_score(source, target)
        
    return topk sources, bounding boxes and masks
'''


if __name__ == "__main__":
    
    images = np.load('Imcrop.npy',allow_pickle=True)
    masks = np.load('Maskcrop.npy',allow_pickle=True)
    search_index = SilhouetteMatcher()
    search_index.construct_index(images, masks)
    return_values = search_index.query(query_mask)
    # return_values is a list of tuples: (image, alpha channel)
    
    target_boxes = np.load('Target_Boxes.npy', allow_pickle=True)
    boxes = target_boxes
    
    source_list = []
    
    source_tuples = []
    for source_tuple in source_tuples:
        source_array = np.concatenate((source_tuple[0], source_tuple[1]), axis=0)
        source_list.append(source_array)
    
    locations_list = []
    bounds_list = []
    for box in target_boxes[1]:
        locations_list.append((int(box[0]), int(box[1])))
        bounds_list.append((int(box[2]-box[0]), int(box[3]-box[1])))
        
    print(locations_list)
    print(bounds_list)
    
    
    target = "target_1.png"
    
    

    source_list = ["cup.png", "cup.png", "cup.png", "cup.png", "cup.png"]


    #synthesize_table = Synthesizer(target, source_list, locations_list, bounds_list)
    #synthesize_table.overlay_all()    
    
    '''
    target = "table.png"
    source_list = ["cup.png", "milk.png"]
    locations_list = [(900, 100), (1200, 100)]  #list of locations of top left coordinate of each source to be collaged onto target
    bounds_list = [(200, 200), (300, 200)]      #list of bounding boxes for each source
'''


    synthesize_table = Synthesizer(target, source_list, locations_list, bounds_list)
    synthesize_table.overlay_all()

    