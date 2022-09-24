import torch
import os
from PIL import Image
import shutil


class Detector:
    def __init__(self):
        self.model = torch.hub.load('../yolov5', 'custom',
                                    path='../data/best.pt', force_reload=True,
                                    source='local')

    def detect(self, path):
        images = []
        for image in os.listdir(path):
            images.append(Image.open(os.path.join(path, image)))

        self.results = self.model(images, size=2048)

    def save(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        self.results.save()
        cur_path = os.getcwd()
        for address, dirs, files in os.walk(os.path.join(cur_path, 'runs')):
            for name in files:
                os.replace(os.path.join(address, name), os.path.join(path, name))
        shutil.rmtree(os.path.join(cur_path, 'runs'))
