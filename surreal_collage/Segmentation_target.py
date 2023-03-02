import torch, torchvision
print(torch.__version__, torch.cuda.is_available())
assert torch.__version__.startswith("1.8")   # please manually install torch 1.8 if Colab changes its default version
from matplotlib import pyplot as plt
import cv2
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

def get_objects(path, N):
    Boxes = []
    Masks = []
    for k in range(0,4):
        imageName = path+"target_"+str(k)+".jpeg"
        print(imageName)
        im = cv2.imread(imageName)

        cfg = get_cfg()
        # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.2  # set threshold for this model
        # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        predictor = DefaultPredictor(cfg)
        outputs = predictor(im)

        v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

        boxes = outputs["instances"].pred_boxes.tensor.cpu().numpy()
        masks = (outputs["instances"].pred_masks).to("cpu").numpy()

        Boxes.append(boxes)
        Masks.append(masks)

        return([boxes, masks])
    
# np.save("Target_Boxes.npy", np.array(Boxes))
# np.save("Target_Masks.npy", np.array(Masks))

path = "./target_img/"
N = 4
[boxes, masks] = get_objects(path, N)


