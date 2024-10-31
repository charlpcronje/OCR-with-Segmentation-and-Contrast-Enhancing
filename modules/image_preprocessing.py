
# modules/image_preprocessing.py

import cv2
import numpy as np

class ImagePreprocessingModule:
    def __init__(self, config, logger):
        self.effects_to_try = config.get('effects_to_try')
        self.logger = logger

    def preprocess_image(self, image_path):
        self.logger.info(f"Preprocessing image: {image_path}")
        original_image = cv2.imread(image_path)
        processed_images = []
        
        # Apply all enabled effects sequentially
        image = original_image.copy()
        for effect in self.effects_to_try:
            if effect['enabled']:
                self.logger.debug(f"Applying effect: {effect['name']}")
                if effect['name'] == 'increase_contrast':
                    image = self._increase_contrast(image)
                elif effect['name'] == 'dehaze':
                    image = self._dehaze(image)
                elif effect['name'] == 'invert_colors':
                    image = self._invert_colors(image)
                elif effect['name'] == 'enhance_texture':
                    image = self._enhance_texture(image)
        processed_images.append(image)
        return processed_images


    def _increase_contrast(self, image):
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l_channel, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl = clahe.apply(l_channel)
        merged = cv2.merge((cl,a,b))
        final = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
        return final

    def _dehaze(self, image):
        # Simple dehazing using histogram equalization
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v_eq = cv2.equalizeHist(v)
        hsv_eq = cv2.merge((h, s, v_eq))
        final = cv2.cvtColor(hsv_eq, cv2.COLOR_HSV2BGR)
        return final

    def _invert_colors(self, image):
        return cv2.bitwise_not(image)

    def _enhance_texture(self, image):
        # Placeholder for texture enhancement
        return image
