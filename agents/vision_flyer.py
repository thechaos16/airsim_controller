
import os
from PIL import Image

import numpy as np

from agents.agent import Agent


class VisionFlyer(Agent):
    def __init__(self, client, move_type):
        super(VisionFlyer, self).__init__(client, move_type)
        self.client.start()

    def get_state(self):
        return self.client.get_state()

    def get_image(self, camera_number):
        return self.client.get_images(camera_number=camera_number)

    def save_image(self, image, path):
        self.client.save_image(path, image)

    def act(self):
        target_vel = [
            np.random.uniform(-1, 1),
            np.random.uniform(-1, 1),
            np.random.uniform(-1, 1)
        ]
        self.client.move(self.move_type, *target_vel)

    def run(self, loop_cnt=100):
        for epoch in range(loop_cnt):
            self.act()
            for cam in ['0', '1']:
                images = self.get_image(cam)
                for idx, img in enumerate(images):
                    self._save_image(img, idx, self._get_repr(cam, epoch, idx))

    @staticmethod
    def _get_repr(camera, epoch, idx):
        return '{}_{}_{}'.format(camera, epoch, idx)

    def _save_image(self, image, idx, name):
        height, width = image.height, image.width
        if idx == 0:
            image = np.fromstring(image.image_data_uint8, dtype=np.int8)
            image = image.reshape(height, width, 4)
            image = Image.fromarray(image, 'RGBA')
        else:
            image = np.array(image.image_data_float, dtype=np.float)
            image = 255 / np.maximum(np.ones(image.size), image)
            image = np.reshape(image, (height, width))
            image = Image.fromarray(image).convert('L')
        image.save(os.path.join(self.client.root_path, 'img_{}.png'.format(name)))