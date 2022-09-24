import torch
import os
from PIL import Image


class Detector:
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:\\Programming projects\\Python\\Hackaton\\data\\best.pt', force_reload=True)

    def detect(self, path):
        images = []
        for image in os.listdir(path):
            images.append(Image.open(os.path.join(path, image)))

        self.results = self.model(images[0], size=2048)

    def save(self):
        self.results.save()
