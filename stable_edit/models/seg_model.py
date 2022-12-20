from segmentation_models_pytorch import Unet
from torch import nn
from torch.utils import model_zoo
from typing import Dict, Any
import re
import torch
class SegmentationModel:
    def __init__(self,
    ):
        self.weights_url="https://github.com/ternaus/people_segmentation/releases/download/0.0.1/2020-09-23a.zip"
        self.model=self.load_model(encoder_name="timm-efficientnet-b3")
        self.model.eval()
        
    def load_model(self,encoder_name,classes=1,encoder_weights=None):
        model = Unet(encoder_name=encoder_name, classes=classes, encoder_weights=encoder_weights)
        state_dict = model_zoo.load_url(self.weights_url, progress=True, map_location="cpu")["state_dict"]
        state_dict = self.rename_layers(state_dict, {"model.": ""})
        model.load_state_dict(state_dict)
        return model

    def rename_layers(self,state_dict: Dict[str, Any], rename_in_layers: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        for key, value in state_dict.items():
            for key_r, value_r in rename_in_layers.items():
                key = re.sub(key_r, value_r, key)

            result[key] = value
        return result

    def __call__(self,img):
        with torch.no_grad():
            predictions = self.model(img)
        return predictions