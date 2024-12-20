import os
import sys
sys.path.append(os.getcwd() + "/brain")
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import models



class Predictor:
    def __init__(self, model_path):
        model = models.DeepConvNet150()
        state_dict = torch.load(model_path,  map_location=torch.device('cpu'), weights_only=True)
        model.load_state_dict(state_dict)
        self.model = model
        self.model.eval()
        
    def predict(self, feature_matrix):
        with torch.no_grad():
            logits = self.model(torch.from_numpy(np.expand_dims(feature_matrix, axis= 0)))
            prediction = F.softmax(logits, dim=1)
        
        return prediction.numpy()
