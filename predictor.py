import os
import sys
import numpy as np
import torch
import torch.nn as nn
from torchinfo import summary
import torch.nn.functional  as F
import models


class Predictor:
	def __init__(self, model_path):
		model = models.DeepConvNet150()
		state_dict = torch.load(model_path,  map_location=torch.device('cpu'))
		model.load_state_dict(state_dict)

		self.model = model

	def predict(self, feature_matrix):
		self.model.eval()
		logits = self.model(torch.from_numpy(np.expand_dims(feature_matrix, axis= 0)))
		prediction = F.softmax(logits, dim=1)
		return prediction.detach().numpy()
